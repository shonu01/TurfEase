from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import transaction
from datetime import datetime, date, timedelta
from decimal import Decimal
from turfs.models import Turf, MaintenanceBlock
from .models import Booking
from .forms import BookingForm


@login_required
def book_turf(request, turf_id):
    turf = get_object_or_404(Turf, pk=turf_id)

    # Admin/staff cannot book — they only manage
    if request.user.is_staff:
        messages.error(request, 'Admin accounts cannot book turfs. Please use a regular account.')
        return redirect('turf_detail', pk=turf_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking_date = form.cleaned_data['booking_date']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            members = form.cleaned_data['members']

            # Validate booking date is not in the past
            if booking_date < date.today():
                messages.error(request, 'You cannot book a turf for a past date.')
                return render(request, 'booking_form.html', {'form': form, 'turf': turf})

            # Validate end time is after start time
            if end_time <= start_time:
                messages.error(request, 'End time must be after start time.')
                return render(request, 'booking_form.html', {'form': form, 'turf': turf})

            # If booking is today, ensure start time is in the future
            if booking_date == date.today() and start_time <= datetime.now().time():
                messages.error(request, 'Start time must be in the future for today\'s bookings.')
                return render(request, 'booking_form.html', {'form': form, 'turf': turf})

            # Check maintenance blocks
            maintenance_conflict = MaintenanceBlock.objects.filter(
                turf=turf,
                date=booking_date,
                start_time__lt=end_time,
                end_time__gt=start_time,
            ).exists()

            if maintenance_conflict:
                messages.error(request, 'This time slot is blocked for maintenance. Please choose a different time.')
                return render(request, 'booking_form.html', {'form': form, 'turf': turf})

            # Calculate total price
            start_dt = datetime.combine(booking_date, start_time)
            end_dt = datetime.combine(booking_date, end_time)
            hours = Decimal(str((end_dt - start_dt).total_seconds() / 3600))
            total_price = turf.price_per_hour * hours

            # Add fixed surcharge based on team size
            if members == 5:
                total_price += turf.price_5a_side
            elif members == 7:
                total_price += turf.price_7a_side
            elif members == 11:
                total_price += turf.price_11a_side

            # Store booking data in session for confirmation step
            request.session['pending_booking'] = {
                'turf_id': turf.pk,
                'booking_date': str(booking_date),
                'start_time': str(start_time),
                'end_time': str(end_time),
                'members': members,
                'total_price': str(total_price),
            }
            return redirect('confirm_booking')
    else:
        form = BookingForm()

    return render(request, 'booking_form.html', {'form': form, 'turf': turf})


@login_required
def confirm_booking(request):
    pending = request.session.get('pending_booking')
    if not pending:
        messages.error(request, 'No pending booking found.')
        return redirect('turf_list')

    turf = get_object_or_404(Turf, pk=pending['turf_id'])
    booking_date = date.fromisoformat(pending['booking_date'])
    start_time = datetime.strptime(pending['start_time'], '%H:%M:%S').time()
    end_time = datetime.strptime(pending['end_time'], '%H:%M:%S').time()
    members = pending['members']
    total_price = Decimal(pending['total_price'])

    if request.method == 'POST':
        # Atomic check to prevent double-booking the same slot
        with transaction.atomic():
            overlapping = Booking.objects.select_for_update().filter(
                turf=turf,
                booking_date=booking_date,
                start_time__lt=end_time,
                end_time__gt=start_time,
            ).exists()

            if overlapping:
                del request.session['pending_booking']
                messages.error(request, 'This time slot was just booked by someone else. Please choose a different time.')
                return redirect('book_turf', turf_id=turf.pk)

            Booking.objects.create(
                user=request.user,
                turf=turf,
                booking_date=booking_date,
                start_time=start_time,
                end_time=end_time,
                members=members,
                total_price=total_price,
            )

        del request.session['pending_booking']
        messages.success(request, f'Turf booked successfully! Total: ₹{total_price}')
        return redirect('booking_history')

    context = {
        'turf': turf,
        'booking_date': booking_date,
        'start_time': start_time,
        'end_time': end_time,
        'members': dict(Booking.MEMBER_CHOICES).get(members, members),
        'total_price': total_price,
    }
    return render(request, 'booking_confirm.html', context)


@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)

    # Only allow cancelling future bookings
    if booking.booking_date < date.today():
        messages.error(request, 'You cannot cancel a past booking.')
        return redirect('booking_history')

    if booking.booking_date == date.today() and booking.start_time <= datetime.now().time():
        messages.error(request, 'You cannot cancel a booking that has already started.')
        return redirect('booking_history')

    if request.method == 'POST':
        booking.delete()
        messages.success(request, 'Booking cancelled successfully!')
        return redirect('booking_history')

    return render(request, 'booking_cancel.html', {'booking': booking})


@login_required
def booking_history(request):
    bookings = Booking.objects.filter(user=request.user).select_related('turf')

    # Filter by date
    filter_date = request.GET.get('date', '')
    if filter_date:
        bookings = bookings.filter(booking_date=filter_date)

    # Filter by turf name
    search = request.GET.get('q', '')
    if search:
        bookings = bookings.filter(turf__name__icontains=search)

    paginator = Paginator(bookings, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search': search,
        'filter_date': filter_date,
    }
    return render(request, 'booking_history.html', context)


@login_required
def booking_receipt(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    return render(request, 'booking_receipt.html', {'booking': booking})
