from django import forms
from .models import Turf, MaintenanceBlock


class TurfForm(forms.ModelForm):
    class Meta:
        model = Turf
        fields = ['name', 'location', 'description', 'price_per_hour', 'price_5a_side', 'price_7a_side', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price_per_hour': forms.NumberInput(attrs={'class': 'form-control'}),
            'price_5a_side': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Additional price for 5-a-side'}),
            'price_7a_side': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Additional price for 7-a-side'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class MaintenanceBlockForm(forms.ModelForm):
    class Meta:
        model = MaintenanceBlock
        fields = ['turf', 'date', 'start_time', 'end_time', 'reason']
        widgets = {
            'turf': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'reason': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Turf repair, Watering'}),
        }
