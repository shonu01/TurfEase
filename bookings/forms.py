from django import forms
from .models import Booking

# Generate chronologically ordered time choices (6:00 AM – 11:30 PM)
TIME_CHOICES = [('', 'Select time')]
for h24 in range(6, 24):
    for minute in ('00', '30'):
        hour12 = h24 % 12 or 12
        period = 'AM' if h24 < 12 else 'PM'
        label = f'{hour12}:{minute} {period}'
        value = f'{h24:02d}:{minute}'
        TIME_CHOICES.append((value, label))


class BookingForm(forms.ModelForm):
    start_time = forms.TimeField(
        widget=forms.Select(
            attrs={'class': 'form-control time-select'},
            choices=TIME_CHOICES,
        ),
    )
    end_time = forms.TimeField(
        widget=forms.Select(
            attrs={'class': 'form-control time-select'},
            choices=TIME_CHOICES,
        ),
    )

    class Meta:
        model = Booking
        fields = ['booking_date', 'start_time', 'end_time', 'members']
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'members': forms.Select(attrs={'class': 'form-control'}),
        }
