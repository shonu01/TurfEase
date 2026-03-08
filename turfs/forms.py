from django import forms
from .models import Turf, MaintenanceBlock

# Same time choices as the booking form (6:00 AM – 11:30 PM, 30-min intervals)
TIME_CHOICES = [('', 'Select time')]
for h24 in range(6, 24):
    for minute in ('00', '30'):
        hour12 = h24 % 12 or 12
        period = 'AM' if h24 < 12 else 'PM'
        label = f'{hour12}:{minute} {period}'
        value = f'{h24:02d}:{minute}'
        TIME_CHOICES.append((value, label))


class TurfForm(forms.ModelForm):
    class Meta:
        model = Turf
        fields = ['name', 'location', 'description', 'price_per_hour', 'price_5a_side', 'price_7a_side', 'price_11a_side', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price_per_hour': forms.NumberInput(attrs={'class': 'form-control'}),
            'price_5a_side': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Additional price for 5-a-side'}),
            'price_7a_side': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Additional price for 7-a-side'}),
            'price_11a_side': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Additional price for 11-a-side'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class MaintenanceBlockForm(forms.ModelForm):
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
        model = MaintenanceBlock
        fields = ['turf', 'date', 'start_time', 'end_time', 'reason']
        widgets = {
            'turf': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'reason': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Turf repair, Watering'}),
        }
