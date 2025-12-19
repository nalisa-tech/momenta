# events/tests/test_forms.py

from django.test import TestCase
from django.contrib.auth.models import User
from events.forms import UserRegistrationForm, BookingForm, PaymentForm


class UserRegistrationFormTest(TestCase):
    """Test user registration form functionality"""
    
    def test_valid_registration_form(self):
        """Test form with valid data"""
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'phone_number': '0977123456',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_password_mismatch(self):
        """Test form with mismatched passwords"""
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'phone_number': '0977123456',
            'password1': 'testpass123',
            'password2': 'differentpass'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
    
    def test_duplicate_username(self):
        """Test form with existing username"""
        # Create existing user
        User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='pass123'
        )
        
        form_data = {
            'username': 'existinguser',
            'email': 'new@example.com',
            'phone_number': '0977123456',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
    
    def test_invalid_email(self):
        """Test form with invalid email"""
        form_data = {
            'username': 'testuser',
            'email': 'invalid-email',
            'phone_number': '0977123456',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    def test_phone_number_validation(self):
        """Test phone number validation"""
        # Valid phone number
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'phone_number': '0977123456',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        # Invalid phone number (too short)
        form_data['phone_number'] = '123'
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())


class BookingFormTest(TestCase):
    """Test booking form functionality"""
    
    def test_valid_booking_form(self):
        """Test form with valid booking data"""
        form_data = {
            'ticket_type': 'vip',
            'tickets': 2
        }
        form = BookingForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_ticket_type(self):
        """Test form with invalid ticket type"""
        form_data = {
            'ticket_type': 'invalid',
            'tickets': 2
        }
        form = BookingForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('ticket_type', form.errors)
    
    def test_invalid_ticket_quantity(self):
        """Test form with invalid ticket quantity"""
        # Zero tickets
        form_data = {
            'ticket_type': 'vip',
            'tickets': 0
        }
        form = BookingForm(data=form_data)
        self.assertFalse(form.is_valid())
        
        # Negative tickets
        form_data['tickets'] = -1
        form = BookingForm(data=form_data)
        self.assertFalse(form.is_valid())
        
        # Too many tickets
        form_data['tickets'] = 11
        form = BookingForm(data=form_data)
        self.assertFalse(form.is_valid())


class PaymentFormTest(TestCase):
    """Test payment form functionality"""
    
    def test_valid_mobile_money_payment(self):
        """Test form with valid mobile money payment"""
        form_data = {
            'payment_method': 'mtn',
            'phone_number': '0977123456'
        }
        form = PaymentForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_valid_bank_transfer_payment(self):
        """Test form with valid bank transfer payment"""
        form_data = {
            'payment_method': 'bank'
        }
        form = PaymentForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_mobile_money_requires_phone(self):
        """Test mobile money payment requires phone number"""
        form_data = {
            'payment_method': 'mtn',
            'phone_number': ''
        }
        form = PaymentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Phone number is required for mobile money payments', form.non_field_errors())
    
    def test_invalid_payment_method(self):
        """Test form with invalid payment method"""
        form_data = {
            'payment_method': 'invalid',
            'phone_number': '0977123456'
        }
        form = PaymentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('payment_method', form.errors)
    
    def test_phone_number_format_validation(self):
        """Test phone number format validation"""
        # Valid formats
        valid_numbers = ['0977123456', '0978123456', '0979123456']
        for number in valid_numbers:
            form_data = {
                'payment_method': 'mtn',
                'phone_number': number
            }
            form = PaymentForm(data=form_data)
            self.assertTrue(form.is_valid(), f"Phone number {number} should be valid")
        
        # Invalid formats
        invalid_numbers = ['123', '12345678901', 'abc123456', '+260977123456']
        for number in invalid_numbers:
            form_data = {
                'payment_method': 'mtn',
                'phone_number': number
            }
            form = PaymentForm(data=form_data)
            self.assertFalse(form.is_valid(), f"Phone number {number} should be invalid")