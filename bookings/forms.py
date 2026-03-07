from django import forms
from .models import Booking

TIME_CHOICES = []
for hour in range(1, 13):
    for minute in ('00', '30'):
        for period in ('AM', 'PM'):
            label = f'{hour}:{minute} {period}'
            # Convert to 24-hour value for the option value
            h24 = hour % 12
            if period == 'PM':
                h24 += 12
            value = f'{h24:02d}:{minute}'
            TIME_CHOICES.append((value, label))


class BookingForm(forms.ModelForm):
    start_time = forms.TimeField(
        widget=forms.Select(attrs={'class': 'form-control'}, choices=TIME_CHOICES),
    )
    end_time = forms.TimeField(
        widget=forms.Select(attrs={'class': 'form-control'}, choices=TIME_CHOICES),
    )

    class Meta:
        model = Booking
        fields = ['booking_date', 'start_time', 'end_time', 'members']
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'members': forms.Select(attrs={'class': 'form-control'}),
        }
