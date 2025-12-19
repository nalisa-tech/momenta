# events/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal


# ============================
# USER PROFILE MODEL
# ============================
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True, null=True, help_text="User's phone number")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"


# Auto-create profile when user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()


# ============================
# CATEGORY MODEL
# ============================
class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


# ============================
# EVENT MODEL
# ============================
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=200)
    
    # Multiple images for different purposes
    main_image = models.ImageField(upload_to="event_images/main/", null=True, blank=True, 
                                  help_text="Main event poster/banner image")
    crowd_image = models.ImageField(upload_to="event_images/crowd/", null=True, blank=True,
                                   help_text="Amazing crowd - Join hundreds of attendees")
    experience_image = models.ImageField(upload_to="event_images/experience/", null=True, blank=True,
                                        help_text="Premium experience showcase")
    performance_image = models.ImageField(upload_to="event_images/performance/", null=True, blank=True,
                                         help_text="Live performances and entertainment")
    
    # Keep old image field for backward compatibility
    image = models.ImageField(upload_to="event_images/", null=True, blank=True,
                             help_text="Legacy image field (use main_image instead)")

    # Correct ForeignKey with related_name
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='events'
    )

    # Ticket seats
    vip_seats_left = models.IntegerField(default=0, blank=True, null=True)
    gold_seats_left = models.IntegerField(default=0, blank=True, null=True)
    standard_seats_left = models.IntegerField(default=0, blank=True, null=True)

    # Organizer info
    organizer_name = models.CharField(max_length=100, default="TechZambia Team")
    organizer_phone = models.CharField(max_length=20, default="+260 977 123 456")

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title

    @property
    def total_seats_left(self):
        return (self.vip_seats_left or 0) + (self.gold_seats_left or 0) + (self.standard_seats_left or 0)
    
    @property
    def vip_available(self):
        return self.vip_seats_left or 0
    
    @property
    def gold_available(self):
        return self.gold_seats_left or 0
    
    @property
    def standard_available(self):
        return self.standard_seats_left or 0
    
    @property
    def primary_image(self):
        """Get the primary image for display (main_image or fallback to image)"""
        return self.main_image or self.image
    
    @property
    def has_all_images(self):
        """Check if event has all required images"""
        return all([self.main_image, self.crowd_image, self.experience_image, self.performance_image])
    
    @property
    def image_count(self):
        """Count how many images are uploaded"""
        images = [self.main_image, self.crowd_image, self.experience_image, self.performance_image]
        return sum(1 for img in images if img)


# ============================
# BOOKING MODEL
# ============================
class Booking(models.Model):
    TICKET_CHOICES = [
        ('vip', 'VIP - K1,500'),
        ('gold', 'Gold - K850'),
        ('standard', 'Standard - K450'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')
    ticket_type = models.CharField(max_length=10, choices=TICKET_CHOICES, default='standard')
    tickets = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    booked_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Auto-calculate price
        prices = {'vip': 1500, 'gold': 850, 'standard': 450}
        self.total_price = self.tickets * prices[self.ticket_type]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.event.title} ({self.tickets} × {self.get_ticket_type_display()})"


# ============================
# EVENT GALLERY MODEL
# ============================
class EventGallery(models.Model):
    event = models.ForeignKey(Event, related_name="gallery_items", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="event_gallery/images/", 
                             help_text="Gallery image from previous events")
    caption = models.CharField(max_length=200, blank=True, help_text="Optional caption for the image")
    order = models.IntegerField(default=0, help_text="Display order (lower numbers first)")
    
    class Meta:
        verbose_name_plural = "Event Gallery"
        ordering = ['order', 'id']
    
    def __str__(self):
        return f"{self.event.title} - Image {self.id}"

# ============================
# PAYMENT TRANSACTION MODEL
# ============================
class PaymentTransaction(models.Model):
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    PAYMENT_METHODS = [
        ('mtn', 'MTN Mobile Money'),
        ('airtel', 'Airtel Money'),
        ('zamtel', 'Zamtel Money'),
        ('bank', 'Bank Transfer'),
    ]
    
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    transaction_id = models.CharField(max_length=100, unique=True, editable=False)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    payment_proof = models.ImageField(upload_to="payment_proofs/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, help_text="Admin notes or error messages")
    
    class Meta:
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.transaction_id:
            import random
            import string
            prefix = self.payment_method.upper()[:3]
            random_str = ''.join(random.choices(string.digits, k=10))
            self.transaction_id = f"{prefix}{random_str}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.transaction_id} - {self.get_payment_method_display()} - {self.status}"

# ============================
# VENUE MODEL
# ============================
class Venue(models.Model):
    name = models.CharField(max_length=200, help_text="Venue name (e.g., Heroes Stadium)")
    address = models.TextField(help_text="Full address of the venue")
    capacity = models.IntegerField(help_text="Maximum capacity")
    contact_person = models.CharField(max_length=100, blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_email = models.EmailField(blank=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, help_text="Cost per hour in Kwacha")
    facilities = models.TextField(blank=True, help_text="Available facilities (parking, sound system, etc.)")
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} (Capacity: {self.capacity})"
    
    class Meta:
        ordering = ['name']

# ============================
# RESOURCE MODEL
# ============================
class Resource(models.Model):
    RESOURCE_TYPES = [
        ('sound', 'Sound System'),
        ('lighting', 'Lighting Equipment'),
        ('stage', 'Stage/Platform'),
        ('seating', 'Additional Seating'),
        ('security', 'Security Personnel'),
        ('catering', 'Catering Equipment'),
        ('transport', 'Transportation'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=200, help_text="Resource name")
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    description = models.TextField(blank=True)
    cost_per_day = models.DecimalField(max_digits=10, decimal_places=2, help_text="Cost per day in Kwacha")
    quantity_available = models.IntegerField(default=1, help_text="How many units available")
    supplier_name = models.CharField(max_length=100, blank=True)
    supplier_phone = models.CharField(max_length=20, blank=True)
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_resource_type_display()})"
    
    class Meta:
        ordering = ['resource_type', 'name']
# ============================
# VENUE BOOKING MODEL
# ============================
class VenueBooking(models.Model):
    BOOKING_STATUS = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    event = models.OneToOneField(Event, on_delete=models.CASCADE, related_name='venue_booking')
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='bookings')
    start_datetime = models.DateTimeField(help_text="Event start date and time")
    end_datetime = models.DateTimeField(help_text="Event end date and time")
    setup_hours = models.IntegerField(default=2, help_text="Hours needed for setup before event")
    cleanup_hours = models.IntegerField(default=1, help_text="Hours needed for cleanup after event")
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    status = models.CharField(max_length=20, choices=BOOKING_STATUS, default='pending')
    notes = models.TextField(blank=True, help_text="Special requirements or notes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Calculate total cost based on duration and venue hourly rate
        if self.start_datetime and self.end_datetime and self.venue:
            duration_hours = (self.end_datetime - self.start_datetime).total_seconds() / 3600
            total_hours = duration_hours + self.setup_hours + self.cleanup_hours
            self.total_cost = Decimal(str(total_hours)) * self.venue.hourly_rate
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.venue.name} - {self.event.title}"
    
    class Meta:
        ordering = ['-start_datetime']
# ============================
# RESOURCE ALLOCATION MODEL
# ============================
class ResourceAllocation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='resource_allocations')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='allocations')
    quantity_needed = models.IntegerField(default=1, help_text="How many units needed")
    start_date = models.DateField(help_text="When resource is needed from")
    end_date = models.DateField(help_text="When resource is needed until")
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    status = models.CharField(max_length=20, choices=[
        ('requested', 'Requested'),
        ('confirmed', 'Confirmed'),
        ('delivered', 'Delivered'),
        ('returned', 'Returned'),
        ('cancelled', 'Cancelled'),
    ], default='requested')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # Calculate total cost based on duration and resource daily rate
        if self.start_date and self.end_date and self.resource:
            duration_days = (self.end_date - self.start_date).days + 1
            self.total_cost = duration_days * self.resource.cost_per_day * self.quantity_needed
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.resource.name} for {self.event.title}"
    
    class Meta:
        ordering = ['-created_at']