from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from turfs.models import Turf, MaintenanceBlock
from turfs.forms import TurfForm, MaintenanceBlockForm
from bookings.models import Booking


def is_admin(user):
    return user.is_staff


@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def dashboard_home(request):
    total_turfs = Turf.objects.count()
    total_users = User.objects.count()
    total_bookings = Booking.objects.count()
    todays_bookings = Booking.objects.filter(booking_date=timezone.now().date()).count()
    recent_bookings = Booking.objects.select_related('user', 'turf')[:5]

    context = {
        'total_turfs': total_turfs,
        'total_users': total_users,
        'total_bookings': total_bookings,
        'todays_bookings': todays_bookings,
        'recent_bookings': recent_bookings,
    }
    return render(request, 'dashboard/dashboard_home.html', context)


@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def dashboard_turfs(request):
    turfs = Turf.objects.all().order_by('-created_at')
    return render(request, 'dashboard/dashboard_turfs.html', {'turfs': turfs})


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
    return render(request, 'dashboard/dashboard_bookings.html', {'bookings': bookings})


@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def dashboard_users(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'dashboard/dashboard_users.html', {'users': users})


@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def dashboard_maintenance(request):
    blocks = MaintenanceBlock.objects.select_related('turf').all()
    return render(request, 'dashboard/dashboard_maintenance.html', {'blocks': blocks})


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
                block.save()
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
