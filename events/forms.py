from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from .models import Booking


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(
        max_length=20,
        required=False,
        validators=[
            RegexValidator(
                regex=r'^[0-9]{10}$',
                message='Phone number must be 10 digits'
            )
        ]
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition'
            })


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['ticket_type', 'tickets']
        widgets = {
            'ticket_type': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-blue-500'
            }),
            'tickets': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-blue-500',
                'min': '1',
                'max': '10'
            })
        }
    
    def clean_tickets(self):
        tickets = self.cleaned_data.get('tickets')
        if tickets < 1:
            raise forms.ValidationError("Number of tickets must be at least 1")
        if tickets > 10:
            raise forms.ValidationError("Maximum 10 tickets per booking")
        return tickets


class PaymentForm(forms.Form):
    PAYMENT_METHODS = [
        ('mtn', 'MTN Mobile Money'),
        ('airtel', 'Airtel Money'),
        ('zamtel', 'Zamtel Money'),
        ('bank', 'Bank Transfer'),
    ]
    
    payment_method = forms.ChoiceField(
        choices=PAYMENT_METHODS,
        required=True,
        widget=forms.RadioSelect(attrs={
            'class': 'payment-method-radio'
        })
    )
    
    phone_number = forms.CharField(
        max_length=20,
        required=False,
        validators=[
            RegexValidator(
                regex=r'^[0-9]{10}$',
                message='Phone number must be 10 digits (e.g., 0977123456)'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-blue-500',
            'placeholder': '0977123456'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        payment_method = cleaned_data.get('payment_method')
        phone_number = cleaned_data.get('phone_number')
        
        # Phone number is required for mobile money payments
        if payment_method in ['mtn', 'airtel', 'zamtel'] and not phone_number:
            raise forms.ValidationError('Phone number is required for mobile money payments')
        
        return cleaned_data
