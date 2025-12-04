# events/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


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
# EVENT VIDEO MODEL
# ============================
class EventVideo(models.Model):
    event = models.ForeignKey(Event, related_name="videos", on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True)
    url = models.URLField(max_length=500, help_text="YouTube or direct video link")
    is_highlight = models.BooleanField(default=False, help_text="Show as main video on event page")

    def __str__(self):
        return self.title or f"Video for {self.event.title}"


# ============================
# EVENT GALLERY MODEL
# ============================
class EventGallery(models.Model):
    MEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    
    event = models.ForeignKey(Event, related_name="gallery_items", on_delete=models.CASCADE)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES, default='image')
    
    # For images
    image = models.ImageField(upload_to="event_gallery/images/", blank=True, null=True, 
                             help_text="Gallery image from previous events")
    
    # For videos
    video_url = models.URLField(blank=True, null=True, 
                               help_text="YouTube, Vimeo, or direct video URL for live performances")
    video_thumbnail = models.ImageField(upload_to="event_gallery/video_thumbnails/", blank=True, null=True,
                                       help_text="Custom thumbnail for video (optional)")
    
    caption = models.CharField(max_length=200, blank=True, help_text="Optional caption for the media")
    order = models.IntegerField(default=0, help_text="Display order (lower numbers first)")
    is_live_performance = models.BooleanField(default=False, 
                                            help_text="Mark as live performance video (for music events)")
    
    class Meta:
        verbose_name_plural = "Event Gallery"
        ordering = ['order', 'id']
    
    def __str__(self):
        media_type = "Video" if self.media_type == 'video' else "Image"
        return f"{self.event.title} - {media_type} {self.id}"
    
    @property
    def is_youtube(self):
        """Check if video is from YouTube"""
        if self.video_url:
            return 'youtube.com' in self.video_url or 'youtu.be' in self.video_url
        return False
    
    @property
    def youtube_embed_url(self):
        """Convert YouTube URL to embed format"""
        if not self.is_youtube:
            return None
            
        url = self.video_url
        if 'youtube.com/watch?v=' in url:
            video_id = url.split('v=')[1].split('&')[0]
        elif 'youtu.be/' in url:
            video_id = url.split('youtu.be/')[1].split('?')[0]
        else:
            return None
            
        return f"https://www.youtube.com/embed/{video_id}"

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