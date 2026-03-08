from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


def validate_gmail(email):
    """Ensure email is a valid Gmail address."""
    if not email.endswith('@gmail.com'):
        raise ValidationError('Only Gmail addresses (@gmail.com) are allowed.')


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, validators=[validate_gmail])

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email', '').lower().strip()
        if User.objects.filter(email=email).exists():
            raise ValidationError('An account with this email already exists.')
        return email


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email', '').lower().strip()
        validate_gmail(email)
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError('An account with this email already exists.')
        return email
