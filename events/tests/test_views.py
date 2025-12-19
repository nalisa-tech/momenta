# events/tests/test_views.py

from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from datetime import date, time, timedelta
from decimal import Decimal
from events.models import Category, Event, Booking, PaymentTransaction


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class HomeViewTest(TestCase):
    """Test home page functionality"""
    
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Music")
        self.event = Event.objects.create(
            title="Test Event",
            description="Test Description",
            date=date.today() + timedelta(days=30),
            category=self.category,
            vip_seats_left=50,
            gold_seats_left=100,
            standard_seats_left=200
        )
    
    def test_home_page_loads(self):
        """Test home page loads successfully"""
        response = self.client.get(reverse('events:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Zambia's #1 Event Platform")
        self.assertContains(response, "Explore Events")
    
    def test_home_page_has_hero_content(self):
        """Test home page displays hero content"""
        response = self.client.get(reverse('events:home'))
        self.assertContains(response, "Concerts • Tech • Food • Conferences")
        self.assertContains(response, "ZMW")


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class EventDetailViewTest(TestCase):
    """Test event detail page functionality"""
    
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Music")
        self.event = Event.objects.create(
            title="Zambian Music Festival",
            description="Amazing music festival",
            date=date.today() + timedelta(days=30),
            time=time(19, 0),
            location="Heroes Stadium",
            category=self.category,
            vip_seats_left=50,
            gold_seats_left=100,
            standard_seats_left=200,
            organizer_name="Music Zambia",
            organizer_phone="+260977123456"
        )
    
    def test_event_detail_page_loads(self):
        """Test event detail page loads successfully"""
        response = self.client.get(
            reverse('events:event_detail', kwargs={'event_id': self.event.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.event.title)
        self.assertContains(response, self.event.description)
        self.assertContains(response, self.event.location)
    
    def test_event_detail_shows_ticket_info(self):
        """Test event detail shows ticket information"""
        response = self.client.get(
            reverse('events:event_detail', kwargs={'event_id': self.event.id})
        )
        
        # Check ticket types and prices are displayed
        self.assertContains(response, "VIP Front Row")
        self.assertContains(response, "K1,500")
        self.assertContains(response, "Gold Section")
        self.assertContains(response, "K850")
        self.assertContains(response, "Standard")
        self.assertContains(response, "K450")
    
    def test_event_detail_shows_organizer_info(self):
        """Test event detail shows organizer information"""
        response = self.client.get(
            reverse('events:event_detail', kwargs={'event_id': self.event.id})
        )
        self.assertContains(response, self.event.organizer_name)
        self.assertContains(response, self.event.organizer_phone)
    
    def test_event_not_found(self):
        """Test 404 for non-existent event"""
        response = self.client.get(
            reverse('events:event_detail', kwargs={'event_id': 99999})
        )
        self.assertEqual(response.status_code, 404)


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class AuthenticationViewsTest(TestCase):
    """Test user authentication views"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_login_page_loads(self):
        """Test login page loads successfully"""
        response = self.client.get(reverse('events:login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sign in")
    
    def test_register_page_loads(self):
        """Test registration page loads successfully"""
        response = self.client.get(reverse('events:register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create Account")
    
    def test_user_login_success(self):
        """Test successful user login"""
        response = self.client.post(reverse('events:login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after login
        
        # Check user is logged in
        user = response.wsgi_request.user
        self.assertTrue(user.is_authenticated)
    
    def test_user_login_failure(self):
        """Test failed user login"""
        response = self.client.post(reverse('events:login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        
        # Should stay on login page with error
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('Invalid username or password' in str(m) for m in messages))
    
    def test_user_registration_success(self):
        """Test successful user registration"""
        response = self.client.post(reverse('events:register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'phone_number': '0977123456',
            'password1': 'newpass123',
            'password2': 'newpass123'
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect after registration
        
        # Check user was created
        self.assertTrue(User.objects.filter(username='newuser').exists())
        
        # Check profile was created with phone number
        new_user = User.objects.get(username='newuser')
        self.assertEqual(new_user.profile.phone_number, '0977123456')
    
    def test_user_registration_password_mismatch(self):
        """Test registration with mismatched passwords"""
        response = self.client.post(reverse('events:register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpass123',
            'password2': 'differentpass'
        })
        
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('Passwords do not match' in str(m) for m in messages))
    
    def test_user_logout(self):
        """Test user logout"""
        # Login first
        self.client.login(username='testuser', password='testpass123')
        
        # Then logout
        response = self.client.get(reverse('events:logout'))
        self.assertEqual(response.status_code, 302)  # Redirect after logout


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class SeatSelectionViewTest(TestCase):
    """Test seat selection functionality"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(name="Music")
        self.event = Event.objects.create(
            title="Test Event",
            description="Test Description",
            date=date.today() + timedelta(days=30),
            category=self.category,
            vip_seats_left=50,
            gold_seats_left=100,
            standard_seats_left=200
        )
    
    def test_seat_selection_requires_login(self):
        """Test seat selection redirects to login if not authenticated"""
        response = self.client.get(
            reverse('events:select_seat', kwargs={'event_id': self.event.id})
        )
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_seat_selection_page_loads_for_authenticated_user(self):
        """Test seat selection page loads for logged-in user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('events:select_seat', kwargs={'event_id': self.event.id})
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Select Your Tickets")
        self.assertContains(response, self.event.title)
    
    def test_seat_selection_shows_available_tickets(self):
        """Test seat selection shows available ticket types"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('events:select_seat', kwargs={'event_id': self.event.id})
        )
        
        # Check all ticket types are shown
        self.assertContains(response, "VIP Front Row")
        self.assertContains(response, "Gold Section")
        self.assertContains(response, "Standard")
        
        # Check seat availability is shown
        self.assertContains(response, "50 seats available")  # VIP
        self.assertContains(response, "100 seats available")  # Gold
        self.assertContains(response, "200 seats available")  # Standard


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class PaymentPageViewTest(TestCase):
    """Test payment page functionality"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(name="Music")
        self.event = Event.objects.create(
            title="Test Event",
            description="Test Description",
            date=date.today() + timedelta(days=30),
            category=self.category,
            vip_seats_left=50,
            gold_seats_left=100,
            standard_seats_left=200
        )
    
    def test_payment_page_requires_login(self):
        """Test payment page redirects to login if not authenticated"""
        response = self.client.post(
            reverse('events:payment_page', kwargs={'event_id': self.event.id})
        )
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_payment_page_with_valid_ticket_selection(self):
        """Test payment page with valid ticket selection"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(
            reverse('events:payment_page', kwargs={'event_id': self.event.id}),
            {
                'ticket_type': 'vip',
                'tickets': '2'
            }
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Secure Payment")
        self.assertContains(response, "K3000")  # 2 × K1,500
    
    def test_payment_page_shows_payment_methods(self):
        """Test payment page shows all payment methods"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(
            reverse('events:payment_page', kwargs={'event_id': self.event.id}),
            {
                'ticket_type': 'standard',
                'tickets': '1'
            }
        )
        
        # Check all payment methods are available
        self.assertContains(response, "MTN Mobile Money")
        self.assertContains(response, "Airtel Money")
        self.assertContains(response, "Zamtel Money")
        self.assertContains(response, "Bank Transfer")
    
    def test_payment_page_invalid_ticket_type(self):
        """Test payment page with invalid ticket type"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(
            reverse('events:payment_page', kwargs={'event_id': self.event.id}),
            {
                'ticket_type': 'invalid',
                'tickets': '1'
            }
        )
        
        # Should redirect back to seat selection with error
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('Invalid ticket type' in str(m) for m in messages))
    
    def test_payment_completion_creates_booking_and_payment(self):
        """Test payment completion creates booking and payment records"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(
            reverse('events:payment_page', kwargs={'event_id': self.event.id}),
            {
                'ticket_type': 'vip',
                'tickets': '2',
                'payment_method': 'mtn',
                'phone_number': '0977123456'
            }
        )
        
        # Check booking was created
        booking = Booking.objects.filter(user=self.user, event=self.event).first()
        self.assertIsNotNone(booking)
        self.assertEqual(booking.ticket_type, 'vip')
        self.assertEqual(booking.tickets, 2)
        self.assertEqual(booking.total_price, Decimal('3000.00'))
        
        # Check payment transaction was created
        payment = PaymentTransaction.objects.filter(booking=booking).first()
        self.assertIsNotNone(payment)
        self.assertEqual(payment.payment_method, 'mtn')
        self.assertEqual(payment.amount, Decimal('3000.00'))
        self.assertEqual(payment.status, 'pending')
        self.assertEqual(payment.phone_number, '0977123456')


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class UserProfileViewTest(TestCase):
    """Test user profile functionality"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(name="Music")
        self.event = Event.objects.create(
            title="Test Event",
            description="Test Description",
            date=date.today() + timedelta(days=30),
            category=self.category
        )
        self.booking = Booking.objects.create(
            user=self.user,
            event=self.event,
            ticket_type='vip',
            tickets=2
        )
    
    def test_profile_requires_login(self):
        """Test profile page redirects to login if not authenticated"""
        response = self.client.get(reverse('events:profile'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_profile_page_loads_for_authenticated_user(self):
        """Test profile page loads for logged-in user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('events:profile'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)
    
    def test_profile_shows_user_bookings(self):
        """Test profile page shows user's bookings"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('events:profile'))
        
        self.assertContains(response, self.event.title)
        self.assertContains(response, "VIP")
        self.assertContains(response, "2")  # Number of tickets


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class CategoriesViewTest(TestCase):
    """Test categories page functionality"""
    
    def setUp(self):
        self.client = Client()
        self.category1 = Category.objects.create(name="Music & Concerts")
        self.category2 = Category.objects.create(name="Tech & Innovation")
        
        self.event1 = Event.objects.create(
            title="Music Event",
            description="Music Description",
            date=date.today() + timedelta(days=30),
            category=self.category1
        )
        self.event2 = Event.objects.create(
            title="Tech Event",
            description="Tech Description",
            date=date.today() + timedelta(days=30),
            category=self.category2
        )
    
    def test_categories_page_loads(self):
        """Test categories page loads successfully"""
        response = self.client.get(reverse('events:categories_with_events'))
        self.assertEqual(response.status_code, 200)
    
    def test_categories_page_shows_categories_and_events(self):
        """Test categories page shows categories with their events"""
        response = self.client.get(reverse('events:categories_with_events'))
        
        # Check categories are shown (HTML encoded)
        self.assertContains(response, "Music &amp; Concerts")
        self.assertContains(response, "Tech &amp; Innovation")
        
        # Check events are shown under their categories
        self.assertContains(response, "Music Event")
        self.assertContains(response, "Tech Event")


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class AdminPaymentActionsTest(TestCase):
    """Test admin payment approval/rejection functionality"""
    
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass123',
            is_staff=True
        )
        self.regular_user = User.objects.create_user(
            username='user',
            email='user@example.com',
            password='userpass123'
        )
        
        self.category = Category.objects.create(name="Music")
        self.event = Event.objects.create(
            title="Test Event",
            description="Test Description",
            date=date.today() + timedelta(days=30),
            category=self.category,
            vip_seats_left=50
        )
        
        self.booking = Booking.objects.create(
            user=self.regular_user,
            event=self.event,
            ticket_type='vip',
            tickets=2
        )
        
        self.payment = PaymentTransaction.objects.create(
            booking=self.booking,
            payment_method='mtn',
            amount=Decimal('3000.00'),
            status='pending'
        )
    
    def test_approve_payment_requires_staff(self):
        """Test payment approval requires staff privileges"""
        self.client.login(username='user', password='userpass123')
        
        response = self.client.post(
            reverse('events:approve_payment', kwargs={'payment_id': self.payment.id})
        )
        
        # Should redirect to login or show permission denied
        self.assertIn(response.status_code, [302, 403])
    
    def test_approve_payment_success(self):
        """Test successful payment approval by admin"""
        self.client.login(username='admin', password='adminpass123')
        
        response = self.client.post(
            reverse('events:approve_payment', kwargs={'payment_id': self.payment.id})
        )
        
        self.assertEqual(response.status_code, 200)
        
        # Check payment status was updated
        self.payment.refresh_from_db()
        self.assertEqual(self.payment.status, 'completed')
        
        # Check seat count was reduced
        self.event.refresh_from_db()
        self.assertEqual(self.event.vip_seats_left, 48)  # 50 - 2 tickets
    
    def test_reject_payment_success(self):
        """Test successful payment rejection by admin"""
        self.client.login(username='admin', password='adminpass123')
        
        response = self.client.post(
            reverse('events:reject_payment', kwargs={'payment_id': self.payment.id})
        )
        
        self.assertEqual(response.status_code, 200)
        
        # Check payment status was updated
        self.payment.refresh_from_db()
        self.assertEqual(self.payment.status, 'failed')
        
        # Check seat count was NOT reduced
        self.event.refresh_from_db()
        self.assertEqual(self.event.vip_seats_left, 50)  # Unchanged