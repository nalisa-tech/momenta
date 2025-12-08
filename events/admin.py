# events/admin.py

from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum, Count
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils import timezone
from .models import Category, Event, Booking, EventGallery, PaymentTransaction, UserProfile


# ============================
# CATEGORY ADMIN
# ============================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name_with_icon", "slug", "event_count_badge", "view_events_link")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    list_per_page = 20

    def name_with_icon(self, obj):
        icons = {
            'music': '🎵',
            'tech': '💻',
            'food': '🍽️',
            'sports': '⚽',
        }
        icon = icons.get(obj.slug, '📁')
        return format_html('<strong>{} {}</strong>', icon, obj.name)
    name_with_icon.short_description = "Category"

    def event_count_badge(self, obj):
        count = obj.events.count()
        color = '#28a745' if count > 0 else '#6c757d'
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 12px; font-weight: bold;">{}</span>',
            color, count
        )
    event_count_badge.short_description = "Events"
    
    def view_events_link(self, obj):
        url = f"/admin/events/event/?category__id__exact={obj.id}"
        return format_html('<a href="{}" style="color: #007bff;">View Events →</a>', url)
    view_events_link.short_description = "Actions"


# ============================
# EVENT ADMIN
# ============================
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("event_title_with_image", "category_badge", "date_formatted", "location_short", "image_status", "seats_status", "booking_count", "revenue")
    list_filter = ("category", "date")
    search_fields = ("title", "location", "description")
    date_hierarchy = "date"
    readonly_fields = ("total_seats_left", "image_preview", "booking_stats", 
                      "main_image_preview", "crowd_image_preview", 
                      "experience_image_preview", "performance_image_preview", 
                      "image_upload_status")
    list_per_page = 25
    
    fieldsets = (
        ("Event Information", {
            "fields": ("title", "description", "category")
        }),
        ("Event Images", {
            "fields": ("main_image", "main_image_preview", 
                      "crowd_image", "crowd_image_preview",
                      "experience_image", "experience_image_preview", 
                      "performance_image", "performance_image_preview",
                      "image_upload_status"),
            "description": "Upload different images for various sections of your event page"
        }),
        ("Date & Location", {
            "fields": ("date", "time", "location")
        }),
        ("Ticket Availability", {
            "fields": ("vip_seats_left", "gold_seats_left", "standard_seats_left", "total_seats_left")
        }),
        ("Organizer Details", {
            "fields": ("organizer_name", "organizer_phone"),
            "classes": ("collapse",)
        }),
        ("Legacy", {
            "fields": ("image", "image_preview"),
            "classes": ("collapse",),
            "description": "Old image field - use Event Images section above instead"
        }),
        ("Statistics", {
            "fields": ("booking_stats",),
            "classes": ("collapse",)
        }),
    )

    def event_title_with_image(self, obj):
        primary_img = obj.primary_image
        if primary_img:
            return format_html(
                '<div style="display: flex; align-items: center; gap: 10px;">'
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 8px;">'
                '<strong>{}</strong></div>',
                primary_img.url, obj.title
            )
        return format_html('<strong>{}</strong>', obj.title)
    event_title_with_image.short_description = "Event"

    def image_status(self, obj):
        count = obj.image_count
        if count == 4:
            return format_html('<span style="color: #28a745; font-weight: bold;">✅ Complete (4/4)</span>')
        elif count >= 2:
            return format_html('<span style="color: #ffc107; font-weight: bold;">⚠️ Partial ({}/4)</span>', count)
        elif count == 1:
            return format_html('<span style="color: #fd7e14; font-weight: bold;">📷 Basic (1/4)</span>')
        else:
            return format_html('<span style="color: #dc3545; font-weight: bold;">❌ No Images</span>')
    image_status.short_description = "Images"

    def category_badge(self, obj):
        colors = {
            'music': '#e91e63',
            'tech': '#2196f3',
            'food': '#ff9800',
            'sports': '#9c27b0',
        }
        color = colors.get(obj.category.slug, '#607d8b')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 12px; border-radius: 15px; font-size: 11px; font-weight: bold;">{}</span>',
            color, obj.category.name
        )
    category_badge.short_description = "Category"

    def date_formatted(self, obj):
        return format_html(
            '<div style="text-align: center;"><strong style="font-size: 16px;">{}</strong><br><span style="color: #666; font-size: 11px;">{}</span></div>',
            obj.date.strftime('%b %d'), obj.date.strftime('%Y')
        )
    date_formatted.short_description = "Date"

    def location_short(self, obj):
        location = obj.location[:30] + '...' if len(obj.location) > 30 else obj.location
        return format_html('<span title="{}">{}</span>', obj.location, location)
    location_short.short_description = "Location"

    def seats_status(self, obj):
        total = obj.total_seats_left
        if total == 0:
            return format_html('<span style="color: #dc3545; font-weight: bold;">❌ SOLD OUT</span>')
        elif total < 50:
            return format_html('<span style="color: #ffc107; font-weight: bold;">⚠️ {} left</span>', total)
        else:
            return format_html('<span style="color: #28a745; font-weight: bold;">✅ {} available</span>', total)
    seats_status.short_description = "Availability"

    def booking_count(self, obj):
        count = obj.bookings.count()
        return format_html(
            '<span style="background-color: #17a2b8; color: white; padding: 3px 10px; border-radius: 12px; font-weight: bold;">{}</span>',
            count
        )
    booking_count.short_description = "Bookings"

    def revenue(self, obj):
        total = obj.bookings.aggregate(total=Sum('total_price'))['total']
        if total is None:
            total = 0
        else:
            total = float(total)
        formatted_amount = f"K{total:,.0f}"
        return format_html('<strong style="color: #28a745;">{}</strong>', formatted_amount)
    revenue.short_description = "Revenue"

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 300px; border-radius: 10px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = "Legacy Image"

    def main_image_preview(self, obj):
        if obj.main_image:
            return format_html('<img src="{}" style="max-width: 200px; border-radius: 8px; border: 2px solid #007bff;" />', obj.main_image.url)
        return format_html('<span style="color: #dc3545;">❌ No main image</span>')
    main_image_preview.short_description = "Main Event Image"

    def crowd_image_preview(self, obj):
        if obj.crowd_image:
            return format_html('<img src="{}" style="max-width: 200px; border-radius: 8px; border: 2px solid #28a745;" />', obj.crowd_image.url)
        return format_html('<span style="color: #dc3545;">❌ No crowd image</span>')
    crowd_image_preview.short_description = "Amazing Crowd Image"

    def experience_image_preview(self, obj):
        if obj.experience_image:
            return format_html('<img src="{}" style="max-width: 200px; border-radius: 8px; border: 2px solid #ffc107;" />', obj.experience_image.url)
        return format_html('<span style="color: #dc3545;">❌ No experience image</span>')
    experience_image_preview.short_description = "Premium Experience Image"

    def performance_image_preview(self, obj):
        if obj.performance_image:
            return format_html('<img src="{}" style="max-width: 200px; border-radius: 8px; border: 2px solid #e91e63;" />', obj.performance_image.url)
        return format_html('<span style="color: #dc3545;">❌ No performance image</span>')
    performance_image_preview.short_description = "Live Performances Image"

    def image_upload_status(self, obj):
        status_html = '<div style="background: #f8f9fa; padding: 15px; border-radius: 8px;">'
        status_html += '<h4 style="margin-top: 0;">Image Upload Status</h4>'
        
        images = [
            ('Main Image', obj.main_image, '🎯'),
            ('Crowd Image', obj.crowd_image, '👥'),
            ('Experience Image', obj.experience_image, '⭐'),
            ('Performance Image', obj.performance_image, '🎤')
        ]
        
        for name, image, icon in images:
            if image:
                status_html += f'<p style="color: #28a745;">{icon} <strong>{name}:</strong> ✅ Uploaded</p>'
            else:
                status_html += f'<p style="color: #dc3545;">{icon} <strong>{name}:</strong> ❌ Missing</p>'
        
        progress = obj.image_count
        status_html += f'<hr><p><strong>Progress:</strong> {progress}/4 images uploaded ({progress*25}%)</p>'
        
        if obj.has_all_images:
            status_html += '<p style="color: #28a745; font-weight: bold;">🎉 All images uploaded!</p>'
        else:
            status_html += '<p style="color: #ffc107; font-weight: bold;">⚠️ Upload missing images for best user experience</p>'
        
        status_html += '</div>'
        return format_html(status_html)
    image_upload_status.short_description = "Upload Progress"

    def booking_stats(self, obj):
        bookings = obj.bookings.all()
        vip_count = bookings.filter(ticket_type='vip').count()
        gold_count = bookings.filter(ticket_type='gold').count()
        standard_count = bookings.filter(ticket_type='standard').count()
        total_revenue = bookings.aggregate(total=Sum('total_price'))['total']
        if total_revenue is None:
            total_revenue = 0
        else:
            total_revenue = float(total_revenue)
        
        formatted_revenue = f"K{total_revenue:,.0f}"
        return format_html(
            '<div style="background: #f8f9fa; padding: 15px; border-radius: 8px;">'
            '<h3 style="margin-top: 0;">Booking Statistics</h3>'
            '<p><strong>VIP Tickets:</strong> {}</p>'
            '<p><strong>Gold Tickets:</strong> {}</p>'
            '<p><strong>Standard Tickets:</strong> {}</p>'
            '<p><strong>Total Bookings:</strong> {}</p>'
            '<p><strong>Total Revenue:</strong> {}</p>'
            '</div>',
            vip_count, gold_count, standard_count, bookings.count(), formatted_revenue
        )
    booking_stats.short_description = "Statistics"


# ============================
# BOOKING ADMIN
# ============================
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("booking_id", "user_info", "event_link", "ticket_badge", "tickets_count", "price_display", "payment_status_badge", "date_booked")
    list_filter = ("ticket_type", "booked_at", "event__category")
    search_fields = ("event__title", "user__username", "user__email", "id")
    readonly_fields = ("booked_at", "total_price", "booking_details")
    date_hierarchy = "booked_at"
    list_per_page = 30
    
    fieldsets = (
        ("Booking Information", {
            "fields": ("user", "event", "booked_at")
        }),
        ("Ticket Details", {
            "fields": ("ticket_type", "tickets", "total_price")
        }),
        ("Full Details", {
            "fields": ("booking_details",),
            "classes": ("collapse",)
        }),
    )

    def booking_id(self, obj):
        return format_html('<strong>#{:06d}</strong>', obj.id)
    booking_id.short_description = "Ref"

    def user_info(self, obj):
        return format_html(
            '<div><strong>{}</strong><br><span style="color: #666; font-size: 11px;">{}</span></div>',
            obj.user.username, obj.user.email
        )
    user_info.short_description = "User"

    def event_link(self, obj):
        url = reverse('admin:events_event_change', args=[obj.event.id])
        return format_html('<a href="{}" style="color: #007bff;">{}</a>', url, obj.event.title[:40])
    event_link.short_description = "Event"

    def ticket_badge(self, obj):
        colors = {'vip': '#dc3545', 'gold': '#ffc107', 'standard': '#28a745'}
        color = colors.get(obj.ticket_type, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: bold; text-transform: uppercase;">{}</span>',
            color, obj.ticket_type
        )
    ticket_badge.short_description = "Type"

    def tickets_count(self, obj):
        return format_html('<strong style="font-size: 16px;">{}</strong>', obj.tickets)
    tickets_count.short_description = "Qty"

    def price_display(self, obj):
        amount = float(obj.total_price)
        formatted_amount = f"K{amount:,.0f}"
        return format_html('<strong style="color: #28a745; font-size: 14px;">{}</strong>', formatted_amount)
    price_display.short_description = "Amount"

    def payment_status_badge(self, obj):
        try:
            payment = obj.payment
            status_colors = {
                'completed': '#28a745',
                'pending': '#ffc107',
                'failed': '#dc3545',
                'refunded': '#6c757d'
            }
            color = status_colors.get(payment.status, '#6c757d')
            return format_html(
                '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 10px; font-size: 10px; font-weight: bold;">{}</span>',
                color, payment.get_status_display()
            )
        except:
            return format_html('<span style="color: #999;">No payment</span>')
    payment_status_badge.short_description = "Payment"

    def date_booked(self, obj):
        return format_html(
            '<div style="font-size: 11px;"><strong>{}</strong><br>{}</div>',
            obj.booked_at.strftime('%b %d, %Y'),
            obj.booked_at.strftime('%I:%M %p')
        )
    date_booked.short_description = "Booked"

    def booking_details(self, obj):
        try:
            payment = obj.payment
            payment_info = f'''
                <p><strong>Payment Method:</strong> {payment.get_payment_method_display()}</p>
                <p><strong>Transaction ID:</strong> {payment.transaction_id}</p>
                <p><strong>Status:</strong> {payment.get_status_display()}</p>
            '''
        except:
            payment_info = '<p><em>No payment information</em></p>'
        
        formatted_price = f"K{float(obj.total_price):,.0f}"
        return format_html(
            '<div style="background: #f8f9fa; padding: 15px; border-radius: 8px;">'
            '<h3 style="margin-top: 0;">Complete Booking Details</h3>'
            '<p><strong>Booking Reference:</strong> #{:06d}</p>'
            '<p><strong>User:</strong> {} ({})</p>'
            '<p><strong>Event:</strong> {}</p>'
            '<p><strong>Ticket Type:</strong> {}</p>'
            '<p><strong>Quantity:</strong> {}</p>'
            '<p><strong>Total Price:</strong> {}</p>'
            '<p><strong>Booked At:</strong> {}</p>'
            '<hr>'
            '{}'
            '</div>',
            obj.id, obj.user.username, obj.user.email, obj.event.title,
            obj.get_ticket_type_display(), obj.tickets, formatted_price,
            obj.booked_at.strftime('%B %d, %Y at %I:%M %p'),
            mark_safe(payment_info)
        )
    booking_details.short_description = "Details"


# ============================
# EVENT GALLERY ADMIN
# ============================
@admin.register(EventGallery)
class EventGalleryAdmin(admin.ModelAdmin):
    list_display = ("image_preview", "event_name", "caption_short", "order", "edit_link")
    list_filter = ("event",)
    search_fields = ("event__title", "caption")
    list_editable = ("order",)
    list_per_page = 20
    
    fieldsets = (
        ("📋 Basic Information", {
            "fields": ("event", "caption", "order")
        }),
        ("🖼️ Image Upload", {
            "fields": ("image",),
            "description": "Upload an image for the event gallery"
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 80px; height: 80px; object-fit: cover; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />',
                obj.image.url
            )
        else:
            return format_html(
                '<div style="width: 80px; height: 80px; background: #f0f0f0; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #999;">'
                '<i class="fas fa-image"></i>'
                '</div>'
            )
    image_preview.short_description = "Preview"

    def event_name(self, obj):
        # Add category icon for context
        category_icons = {
            'music': '🎵',
            'tech': '💻', 
            'food': '🍽️',
            'sports': '⚽'
        }
        icon = category_icons.get(obj.event.category.slug, '📁')
        return format_html('<strong>{} {}</strong>', icon, obj.event.title)
    event_name.short_description = "Event"

    def caption_short(self, obj):
        if obj.caption:
            caption = obj.caption[:40] + '...' if len(obj.caption) > 40 else obj.caption
            return format_html('<span title="{}">{}</span>', obj.caption, caption)
        return format_html('<span style="color: #999;">No caption</span>')
    caption_short.short_description = "Caption"

    def edit_link(self, obj):
        return format_html(
            '<a href="/admin/events/eventgallery/{}/change/" style="color: #007bff; text-decoration: none;">'
            '<i class="fas fa-edit"></i> Edit'
            '</a>',
            obj.id
        )
    edit_link.short_description = "Actions"


# ============================
# PAYMENT TRANSACTION ADMIN
# ============================
@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ("transaction_id_display", "user_details", "event_name", "payment_method_badge", "amount_display", "status_badge", "quick_actions", "date_created")
    list_filter = ("status", "payment_method", "created_at", "booking__event__category")
    search_fields = ("transaction_id", "booking__user__username", "booking__user__email", "booking__event__title", "phone_number")
    readonly_fields = ("transaction_id", "created_at", "updated_at", "transaction_details", "payment_summary", "user_booking_history")
    date_hierarchy = "created_at"
    list_per_page = 25
    actions = ['approve_payments', 'reject_payments', 'mark_as_pending', 'export_transactions']
    ordering = ('-created_at',)
    
    fieldsets = (
        ("🔍 Transaction Overview", {
            "fields": ("payment_summary",),
            "description": "Quick overview of this payment transaction"
        }),
        ("📋 Transaction Info", {
            "fields": ("transaction_id", "booking", "status"),
            "classes": ("wide",)
        }),
        ("💳 Payment Details", {
            "fields": ("payment_method", "amount", "phone_number", "payment_proof"),
            "classes": ("wide",)
        }),
        ("⏰ Timeline", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
        ("📝 Admin Notes", {
            "fields": ("notes",),
            "classes": ("collapse",),
            "description": "Internal notes for admin reference"
        }),
        ("👤 User History", {
            "fields": ("user_booking_history",),
            "classes": ("collapse",),
            "description": "View this user's complete booking history"
        }),
        ("📊 Complete Details", {
            "fields": ("transaction_details",),
            "classes": ("collapse",)
        }),
    )

    def transaction_id_display(self, obj):
        # Color code based on payment method
        method_colors = {
            'mtn': '#ffcc00',
            'airtel': '#ed1c24', 
            'zamtel': '#009639',
            'bank': '#0066cc'
        }
        bg_color = method_colors.get(obj.payment_method, '#6c757d')
        
        return mark_safe(
            f'<div style="display: flex; align-items: center; gap: 8px;">'
            f'<div style="width: 4px; height: 40px; background: {bg_color}; border-radius: 2px;"></div>'
            f'<div>'
            f'<strong style="font-family: monospace; font-size: 13px; color: #333;">{obj.transaction_id}</strong><br>'
            f'<span style="font-size: 10px; color: #666; text-transform: uppercase;">{obj.get_payment_method_display()}</span>'
            f'</div>'
            f'</div>'
        )
    transaction_id_display.short_description = "TRANSACTION ID"

    def user_details(self, obj):
        # Count user's total bookings
        user_bookings = obj.booking.user.booking_set.count()
        user_payments = PaymentTransaction.objects.filter(booking__user=obj.booking.user).count()
        
        # Determine user status
        if user_bookings >= 5:
            status_badge = '<span style="background: #28a745; color: white; padding: 2px 6px; border-radius: 10px; font-size: 9px;">VIP</span>'
        elif user_bookings >= 2:
            status_badge = '<span style="background: #ffc107; color: white; padding: 2px 6px; border-radius: 10px; font-size: 9px;">REGULAR</span>'
        else:
            status_badge = '<span style="background: #6c757d; color: white; padding: 2px 6px; border-radius: 10px; font-size: 9px;">NEW</span>'
        
        return mark_safe(
            f'<div style="min-width: 150px;">'
            f'<div style="display: flex; align-items: center; gap: 6px; margin-bottom: 2px;">'
            f'<strong style="font-size: 13px;">{obj.booking.user.username}</strong> {status_badge}'
            f'</div>'
            f'<div style="color: #666; font-size: 11px;">{obj.booking.user.email}</div>'
            f'<div style="color: #999; font-size: 10px;">📊 {user_bookings} bookings</div>'
            f'</div>'
        )
    user_details.short_description = "USER"

    def event_name(self, obj):
        event = obj.booking.event
        # Category color coding
        category_colors = {
            'music': '#e91e63',
            'tech': '#2196f3', 
            'food': '#ff9800',
            'sports': '#9c27b0'
        }
        color = category_colors.get(event.category.slug, '#607d8b')
        
        title_display = event.title[:25] + ('...' if len(event.title) > 25 else '')
        return mark_safe(
            f'<div style="min-width: 180px;">'
            f'<div style="display: flex; align-items: center; gap: 6px; margin-bottom: 2px;">'
            f'<div style="width: 8px; height: 8px; background: {color}; border-radius: 50%;"></div>'
            f'<strong style="font-size: 12px;" title="{event.title}">{title_display}</strong>'
            f'</div>'
            f'<div style="color: #666; font-size: 10px;">📅 {event.date.strftime("%b %d, %Y")}</div>'
            f'<div style="color: #666; font-size: 10px;">🎫 {obj.booking.get_ticket_type_display()} × {obj.booking.tickets}</div>'
            f'</div>'
        )
    event_name.short_description = "EVENT"

    def payment_method_badge(self, obj):
        method_config = {
            'mtn': ('#ffcc00', 'MTN', '📱'),
            'airtel': ('#ed1c24', 'Airtel', '📱'),
            'zamtel': ('#009639', 'Zamtel', '📱'),
            'bank': ('#0066cc', 'Bank', '🏦')
        }
        color, name, icon = method_config.get(obj.payment_method, ('#6c757d', 'Unknown', '❓'))
        
        phone_display = ''
        if obj.phone_number and obj.payment_method in ['mtn', 'airtel', 'zamtel']:
            phone_display = f'<div style="font-size: 9px; color: #666; margin-top: 2px;">{obj.phone_number}</div>'
        
        return mark_safe(
            f'<div style="text-align: center; min-width: 80px;">'
            f'<div style="background: {color}; color: white; padding: 6px 10px; border-radius: 12px; font-size: 11px; font-weight: bold; margin-bottom: 2px;">'
            f'{icon} {name}'
            f'</div>'
            f'{phone_display}'
            f'</div>'
        )
    payment_method_badge.short_description = "METHOD"

    def amount_display(self, obj):
        amount = float(obj.amount)
        formatted_amount = f"K{amount:,.0f}"
        
        # Color based on amount ranges
        if amount >= 5000:
            color = '#28a745'  # Green for high amounts
            size_class = 'font-size: 16px; font-weight: bold;'
        elif amount >= 1000:
            color = '#ffc107'  # Yellow for medium amounts  
            size_class = 'font-size: 14px; font-weight: bold;'
        else:
            color = '#6c757d'  # Gray for low amounts
            size_class = 'font-size: 13px;'
        
        return mark_safe(
            f'<div style="text-align: center; min-width: 80px;">'
            f'<div style="color: {color}; {size_class};">{formatted_amount}</div>'
            f'<div style="font-size: 9px; color: #999;">ZMW</div>'
            f'</div>'
        )
    amount_display.short_description = "AMOUNT"

    def status_badge(self, obj):
        status_config = {
            'completed': ('#28a745', '✅', 'Approved'),
            'pending': ('#ffc107', '⏳', 'Pending'),
            'failed': ('#dc3545', '❌', 'Failed'),
            'refunded': ('#6c757d', '↩️', 'Refunded')
        }
        color, icon, display = status_config.get(obj.status, ('#6c757d', '❓', 'Unknown'))
        
        # Add pulsing animation for pending status
        animation = 'animation: pulse 2s infinite;' if obj.status == 'pending' else ''
        
        return mark_safe(
            f'<div style="text-align: center; min-width: 90px;">'
            f'<div style="background: {color}; color: white; padding: 6px 12px; border-radius: 15px; font-size: 11px; font-weight: bold; {animation};">'
            f'{icon} {display}'
            f'</div>'
            f'</div>'
        )
    status_badge.short_description = "STATUS"

    def date_created(self, obj):
        from django.utils import timezone
        now = timezone.now()
        diff = now - obj.created_at
        
        # Time ago calculation
        if diff.days > 0:
            time_ago = f"{diff.days}d ago"
        elif diff.seconds > 3600:
            time_ago = f"{diff.seconds // 3600}h ago"
        elif diff.seconds > 60:
            time_ago = f"{diff.seconds // 60}m ago"
        else:
            time_ago = "Just now"
        
        return mark_safe(
            f'<div style="text-align: center; min-width: 90px;">'
            f'<div style="font-size: 11px; font-weight: bold; color: #333;">{obj.created_at.strftime("%b %d")}</div>'
            f'<div style="font-size: 10px; color: #666;">{obj.created_at.strftime("%I:%M %p")}</div>'
            f'<div style="font-size: 9px; color: #999;">{time_ago}</div>'
            f'</div>'
        )
    date_created.short_description = "CREATED"

    def quick_actions(self, obj):
        if obj.status == 'pending':
            return mark_safe(
                f'<div style="display: flex; flex-direction: column; gap: 2px; min-width: 100px;">'
                f'<button onclick="approvePayment({obj.id})" '
                f'style="background: linear-gradient(135deg, #28a745, #20c997); color: white; border: none; padding: 4px 8px; border-radius: 6px; font-size: 10px; cursor: pointer; margin-bottom: 2px;">'
                f'✅ Approve'
                f'</button>'
                f'<button onclick="rejectPayment({obj.id})" '
                f'style="background: linear-gradient(135deg, #dc3545, #e74c3c); color: white; border: none; padding: 4px 8px; border-radius: 6px; font-size: 10px; cursor: pointer;">'
                f'❌ Reject'
                f'</button>'
                f'<a href="/admin/events/paymenttransaction/{obj.id}/change/" '
                f'style="color: #007bff; font-size: 9px; text-decoration: none; text-align: center; margin-top: 2px;">'
                f'🔍 Details'
                f'</a>'
                f'</div>'
            )
        elif obj.status == 'completed':
            return mark_safe(
                f'<div style="display: flex; flex-direction: column; gap: 2px; min-width: 100px;">'
                f'<div style="color: #28a745; font-size: 10px; text-align: center;">✅ Approved</div>'
                f'<a href="/admin/events/paymenttransaction/{obj.id}/change/" '
                f'style="color: #007bff; font-size: 9px; text-decoration: none; text-align: center; margin-top: 2px;">'
                f'🔍 Details'
                f'</a>'
                f'</div>'
            )
        elif obj.status == 'failed':
            return mark_safe(
                f'<div style="display: flex; flex-direction: column; gap: 2px; min-width: 100px;">'
                f'<div style="color: #dc3545; font-size: 10px; text-align: center;">❌ Rejected</div>'
                f'<a href="/admin/events/paymenttransaction/{obj.id}/change/" '
                f'style="color: #007bff; font-size: 9px; text-decoration: none; text-align: center; margin-top: 2px;">'
                f'🔍 Details'
                f'</a>'
                f'</div>'
            )
        else:
            return mark_safe(
                f'<div style="display: flex; flex-direction: column; gap: 2px; min-width: 100px;">'
                f'<div style="color: #6c757d; font-size: 10px; text-align: center;">No actions</div>'
                f'<a href="/admin/events/paymenttransaction/{obj.id}/change/" '
                f'style="color: #007bff; font-size: 9px; text-decoration: none; text-align: center; margin-top: 2px;">'
                f'🔍 Details'
                f'</a>'
                f'</div>'
            )
    quick_actions.short_description = "QUICK ACTIONS"

    def payment_summary(self, obj):
        """Enhanced payment overview with visual elements"""
        status_colors = {
            'completed': '#28a745',
            'pending': '#ffc107', 
            'failed': '#dc3545',
            'refunded': '#6c757d'
        }
        status_color = status_colors.get(obj.status, '#6c757d')
        
        method_icons = {
            'mtn': '📱 MTN MoMo',
            'airtel': '📱 Airtel Money',
            'zamtel': '📱 Zamtel Money', 
            'bank': '🏦 Bank Transfer'
        }
        method_display = method_icons.get(obj.payment_method, '❓ Unknown')
        
        return mark_safe(
            f'<div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 20px; border-radius: 12px; border-left: 5px solid {status_color};">'
            f'<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 15px;">'
            f'<div>'
            f'<h4 style="margin: 0 0 8px 0; color: #495057;">💳 Payment Details</h4>'
            f'<p style="margin: 4px 0;"><strong>Amount:</strong> <span style="color: #28a745; font-size: 18px;">K{float(obj.amount):,.0f}</span></p>'
            f'<p style="margin: 4px 0;"><strong>Method:</strong> {method_display}</p>'
            f'<p style="margin: 4px 0;"><strong>Phone:</strong> {obj.phone_number or "N/A"}</p>'
            f'</div>'
            f'<div>'
            f'<h4 style="margin: 0 0 8px 0; color: #495057;">📊 Status</h4>'
            f'<p style="margin: 4px 0;"><strong>Current:</strong> <span style="color: {status_color}; font-weight: bold;">{obj.get_status_display()}</span></p>'
            f'<p style="margin: 4px 0;"><strong>Transaction:</strong> <code>{obj.transaction_id}</code></p>'
            f'<p style="margin: 4px 0;"><strong>Created:</strong> {obj.created_at.strftime("%b %d, %Y at %I:%M %p")}</p>'
            f'</div>'
            f'</div>'
            f'<div style="background: white; padding: 12px; border-radius: 8px; border: 1px solid #dee2e6;">'
            f'<h5 style="margin: 0 0 8px 0; color: #495057;">🎫 Booking Information</h5>'
            f'<p style="margin: 4px 0;"><strong>Event:</strong> {obj.booking.event.title}</p>'
            f'<p style="margin: 4px 0;"><strong>User:</strong> {obj.booking.user.username} ({obj.booking.user.email})</p>'
            f'<p style="margin: 4px 0;"><strong>Tickets:</strong> {obj.booking.tickets} × {obj.booking.get_ticket_type_display()} = K{float(obj.booking.total_price):,.0f}</p>'
            f'</div>'
            f'</div>'
        )
    payment_summary.short_description = "Payment Overview"

    def user_booking_history(self, obj):
        """Display user's complete booking history"""
        user = obj.booking.user
        user_bookings = user.booking_set.order_by('-booked_at')[:10]  # Last 10 bookings
        total_spent = user.booking_set.aggregate(total=Sum('total_price'))['total'] or 0
        
        history_html = f'''
        <div style="background: #f8f9fa; padding: 15px; border-radius: 8px;">
            <h4 style="margin-top: 0; color: #495057;">👤 {user.username}'s Booking History</h4>
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; margin-bottom: 15px;">
                <div style="text-align: center; background: white; padding: 10px; border-radius: 6px;">
                    <div style="font-size: 24px; font-weight: bold; color: #007bff;">{user_bookings.count()}</div>
                    <div style="font-size: 12px; color: #666;">Total Bookings</div>
                </div>
                <div style="text-align: center; background: white; padding: 10px; border-radius: 6px;">
                    <div style="font-size: 24px; font-weight: bold; color: #28a745;">K{total_spent:,.0f}</div>
                    <div style="font-size: 12px; color: #666;">Total Spent</div>
                </div>
                <div style="text-align: center; background: white; padding: 10px; border-radius: 6px;">
                    <div style="font-size: 24px; font-weight: bold; color: #ffc107;">{PaymentTransaction.objects.filter(booking__user=user, status='completed').count()}</div>
                    <div style="font-size: 12px; color: #666;">Successful Payments</div>
                </div>
            </div>
            <h5 style="margin: 15px 0 10px 0;">Recent Bookings:</h5>
            <div style="max-height: 300px; overflow-y: auto;">
        '''
        
        for booking in user_bookings:
            try:
                payment_status = booking.payment.get_status_display()
                payment_color = {'Completed': '#28a745', 'Pending': '#ffc107', 'Failed': '#dc3545'}.get(payment_status, '#6c757d')
            except:
                payment_status = 'No Payment'
                payment_color = '#999'
                
            history_html += f'''
                <div style="background: white; padding: 10px; margin-bottom: 8px; border-radius: 6px; border-left: 3px solid {payment_color};">
                    <div style="display: flex; justify-content: between; align-items: center;">
                        <div style="flex: 1;">
                            <strong>{booking.event.title}</strong><br>
                            <small style="color: #666;">{booking.booked_at.strftime('%b %d, %Y')} • {booking.get_ticket_type_display()} × {booking.tickets}</small>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-weight: bold;">K{float(booking.total_price):,.0f}</div>
                            <div style="font-size: 10px; color: {payment_color};">{payment_status}</div>
                        </div>
                    </div>
                </div>
            '''
        
        history_html += '</div></div>'
        return format_html(history_html)
    user_booking_history.short_description = "User History"

    def approve_payments(self, request, queryset):
        """Bulk action to approve pending payments"""
        count = 0
        for payment in queryset.filter(status='pending'):
            payment.status = 'completed'
            payment.notes += f"\n\nApproved by admin: {request.user.username} on {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}"
            payment.save()
            count += 1
        self.message_user(request, f"✅ Successfully approved {count} payment(s). Confirmation emails sent to users.")
    approve_payments.short_description = "✅ Approve selected payments"

    def reject_payments(self, request, queryset):
        """Bulk action to reject pending payments"""
        count = 0
        for payment in queryset.filter(status='pending'):
            payment.status = 'failed'
            payment.notes += f"\n\nRejected by admin: {request.user.username} on {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}"
            payment.save()
            count += 1
        self.message_user(request, f"❌ Rejected {count} payment(s).")
    reject_payments.short_description = "❌ Reject selected payments"

    def mark_as_pending(self, request, queryset):
        """Bulk action to mark payments as pending for review"""
        count = 0
        for payment in queryset.exclude(status='pending'):
            payment.status = 'pending'
            payment.notes += f"\n\nMarked as pending by admin: {request.user.username} on {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}"
            payment.save()
            count += 1
        self.message_user(request, f"⏳ Marked {count} payment(s) as pending for review.")
    mark_as_pending.short_description = "⏳ Mark as pending review"

    def export_transactions(self, request, queryset):
        """Export selected transactions to CSV"""
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="payment_transactions.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Transaction ID', 'User', 'Email', 'Event', 'Amount', 'Method', 'Status', 'Created', 'Phone'])
        
        for payment in queryset:
            writer.writerow([
                payment.transaction_id,
                payment.booking.user.username,
                payment.booking.user.email,
                payment.booking.event.title,
                float(payment.amount),
                payment.get_payment_method_display(),
                payment.get_status_display(),
                payment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                payment.phone_number or ''
            ])
        
        self.message_user(request, f"📊 Exported {queryset.count()} transactions to CSV.")
        return response
    export_transactions.short_description = "📊 Export to CSV"

    def transaction_details(self, obj):
        proof_html = ''
        if obj.payment_proof:
            proof_html = f'<p><strong>Payment Proof:</strong> <a href="{obj.payment_proof.url}" target="_blank">View File</a></p>'
        
        formatted_amount = f"K{float(obj.amount):,.0f}"
        return format_html(
            '<div style="background: #f8f9fa; padding: 15px; border-radius: 8px;">'
            '<h3 style="margin-top: 0;">Complete Transaction Details</h3>'
            '<p><strong>Transaction ID:</strong> {}</p>'
            '<p><strong>User:</strong> {} ({})</p>'
            '<p><strong>Event:</strong> {}</p>'
            '<p><strong>Booking Reference:</strong> #{:06d}</p>'
            '<p><strong>Payment Method:</strong> {}</p>'
            '<p><strong>Amount:</strong> {}</p>'
            '<p><strong>Phone Number:</strong> {}</p>'
            '<p><strong>Status:</strong> {}</p>'
            '<p><strong>Created:</strong> {}</p>'
            '<p><strong>Updated:</strong> {}</p>'
            '{}'
            '<hr>'
            '<p><strong>Notes:</strong></p>'
            '<p style="white-space: pre-wrap;">{}</p>'
            '</div>',
            obj.transaction_id,
            obj.booking.user.username, obj.booking.user.email,
            obj.booking.event.title,
            obj.booking.id,
            obj.get_payment_method_display(),
            formatted_amount,
            obj.phone_number or 'N/A',
            obj.get_status_display(),
            obj.created_at.strftime('%B %d, %Y at %I:%M %p'),
            obj.updated_at.strftime('%B %d, %Y at %I:%M %p'),
            mark_safe(proof_html),
            obj.notes or 'No notes'
        )
    transaction_details.short_description = "Details"


# ============================
# USER PROFILE ADMIN
# ============================
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user_info", "phone_display", "bookings_count", "total_spent", "date_joined")
    search_fields = ("user__username", "user__email", "phone_number")
    readonly_fields = ("created_at", "updated_at", "user_stats")
    list_per_page = 30
    
    fieldsets = (
        ("User Information", {
            "fields": ("user", "phone_number")
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
        ("Statistics", {
            "fields": ("user_stats",),
            "classes": ("collapse",)
        }),
    )
    
    def user_info(self, obj):
        return format_html(
            '<div><strong>{}</strong><br><span style="color: #666; font-size: 11px;">{}</span></div>',
            obj.user.username, obj.user.email
        )
    user_info.short_description = "User"
    
    def phone_display(self, obj):
        if obj.phone_number:
            return format_html(
                '<span style="font-family: monospace;"><i class="fas fa-phone text-green-600 mr-1"></i>{}</span>',
                obj.phone_number
            )
        return format_html('<span style="color: #999;">No phone</span>')
    phone_display.short_description = "Phone Number"
    
    def bookings_count(self, obj):
        count = obj.user.booking_set.count()
        return format_html(
            '<span style="background: #17a2b8; color: white; padding: 3px 10px; border-radius: 12px; font-weight: bold;">{}</span>',
            count
        )
    bookings_count.short_description = "Bookings"
    
    def total_spent(self, obj):
        total = obj.user.booking_set.aggregate(total=Sum('total_price'))['total']
        if total is None:
            total = 0
        else:
            total = float(total)
        formatted_amount = f"K{total:,.0f}"
        return format_html('<strong style="color: #28a745;">{}</strong>', formatted_amount)
    total_spent.short_description = "Total Spent"
    
    def date_joined(self, obj):
        return format_html(
            '<div style="font-size: 11px;"><strong>{}</strong></div>',
            obj.user.date_joined.strftime('%b %d, %Y')
        )
    date_joined.short_description = "Joined"
    
    def user_stats(self, obj):
        bookings = obj.user.booking_set.all()
        total_spent = bookings.aggregate(total=Sum('total_price'))['total']
        if total_spent is None:
            total_spent = 0
        else:
            total_spent = float(total_spent)
        
        return format_html(
            '<div style="background: #f8f9fa; padding: 15px; border-radius: 8px;">'
            '<h3 style="margin-top: 0;">User Statistics</h3>'
            '<p><strong>Username:</strong> {}</p>'
            '<p><strong>Email:</strong> {}</p>'
            '<p><strong>Phone:</strong> {}</p>'
            '<p><strong>Total Bookings:</strong> {}</p>'
            '<p><strong>Total Spent:</strong> K{:,.0f}</p>'
            '<p><strong>Member Since:</strong> {}</p>'
            '</div>',
            obj.user.username,
            obj.user.email,
            obj.phone_number or 'Not provided',
            bookings.count(),
            total_spent,
            obj.user.date_joined.strftime('%B %d, %Y')
        )
    user_stats.short_description = "Statistics"


# ============================
# CUSTOM ADMIN SITE CONFIGURATION
# ============================
admin.site.site_header = "Momenta Administration"
admin.site.site_title = "Momenta Admin"
admin.site.index_title = "Welcome to Momenta Management"