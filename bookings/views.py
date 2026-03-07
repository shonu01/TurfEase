from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from datetime import datetime, timedelta
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

            # Validate end time is after start time
            if end_time <= start_time:
                messages.error(request, 'End time must be after start time.')
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

            # Atomic check to prevent double-booking the same slot
            with transaction.atomic():
                overlapping = Booking.objects.select_for_update().filter(
                    turf=turf,
                    booking_date=booking_date,
                    start_time__lt=end_time,
                    end_time__gt=start_time,
                ).exists()

                if overlapping:
                    messages.error(request, 'This time slot is already booked. Please choose a different time.')
                    return render(request, 'booking_form.html', {'form': form, 'turf': turf})

                # Calculate total price
                start_dt = datetime.combine(booking_date, start_time)
                end_dt = datetime.combine(booking_date, end_time)
                hours = Decimal(str((end_dt - start_dt).total_seconds() / 3600))
                total_price = turf.price_per_hour * hours

                # Add fixed surcharge for 5-a-side or 7-a-side
                if members == 5:
                    total_price += turf.price_5a_side
                elif members == 7:
                    total_price += turf.price_7a_side

                # Save booking
                booking = form.save(commit=False)
                booking.user = request.user
                booking.turf = turf
                booking.total_price = total_price
                booking.save()

            messages.success(request, f'Turf booked successfully! Total: ₹{total_price}')
            return redirect('booking_history')
    else:
        form = BookingForm()

    return render(request, 'booking_form.html', {'form': form, 'turf': turf})


@login_required
def booking_history(request):
    bookings = Booking.objects.filter(user=request.user).select_related('turf')
    return render(request, 'booking_history.html', {'bookings': bookings})
