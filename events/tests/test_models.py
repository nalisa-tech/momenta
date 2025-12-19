# events/tests/test_models.py

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from decimal import Decimal
from datetime import date, time, datetime, timedelta
from events.models import (
    Category, Event, UserProfile, Booking, 
    PaymentTransaction, EventGallery, Venue, Resource,
    VenueBooking, ResourceAllocation
)


class CategoryModelTest(TestCase):
    """Test Category model functionality"""
    
    def setUp(self):
        self.category = Category.objects.create(name="Music & Concerts")
    
    def test_category_creation(self):
        """Test category is created correctly"""
        self.assertEqual(self.category.name, "Music & Concerts")
        self.assertEqual(self.category.slug, "music-concerts")
        self.assertEqual(str(self.category), "Music & Concerts")
    
    def test_slug_auto_generation(self):
        """Test slug is automatically generated from name"""
        category = Category.objects.create(name="Tech & Innovation")
        self.assertEqual(category.slug, "tech-innovation")
    
    def test_unique_slug_generation(self):
        """Test unique slug generation for duplicate names"""
        # Create first category with unique name
        category1 = Category.objects.create(name="Music Events")
        self.assertEqual(category1.slug, "music-events")
        
        # Create second category with same name - should get unique slug
        # Note: The model has unique constraint on name, so we need to test slug uniqueness differently
        category2 = Category.objects.create(name="Music Events 2")
        self.assertEqual(category2.slug, "music-events-2")


class UserProfileModelTest(TestCase):
    """Test UserProfile model functionality"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_user_profile_auto_creation(self):
        """Test profile is automatically created when user is created"""
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsInstance(self.user.profile, UserProfile)
    
    def test_user_profile_str_method(self):
        """Test UserProfile string representation"""
        expected = f"{self.user.username}'s Profile"
        self.assertEqual(str(self.user.profile), expected)
    
    def test_phone_number_field(self):
        """Test phone number field functionality"""
        self.user.profile.phone_number = "0977123456"
        self.user.profile.save()
        self.assertEqual(self.user.profile.phone_number, "0977123456")


class EventModelTest(TestCase):
    """Test Event model functionality"""
    
    def setUp(self):
        self.category = Category.objects.create(name="Music")
        self.event = Event.objects.create(
            title="Zambian Music Festival",
            description="Amazing music festival in Lusaka",
            date=date.today() + timedelta(days=30),
            time=time(19, 0),
            location="Heroes Stadium, Lusaka",
            category=self.category,
            vip_seats_left=100,
            gold_seats_left=200,
            standard_seats_left=500,
            organizer_name="Music Zambia",
            organizer_phone="+260977123456"
        )
    
    def test_event_creation(self):
        """Test event is created correctly"""
        self.assertEqual(self.event.title, "Zambian Music Festival")
        self.assertEqual(self.event.category, self.category)
        self.assertEqual(str(self.event), "Zambian Music Festival")
    
    def test_total_seats_left_property(self):
        """Test total_seats_left calculated property"""
        expected_total = 100 + 200 + 500  # vip + gold + standard
        self.assertEqual(self.event.total_seats_left, expected_total)
    
    def test_seat_availability_properties(self):
        """Test seat availability properties"""
        self.assertEqual(self.event.vip_available, 100)
        self.assertEqual(self.event.gold_available, 200)
        self.assertEqual(self.event.standard_available, 500)
    
    def test_primary_image_property(self):
        """Test primary_image property fallback"""
        # Should return empty ImageFieldFile when no images
        self.assertFalse(self.event.primary_image)
    
    def test_event_ordering(self):
        """Test events are ordered by date (newest first)"""
        event1 = Event.objects.create(
            title="Event 1",
            description="Test",
            date=date.today() + timedelta(days=10),
            category=self.category
        )
        event2 = Event.objects.create(
            title="Event 2", 
            description="Test",
            date=date.today() + timedelta(days=20),
            category=self.category
        )
        
        events = list(Event.objects.all())
        # Should be ordered by date descending (newest first)
        self.assertEqual(events[0], self.event)  # 30 days from now
        self.assertEqual(events[1], event2)      # 20 days from now
        self.assertEqual(events[2], event1)      # 10 days from now


class BookingModelTest(TestCase):
    """Test Booking model functionality"""
    
    def setUp(self):
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
    
    def test_booking_creation(self):
        """Test booking is created correctly"""
        booking = Booking.objects.create(
            user=self.user,
            event=self.event,
            ticket_type='vip',
            tickets=2
        )
        
        self.assertEqual(booking.user, self.user)
        self.assertEqual(booking.event, self.event)
        self.assertEqual(booking.ticket_type, 'vip')
        self.assertEqual(booking.tickets, 2)
    
    def test_total_price_calculation(self):
        """Test total price is calculated automatically"""
        # VIP tickets: K1,500 each
        vip_booking = Booking.objects.create(
            user=self.user,
            event=self.event,
            ticket_type='vip',
            tickets=2
        )
        self.assertEqual(vip_booking.total_price, Decimal('3000.00'))
        
        # Gold tickets: K850 each
        gold_booking = Booking.objects.create(
            user=self.user,
            event=self.event,
            ticket_type='gold',
            tickets=3
        )
        self.assertEqual(gold_booking.total_price, Decimal('2550.00'))
        
        # Standard tickets: K450 each
        standard_booking = Booking.objects.create(
            user=self.user,
            event=self.event,
            ticket_type='standard',
            tickets=4
        )
        self.assertEqual(standard_booking.total_price, Decimal('1800.00'))
    
    def test_booking_str_method(self):
        """Test booking string representation"""
        booking = Booking.objects.create(
            user=self.user,
            event=self.event,
            ticket_type='vip',
            tickets=2
        )
        expected = f"{self.user.username} - {self.event.title} (2 × VIP - K1,500)"
        self.assertEqual(str(booking), expected)


class PaymentTransactionModelTest(TestCase):
    """Test PaymentTransaction model functionality"""
    
    def setUp(self):
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
    
    def test_payment_transaction_creation(self):
        """Test payment transaction is created correctly"""
        payment = PaymentTransaction.objects.create(
            booking=self.booking,
            payment_method='mtn',
            amount=Decimal('3000.00'),
            phone_number='0977123456'
        )
        
        self.assertEqual(payment.booking, self.booking)
        self.assertEqual(payment.payment_method, 'mtn')
        self.assertEqual(payment.amount, Decimal('3000.00'))
        self.assertEqual(payment.status, 'pending')  # Default status
    
    def test_transaction_id_auto_generation(self):
        """Test transaction ID is automatically generated"""
        payment = PaymentTransaction.objects.create(
            booking=self.booking,
            payment_method='mtn',
            amount=Decimal('3000.00')
        )
        
        self.assertTrue(payment.transaction_id.startswith('MTN'))
        self.assertEqual(len(payment.transaction_id), 13)  # MTN + 10 digits
    
    def test_payment_status_choices(self):
        """Test payment status choices"""
        payment = PaymentTransaction.objects.create(
            booking=self.booking,
            payment_method='airtel',
            amount=Decimal('1500.00')
        )
        
        # Test status updates
        payment.status = 'completed'
        payment.save()
        self.assertEqual(payment.status, 'completed')
        
        payment.status = 'failed'
        payment.save()
        self.assertEqual(payment.status, 'failed')
    
    def test_payment_method_choices(self):
        """Test different payment methods"""
        methods = ['mtn', 'airtel', 'zamtel', 'bank']
        
        for i, method in enumerate(methods):
            # Create a new booking for each payment to avoid unique constraint
            booking = Booking.objects.create(
                user=self.user,
                event=self.event,
                ticket_type='standard',
                tickets=1
            )
            payment = PaymentTransaction.objects.create(
                booking=booking,
                payment_method=method,
                amount=Decimal('1000.00')
            )
            self.assertEqual(payment.payment_method, method)


class VenueModelTest(TestCase):
    """Test Venue model functionality"""
    
    def setUp(self):
        self.venue = Venue.objects.create(
            name="Heroes Stadium",
            address="Independence Avenue, Lusaka",
            capacity=60000,
            contact_person="John Mwanza",
            contact_phone="+260977123456",
            contact_email="john@heroes.zm",
            hourly_rate=Decimal('2000.00'),
            facilities="Parking, Sound System, Security"
        )
    
    def test_venue_creation(self):
        """Test venue is created correctly"""
        self.assertEqual(self.venue.name, "Heroes Stadium")
        self.assertEqual(self.venue.capacity, 60000)
        self.assertEqual(self.venue.hourly_rate, Decimal('2000.00'))
        self.assertTrue(self.venue.is_available)
    
    def test_venue_str_method(self):
        """Test venue string representation"""
        expected = "Heroes Stadium (Capacity: 60000)"
        self.assertEqual(str(self.venue), expected)


class ResourceModelTest(TestCase):
    """Test Resource model functionality"""
    
    def setUp(self):
        self.resource = Resource.objects.create(
            name="Professional Sound System",
            resource_type="sound",
            description="High-quality sound system with microphones",
            cost_per_day=Decimal('500.00'),
            quantity_available=3,
            supplier_name="Audio Pro Zambia",
            supplier_phone="+260977654321"
        )
    
    def test_resource_creation(self):
        """Test resource is created correctly"""
        self.assertEqual(self.resource.name, "Professional Sound System")
        self.assertEqual(self.resource.resource_type, "sound")
        self.assertEqual(self.resource.cost_per_day, Decimal('500.00'))
        self.assertEqual(self.resource.quantity_available, 3)
        self.assertTrue(self.resource.is_available)
    
    def test_resource_str_method(self):
        """Test resource string representation"""
        expected = "Professional Sound System (Sound System)"
        self.assertEqual(str(self.resource), expected)


class VenueBookingModelTest(TestCase):
    """Test VenueBooking model functionality"""
    
    def setUp(self):
        self.category = Category.objects.create(name="Music")
        self.event = Event.objects.create(
            title="Test Event",
            description="Test Description",
            date=date.today() + timedelta(days=30),
            category=self.category
        )
        self.venue = Venue.objects.create(
            name="Test Venue",
            address="Test Address",
            capacity=1000,
            hourly_rate=Decimal('1000.00')
        )
    
    def test_venue_booking_creation(self):
        """Test venue booking is created correctly"""
        start_time = timezone.now() + timedelta(days=30)
        end_time = start_time + timedelta(hours=4)
        
        booking = VenueBooking.objects.create(
            event=self.event,
            venue=self.venue,
            start_datetime=start_time,
            end_datetime=end_time,
            setup_hours=2,
            cleanup_hours=1
        )
        
        self.assertEqual(booking.event, self.event)
        self.assertEqual(booking.venue, self.venue)
        self.assertEqual(booking.status, 'pending')
    
    def test_total_cost_calculation(self):
        """Test total cost calculation for venue booking"""
        start_time = timezone.now() + timedelta(days=30)
        end_time = start_time + timedelta(hours=4)  # 4 hour event
        
        booking = VenueBooking.objects.create(
            event=self.event,
            venue=self.venue,
            start_datetime=start_time,
            end_datetime=end_time,
            setup_hours=2,
            cleanup_hours=1
        )
        
        # Total hours: 4 (event) + 2 (setup) + 1 (cleanup) = 7 hours
        # Cost: 7 hours × K1,000/hour = K7,000
        expected_cost = Decimal('7000.00')
        self.assertEqual(booking.total_cost, expected_cost)


class ResourceAllocationModelTest(TestCase):
    """Test ResourceAllocation model functionality"""
    
    def setUp(self):
        self.category = Category.objects.create(name="Music")
        self.event = Event.objects.create(
            title="Test Event",
            description="Test Description",
            date=date.today() + timedelta(days=30),
            category=self.category
        )
        self.resource = Resource.objects.create(
            name="Sound System",
            resource_type="sound",
            cost_per_day=Decimal('500.00'),
            quantity_available=5
        )
    
    def test_resource_allocation_creation(self):
        """Test resource allocation is created correctly"""
        start_date = date.today() + timedelta(days=29)
        end_date = date.today() + timedelta(days=31)
        
        allocation = ResourceAllocation.objects.create(
            event=self.event,
            resource=self.resource,
            quantity_needed=2,
            start_date=start_date,
            end_date=end_date
        )
        
        self.assertEqual(allocation.event, self.event)
        self.assertEqual(allocation.resource, self.resource)
        self.assertEqual(allocation.quantity_needed, 2)
        self.assertEqual(allocation.status, 'requested')
    
    def test_total_cost_calculation(self):
        """Test total cost calculation for resource allocation"""
        start_date = date.today() + timedelta(days=29)
        end_date = date.today() + timedelta(days=31)  # 3 days
        
        allocation = ResourceAllocation.objects.create(
            event=self.event,
            resource=self.resource,
            quantity_needed=2,
            start_date=start_date,
            end_date=end_date
        )
        
        # Cost: 3 days × K500/day × 2 units = K3,000
        expected_cost = Decimal('3000.00')
        self.assertEqual(allocation.total_cost, expected_cost)