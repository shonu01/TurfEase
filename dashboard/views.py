from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.utils import timezone
from django.db import models, transaction
from turfs.models import Turf, MaintenanceBlock
from turfs.forms import TurfForm, MaintenanceBlockForm
from bookings.models import Booking, CancelledBooking, Notification


def is_admin(user):
    return user.is_staff


@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def dashboard_home(request):
    total_turfs = Turf.objects.count()
    total_users = User.objects.count()
    total_bookings = Booking.objects.count()
    todays_bookings = Booking.objects.filter(booking_date=timezone.now().date()).count()
    total_cancelled = CancelledBooking.objects.count()
    total_refunded = CancelledBooking.objects.aggregate(total=models.Sum('refund_amount'))['total'] or 0
    recent_bookings = Booking.objects.select_related('user', 'turf')[:5]
    recent_cancelled = CancelledBooking.objects.select_related('user')[:5]

    context = {
        'total_turfs': total_turfs,
        'total_users': total_users,
        'total_bookings': total_bookings,
        'todays_bookings': todays_bookings,
        'total_cancelled': total_cancelled,
        'total_refunded': total_refunded,
        'recent_bookings': recent_bookings,
        'recent_cancelled': recent_cancelled,
    }
    return render(request, 'dashboard/dashboard_home.html', context)


@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def dashboard_turfs(request):
    turfs = Turf.objects.all().order_by('-created_at')

    search = request.GET.get('q', '')
    if search:
        from django.db.models import Q
        turfs = turfs.filter(
            Q(name__icontains=search) | Q(location__icontains=search)
        )

    paginator = Paginator(turfs, 12)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'dashboard/dashboard_turfs.html', {
        'page_obj': page_obj,
        'search': search,
    })


@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def add_turf(request):
    if request.method == 'POST':
        form = TurfForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Turf added successfully!')
            return redirect('dashboard_turfs')
    else:
        form = TurfForm()
    return render(request, 'dashboard/turf_form.html', {'form': form, 'title': 'Add Turf'})


@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def edit_turf(request, pk):
    turf = get_object_or_404(Turf, pk=pk)
    if request.method == 'POST':
        form = TurfForm(request.POST, request.FILES, instance=turf)
        if form.is_valid():
            form.save()
            messages.success(request, 'Turf updated successfully!')
            return redirect('dashboard_turfs')
    else:
        form = TurfForm(instance=turf)
    return render(request, 'dashboard/turf_form.html', {'form': form, 'title': 'Edit Turf'})


@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def delete_turf(request, pk):
    turf = get_object_or_404(Turf, pk=pk)
    if request.method == 'POST':
        turf.delete()
        messages.success(request, 'Turf deleted successfully!')
        return redirect('dashboard_turfs')
    return render(request, 'dashboard/confirm_delete.html', {'turf': turf})


@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def dashboard_bookings(request):
    bookings = Booking.objects.select_related('user', 'turf').all()

    search = request.GET.get('q', '')
    if search:
        from django.db.models import Q
        bookings = bookings.filter(
            Q(user__username__icontains=search) | Q(turf__name__icontains=search)
        )

    filter_date = request.GET.get('date', '')
    if filter_date:
        bookings = bookings.filter(booking_date=filter_date)

    paginator = Paginator(bookings, 15)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'dashboard/dashboard_bookings.html', {
        'page_obj': page_obj,
        'search': search,
        'filter_date': filter_date,
    })


@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def dashboard_users(request):
    users = User.objects.all().order_by('-date_joined')

    search = request.GET.get('q', '')
    if search:
        from django.db.models import Q
        users = users.filter(
            Q(username__icontains=search) | Q(email__icontains=search)
        )

    paginator = Paginator(users, 15)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'dashboard/dashboard_users.html', {
        'page_obj': page_obj,
        'search': search,
    })


@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def dashboard_maintenance(request):
    blocks = MaintenanceBlock.objects.select_related('turf').all()

    search = request.GET.get('q', '')
    if search:
        blocks = blocks.filter(turf__name__icontains=search)

    paginator = Paginator(blocks, 15)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'dashboard/dashboard_maintenance.html', {
        'page_obj': page_obj,
        'search': search,
    })


@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def add_maintenance(request):
    if request.method == 'POST':
        form = MaintenanceBlockForm(request.POST)
        if form.is_valid():
            block = form.save(commit=False)
            if block.end_time <= block.start_time:
                messages.error(request, 'End time must be after start time.')
            else:
                # Find bookings that conflict with this maintenance window
                conflicting_bookings = Booking.objects.select_related('user', 'turf').filter(
                    turf=block.turf,
                    booking_date=block.date,
                    start_time__lt=block.end_time,
                    end_time__gt=block.start_time,
                )

                with transaction.atomic():
                    block.save()

                    cancelled_count = 0
                    for booking in conflicting_bookings:
                        # Create refund/cancellation record (full cashback)
                        cancelled = CancelledBooking.objects.create(
                            user=booking.user,
                            turf=booking.turf,
                            turf_name=booking.turf.name,
                            turf_location=booking.turf.location,
                            booking_date=booking.booking_date,
                            start_time=booking.start_time,
                            end_time=booking.end_time,
                            members=booking.members,
                            original_price=booking.total_price,
                            refund_amount=booking.total_price,
                            reason=f'Maintenance: {block.reason}' if block.reason else 'Cancelled due to scheduled maintenance',
                        )

                        # Notify the user
                        Notification.objects.create(
                            user=booking.user,
                            title='Booking Cancelled — Full Refund',
                            message=(
                                f'Your booking for {booking.turf.name} on {booking.booking_date.strftime("%b %d, %Y")} '
                                f'({booking.start_time.strftime("%I:%M %p")} – {booking.end_time.strftime("%I:%M %p")}) '
                                f'has been cancelled due to maintenance. '
                                f'A full cashback of ₹{booking.total_price} has been issued.'
                            ),
                            link=f'/bookings/cancelled-receipt/{cancelled.pk}/',
                        )

                        booking.delete()
                        cancelled_count += 1

                if cancelled_count > 0:
                    messages.warning(
                        request,
                        f'Maintenance block added. {cancelled_count} conflicting booking(s) were auto-cancelled '
                        f'with full cashback. Affected users have been notified.'
                    )
                else:
                    messages.success(request, 'Maintenance block added successfully!')
                return redirect('dashboard_maintenance')
    else:
        form = MaintenanceBlockForm()
    return render(request, 'dashboard/maintenance_form.html', {'form': form, 'title': 'Add Maintenance Block'})


@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def delete_maintenance(request, pk):
    block = get_object_or_404(MaintenanceBlock, pk=pk)
    if request.method == 'POST':
        block.delete()
        messages.success(request, 'Maintenance block removed!')
        return redirect('dashboard_maintenance')
    return render(request, 'dashboard/confirm_delete_maintenance.html', {'block': block})


@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def export_bookings_csv(request):
    import csv

    bookings = Booking.objects.select_related('user', 'turf').all().order_by('-booking_date')

    # Apply same filters as the bookings page
    search = request.GET.get('q', '')
    if search:
        from django.db.models import Q
        bookings = bookings.filter(
            Q(user__username__icontains=search) | Q(turf__name__icontains=search)
        )
    filter_date = request.GET.get('date', '')
    if filter_date:
        bookings = bookings.filter(booking_date=filter_date)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="turfease_bookings_{timezone.now().strftime("%Y%m%d")}.csv"'

    writer = csv.writer(response)
    writer.writerow(['#', 'User', 'Email', 'Turf', 'Location', 'Date', 'Start Time', 'End Time', 'Members', 'Total Price', 'Booked On'])

    for i, b in enumerate(bookings, 1):
        writer.writerow([
            i,
            b.user.username,
            b.user.email,
            b.turf.name,
            b.turf.location,
            b.booking_date.strftime('%Y-%m-%d'),
            b.start_time.strftime('%I:%M %p'),
            b.end_time.strftime('%I:%M %p'),
            b.get_members_display(),
            str(b.total_price),
            b.created_at.strftime('%Y-%m-%d %H:%M'),
        ])

    return response


@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def dashboard_cancelled(request):
    cancelled = CancelledBooking.objects.select_related('user', 'turf').all()

    search = request.GET.get('q', '')
    if search:
        from django.db.models import Q
        cancelled = cancelled.filter(
            Q(user__username__icontains=search) | Q(turf_name__icontains=search)
        )

    filter_date = request.GET.get('date', '')
    if filter_date:
        cancelled = cancelled.filter(booking_date=filter_date)

    paginator = Paginator(cancelled, 15)
    page_obj = paginator.get_page(request.GET.get('page'))

    total_refunded = CancelledBooking.objects.aggregate(total=models.Sum('refund_amount'))['total'] or 0

    return render(request, 'dashboard/dashboard_cancelled.html', {
        'page_obj': page_obj,
        'search': search,
        'filter_date': filter_date,
        'total_refunded': total_refunded,
    })
