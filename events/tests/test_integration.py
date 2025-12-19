# events/tests/test_integration.py

from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from datetime import date, time, timedelta
from decimal import Decimal
from events.models import Category, Event, Booking, PaymentTransaction


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class CompleteBookingFlowTest(TestCase):
    """Test the complete booking flow from event selection to payment"""
    
    def setUp(self):
        self.client = Client()
        
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create test event
        self.category = Category.objects.create(name="Music & Concerts")
        self.event = Event.objects.create(
            title="Zambian Music Festival 2025",
            description="The biggest music festival in Zambia",
            date=date.today() + timedelta(days=30),
            time=time(19, 0),
            location="Heroes Stadium, Lusaka",
            category=self.category,
            vip_seats_left=50,
            gold_seats_left=100,
            standard_seats_left=200,
            organizer_name="Music Zambia",
            organizer_phone="+260977123456"
        )
    
    def test_complete_booking_flow_vip_mtn(self):
        """Test complete booking flow: VIP tickets with MTN payment"""
        
        # Step 1: User visits home page
        response = self.client.get(reverse('events:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Zambia's #1 Event Platform")
        
        # Step 2: User clicks on event to view details
        response = self.client.get(
            reverse('events:event_detail', kwargs={'event_id': self.event.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "LOGIN TO BOOK")
        
        # Step 3: User tries to book but needs to login first
        response = self.client.get(
            reverse('events:select_seat', kwargs={'event_id': self.event.id})
        )
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
        # Step 4: User logs in
        login_response = self.client.post(reverse('events:login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(login_response.status_code, 302)  # Redirect after login
        
        # Step 5: User accesses seat selection page
        response = self.client.get(
            reverse('events:select_seat', kwargs={'event_id': self.event.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Select Your Tickets")
        self.assertContains(response, "VIP Front Row")
        self.assertContains(response, "50 seats available")
        
        # Step 6: User selects VIP tickets and proceeds to payment
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
        self.assertContains(response, "MTN Mobile Money")
        
        # Step 7: User completes payment with MTN
        response = self.client.post(
            reverse('events:payment_page', kwargs={'event_id': self.event.id}),
            {
                'ticket_type': 'vip',
                'tickets': '2',
                'payment_method': 'mtn',
                'phone_number': '0977123456'
            }
        )
        
        # Should show payment success page
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Payment submitted successfully")
        
        # Step 8: Verify booking was created
        booking = Booking.objects.filter(user=self.user, event=self.event).first()
        self.assertIsNotNone(booking)
        self.assertEqual(booking.ticket_type, 'vip')
        self.assertEqual(booking.tickets, 2)
        self.assertEqual(booking.total_price, Decimal('3000.00'))
        
        # Step 9: Verify payment transaction was created
        payment = PaymentTransaction.objects.filter(booking=booking).first()
        self.assertIsNotNone(payment)
        self.assertEqual(payment.payment_method, 'mtn')
        self.assertEqual(payment.amount, Decimal('3000.00'))
        self.assertEqual(payment.status, 'pending')
        self.assertEqual(payment.phone_number, '0977123456')
        
        # Step 10: User can view booking in profile
        response = self.client.get(reverse('events:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.event.title)
        self.assertContains(response, "VIP")
        self.assertContains(response, "2")
    
    def test_complete_booking_flow_standard_bank(self):
        """Test complete booking flow: Standard tickets with Bank Transfer"""
        
        # Login user
        self.client.login(username='testuser', password='testpass123')
        
        # Select standard tickets
        response = self.client.post(
            reverse('events:payment_page', kwargs={'event_id': self.event.id}),
            {
                'ticket_type': 'standard',
                'tickets': '4'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "K1800")  # 4 × K450
        
        # Complete payment with bank transfer
        response = self.client.post(
            reverse('events:payment_page', kwargs={'event_id': self.event.id}),
            {
                'ticket_type': 'standard',
                'tickets': '4',
                'payment_method': 'bank'
            }
        )
        
        # Verify booking and payment
        booking = Booking.objects.filter(user=self.user, event=self.event).first()
        self.assertEqual(booking.ticket_type, 'standard')
        self.assertEqual(booking.tickets, 4)
        self.assertEqual(booking.total_price, Decimal('1800.00'))
        
        payment = PaymentTransaction.objects.filter(booking=booking).first()
        self.assertEqual(payment.payment_method, 'bank')
        self.assertEqual(payment.amount, Decimal('1800.00'))
    
    def test_booking_flow_insufficient_seats(self):
        """Test booking flow when insufficient seats available"""
        
        # Login user
        self.client.login(username='testuser', password='testpass123')
        
        # Try to book more VIP tickets than available
        response = self.client.post(
            reverse('events:payment_page', kwargs={'event_id': self.event.id}),
            {
                'ticket_type': 'vip',
                'tickets': '100'  # More than 50 available
            }
        )
        
        # Should redirect back with error message
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('Only 50 VIP seats available' in str(m) for m in messages))
        
        # No booking should be created
        self.assertFalse(Booking.objects.filter(user=self.user, event=self.event).exists())


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class AdminWorkflowTest(TestCase):
    """Test admin workflow for payment approval"""
    
    def setUp(self):
        self.client = Client()
        
        # Create admin user
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass123',
            is_staff=True
        )
        
        # Create regular user
        self.user = User.objects.create_user(
            username='user',
            email='user@example.com',
            password='userpass123'
        )
        
        # Create test event
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
    
    def test_admin_payment_approval_workflow(self):
        """Test complete admin payment approval workflow"""
        
        # Step 1: User makes a booking
        self.client.login(username='user', password='userpass123')
        
        response = self.client.post(
            reverse('events:payment_page', kwargs={'event_id': self.event.id}),
            {
                'ticket_type': 'vip',
                'tickets': '2',
                'payment_method': 'mtn',
                'phone_number': '0977123456'
            }
        )
        
        # Verify booking and payment were created
        booking = Booking.objects.filter(user=self.user, event=self.event).first()
        payment = PaymentTransaction.objects.filter(booking=booking).first()
        self.assertEqual(payment.status, 'pending')
        
        # Verify seats are NOT yet reduced
        self.event.refresh_from_db()
        self.assertEqual(self.event.vip_seats_left, 50)
        
        # Step 2: Admin logs in and approves payment
        self.client.login(username='admin', password='adminpass123')
        
        response = self.client.post(
            reverse('events:approve_payment', kwargs={'payment_id': payment.id})
        )
        self.assertEqual(response.status_code, 200)
        
        # Step 3: Verify payment status updated and seats reduced
        payment.refresh_from_db()
        self.assertEqual(payment.status, 'completed')
        
        self.event.refresh_from_db()
        self.assertEqual(self.event.vip_seats_left, 48)  # 50 - 2 tickets
    
    def test_admin_payment_rejection_workflow(self):
        """Test admin payment rejection workflow"""
        
        # User makes a booking
        self.client.login(username='user', password='userpass123')
        
        response = self.client.post(
            reverse('events:payment_page', kwargs={'event_id': self.event.id}),
            {
                'ticket_type': 'gold',
                'tickets': '3',
                'payment_method': 'mtn',
                'phone_number': '0977123456'
            }
        )
        
        booking = Booking.objects.filter(user=self.user, event=self.event).first()
        payment = PaymentTransaction.objects.filter(booking=booking).first()
        
        # Admin rejects payment
        self.client.login(username='admin', password='adminpass123')
        
        response = self.client.post(
            reverse('events:reject_payment', kwargs={'payment_id': payment.id})
        )
        self.assertEqual(response.status_code, 200)
        
        # Verify payment status updated but seats NOT reduced
        payment.refresh_from_db()
        self.assertEqual(payment.status, 'failed')
        
        self.event.refresh_from_db()
        self.assertEqual(self.event.gold_seats_left, 100)  # Unchanged


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class MultipleUsersBookingTest(TestCase):
    """Test multiple users booking the same event"""
    
    def setUp(self):
        self.client = Client()
        
        # Create multiple users
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='pass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='pass123'
        )
        
        # Create admin
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass123',
            is_staff=True
        )
        
        # Create event with limited seats
        self.category = Category.objects.create(name="Music")
        self.event = Event.objects.create(
            title="Limited Seats Event",
            description="Event with very limited seats",
            date=date.today() + timedelta(days=30),
            category=self.category,
            vip_seats_left=5,  # Only 5 VIP seats
            gold_seats_left=10,
            standard_seats_left=20
        )
    
    def test_concurrent_bookings_seat_management(self):
        """Test seat management with concurrent bookings"""
        
        # User 1 books 3 VIP tickets
        self.client.login(username='user1', password='pass123')
        
        response = self.client.post(
            reverse('events:payment_page', kwargs={'event_id': self.event.id}),
            {
                'ticket_type': 'vip',
                'tickets': '3',
                'payment_method': 'mtn',
                'phone_number': '0977111111'
            }
        )
        
        booking1 = Booking.objects.filter(user=self.user1, event=self.event).first()
        payment1 = PaymentTransaction.objects.filter(booking=booking1).first()
        
        # User 2 books 2 VIP tickets
        self.client.login(username='user2', password='pass123')
        
        response = self.client.post(
            reverse('events:payment_page', kwargs={'event_id': self.event.id}),
            {
                'ticket_type': 'vip',
                'tickets': '2',
                'payment_method': 'airtel',
                'phone_number': '0978222222'
            }
        )
        
        booking2 = Booking.objects.filter(user=self.user2, event=self.event).first()
        payment2 = PaymentTransaction.objects.filter(booking=booking2).first()
        
        # Admin approves both payments
        self.client.login(username='admin', password='adminpass123')
        
        # Approve payment 1
        self.client.post(
            reverse('events:approve_payment', kwargs={'payment_id': payment1.id})
        )
        
        # Approve payment 2
        self.client.post(
            reverse('events:approve_payment', kwargs={'payment_id': payment2.id})
        )
        
        # Verify seat count is correct
        self.event.refresh_from_db()
        self.assertEqual(self.event.vip_seats_left, 0)  # 5 - 3 - 2 = 0
        
        # User 3 tries to book VIP but should fail
        user3 = User.objects.create_user(
            username='user3',
            email='user3@example.com',
            password='pass123'
        )
        
        self.client.login(username='user3', password='pass123')
        
        response = self.client.post(
            reverse('events:payment_page', kwargs={'event_id': self.event.id}),
            {
                'ticket_type': 'vip',
                'tickets': '1'
            }
        )
        
        # Should redirect with error message
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('Only 0 VIP seats available' in str(m) for m in messages))


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class EventCapacityTest(TestCase):
    """Test event capacity and sold out scenarios"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='user',
            email='user@example.com',
            password='pass123'
        )
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass123',
            is_staff=True
        )
        
        self.category = Category.objects.create(name="Music")
        self.event = Event.objects.create(
            title="Small Venue Event",
            description="Event in small venue",
            date=date.today() + timedelta(days=30),
            category=self.category,
            vip_seats_left=1,  # Only 1 seat of each type
            gold_seats_left=1,
            standard_seats_left=1
        )
    
    def test_event_sold_out_display(self):
        """Test event shows as sold out when no seats available"""
        
        # Book all seats
        self.client.login(username='user', password='pass123')
        
        # Book VIP
        self.client.post(
            reverse('events:payment_page', kwargs={'event_id': self.event.id}),
            {
                'ticket_type': 'vip',
                'tickets': '1',
                'payment_method': 'mtn',
                'phone_number': '0977111111'
            }
        )
        
        # Book Gold
        self.client.post(
            reverse('events:payment_page', kwargs={'event_id': self.event.id}),
            {
                'ticket_type': 'gold',
                'tickets': '1',
                'payment_method': 'mtn',
                'phone_number': '0977111111'
            }
        )
        
        # Book Standard
        self.client.post(
            reverse('events:payment_page', kwargs={'event_id': self.event.id}),
            {
                'ticket_type': 'standard',
                'tickets': '1',
                'payment_method': 'mtn',
                'phone_number': '0977111111'
            }
        )
        
        # Approve all payments
        self.client.login(username='admin', password='adminpass123')
        
        payments = PaymentTransaction.objects.filter(
            booking__event=self.event,
            status='pending'
        )
        
        for payment in payments:
            self.client.post(
                reverse('events:approve_payment', kwargs={'payment_id': payment.id})
            )
        
        # Check event detail page shows sold out
        response = self.client.get(
            reverse('events:event_detail', kwargs={'event_id': self.event.id})
        )
        
        # Check that all seat counts are 0
        self.event.refresh_from_db()
        self.assertEqual(self.event.total_seats_left, 0)
        
        # Check seat selection page shows sold out
        self.client.login(username='user', password='pass123')
        response = self.client.get(
            reverse('events:select_seat', kwargs={'event_id': self.event.id})
        )
        
        self.assertContains(response, "Event Sold Out")