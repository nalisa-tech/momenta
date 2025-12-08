from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.db import models
from .models import Event, Category, Booking, PaymentTransaction
import requests
import json
import time
import random


# ==============================
# CATEGORY LIST PAGE
# ==============================
def categories_with_events(request):
    categories = Category.objects.prefetch_related("events").all()
    return render(request, "events/categories_with_events.html", {
        "categories": categories
    })


# ==============================
# HOME PAGE
# ==============================
def home(request):
    events = Event.objects.all().order_by("-date")
    return render(request, "home.html", {"events": events})


# ==============================
# EVENT DETAIL PAGE
# ==============================
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, "events/event_detail.html", {"event": event})


# ==============================
# BOOK EVENT (OLD SIMPLE BOOKING)
# ==============================
@login_required
def book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        tickets = int(request.POST.get("tickets", 1))
        Booking.objects.create(
            user=request.user,
            event=event,
            tickets=tickets
        )
        messages.success(request, f"You booked {tickets} ticket(s) for {event.title}!")
        return redirect("events:home")

    return render(request, "booking.html", {"event": event})


# ==============================
# USER REGISTRATION
# ==============================
def register_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        phone_number = request.POST.get("phone_number", "")
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("events:register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect("events:register")

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password1)
        
        # Save phone number to profile
        if phone_number:
            user.profile.phone_number = phone_number
            user.profile.save()
        
        messages.success(request, "Account created! Please log in.")
        return redirect("events:login")

    return render(request, "register.html")


# ==============================
# USER LOGIN
# ==============================
def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("events:home")

        messages.error(request, "Invalid username or password.")
        return redirect("events:login")

    return render(request, "login.html")


# ==============================
# USER LOGOUT
# ==============================
def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("events:home")


# ==============================
# CATEGORY PAGE (DYNAMIC)
# ==============================
def category_events(request, slug):
    category = get_object_or_404(Category, slug=slug)
    events = Event.objects.filter(category=category)
    return render(request, "events/category.html", {
        "category": category,
        "events": events
    })


# ==============================
# DYNAMIC CATEGORY PAGE (REPLACES ALL 4 STATIC ONES)
# ==============================
# ADD THIS FUNCTION TO views.py (anywhere near the bottom)
def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    events = Event.objects.filter(category=category).order_by('-date')
    
    title_map = {
        'music': 'Music & Concerts',
        'tech': 'Tech & Innovation',
        'food': 'Food & Festivals',
        'sports': 'Sports & Recreation',
    }
    page_title = title_map.get(slug, category.name)

    return render(request, "events/category_detail.html", {
        "category": category,
        "events": events,
        "page_title": page_title
    })
# ==============================
# SEAT SELECTION PAGE
# ==============================
@login_required
def select_seat(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, "events/select_seat.html", {"event": event})


# ==============================
# PAYMENT PAGE
# ==============================
@login_required
def payment_page(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        ticket_type = request.POST.get("ticket_type")
        try:
            tickets = int(request.POST.get("tickets", 1))
        except ValueError:
            messages.error(request, "Invalid number of tickets.")
            return redirect("events:select_seat", event_id=event.id)

        # Validate ticket type
        if not ticket_type or ticket_type not in ['vip', 'gold', 'standard']:
            messages.error(request, f"Invalid ticket type. Please select a valid ticket type.")
            return redirect("events:select_seat", event_id=event.id)

        # Check seat availability
        seats_available = {
            'vip': event.vip_seats_left or 0,
            'gold': event.gold_seats_left or 0,
            'standard': event.standard_seats_left or 0
        }
        
        if tickets > seats_available[ticket_type]:
            messages.error(request, f"Only {seats_available[ticket_type]} {ticket_type.upper()} seats available.")
            return redirect("events:select_seat", event_id=event.id)

        prices = {'vip': 1500, 'gold': 850, 'standard': 450}
        total_price = tickets * prices[ticket_type]

        # COMPLETE PAYMENT
        if "payment_method" in request.POST or "selected_payment_method" in request.POST:
            payment_method = request.POST.get("payment_method") or request.POST.get("selected_payment_method")
            
            # Get payment details based on method
            payment_details = {}
            phone_number = request.POST.get("phone_number")
            
            if payment_method == "mtn":
                payment_details['phone'] = phone_number
                payment_details['provider'] = "MTN Mobile Money"
            elif payment_method == "airtel":
                payment_details['phone'] = phone_number
                payment_details['provider'] = "Airtel Money"
            elif payment_method == "zamtel":
                payment_details['phone'] = phone_number
                payment_details['provider'] = "Zamtel Money"
            elif payment_method == "bank":
                payment_details['provider'] = "Bank Transfer"
                # Handle file upload for bank transfer
                if 'payment_proof' in request.FILES:
                    payment_details['proof'] = request.FILES['payment_proof']

            # Process payment (simulate for now - in production, integrate with real APIs)
            print(f"Processing payment: {payment_method}, Amount: {total_price}, Details: {payment_details}")
            
            try:
                payment_success = process_payment(payment_method, total_price, payment_details)
                print(f"Payment result: {payment_success}")
            except Exception as e:
                print(f"Payment processing error: {e}")
                payment_success = True  # For demo, assume success
            
            if payment_success:
                # Create booking
                booking = Booking.objects.create(
                    user=request.user,
                    event=event,
                    ticket_type=ticket_type,
                    tickets=tickets
                )

                # Create payment transaction with PENDING status
                # Admin must confirm payment before ticket is valid
                payment_transaction = PaymentTransaction.objects.create(
                    booking=booking,
                    payment_method=payment_method,
                    amount=total_price,
                    status='pending',  # Requires admin confirmation
                    phone_number=payment_details.get('phone', ''),
                    payment_proof=payment_details.get('proof') if payment_method == 'bank' else None,
                    notes=f"Payment initiated by {request.user.username}. Awaiting admin confirmation."
                )

                # DO NOT update seat counts yet - wait for admin confirmation
                # Seats will be reserved when admin confirms payment
                # event.vip_seats_left -= tickets  # DISABLED
                # event.gold_seats_left -= tickets  # DISABLED
                # event.standard_seats_left -= tickets  # DISABLED
                # event.save()  # DISABLED
                
                # Send confirmation email
                email_sent = send_booking_confirmation_email(
                    booking=booking,
                    event=event,
                    payment_method=payment_details.get('provider', payment_method),
                    payment_details=payment_details
                )
                
                # Update messages to reflect pending status
                messages.success(request, f"🎉 Payment submitted successfully!")
                messages.warning(request, f"⏳ Your payment is pending admin confirmation. Booking Reference: #{booking.id:06d}")
                messages.info(request, "📧 You will receive a confirmation email once the admin approves your payment.")
                messages.info(request, "💡 Please keep your booking reference number for tracking.")

                return render(request, "events/payment_success.html", {
                    "event": event,
                    "payment_method": payment_details.get('provider', payment_method),
                    "tickets": tickets,
                    "ticket_type": ticket_type,
                    "total_price": total_price,
                    "booking": booking,
                    "payment_details": payment_details,
                    "email_sent": email_sent,
                })
            else:
                messages.error(request, "Payment failed. Please try again or use a different payment method.")
                return redirect("events:select_seat", event_id=event.id)

        # SHOW PAYMENT PAGE
        return render(request, "events/payment_page.html", {
            "event": event,
            "ticket_type": ticket_type,
            "tickets": tickets,
            "total_price": total_price,
            "mtn_number": settings.MTN_NUMBER,
            "airtel_number": settings.AIRTEL_NUMBER,
            "zamtel_number": settings.ZAMTEL_NUMBER,
            "bank_name": settings.BANK_NAME,
            "bank_account_number": settings.BANK_ACCOUNT_NUMBER,
            "bank_account_name": settings.BANK_ACCOUNT_NAME,
        })

    return redirect("events:select_seat", event_id=event.id)


# ==============================
# USER PROFILE & BOOKINGS
# ==============================
@login_required
def user_profile(request):
    bookings = Booking.objects.filter(user=request.user).select_related('event').order_by('-booked_at')
    return render(request, "events/profile.html", {
        "bookings": bookings
    })


# ==============================
# PAYMENT PROCESSING FUNCTION
# ==============================
def process_payment(payment_method, amount, payment_details):
    """
    Process payment through various Zambian payment providers
    This is a simulation - in production, integrate with real APIs
    """
    
    if payment_method == "mtn":
        return process_mtn_payment(amount, payment_details.get('phone'))
    elif payment_method == "airtel":
        return process_airtel_payment(amount, payment_details.get('phone'))
    elif payment_method == "zamtel":
        return process_zamtel_payment(amount, payment_details.get('phone'))
    elif payment_method == "bank":
        return process_bank_transfer(amount, payment_details)
    
    return False


def process_mtn_payment(amount, phone_number):
    """
    Process MTN Mobile Money payment
    In production, integrate with MTN MoMo API
    """
    try:
        # Simulate API call to MTN Mobile Money
        print(f"Processing MTN payment: K{amount} from {phone_number}")
        
        # Simulate processing time
        time.sleep(2)
        
        # Simulate success/failure (90% success rate for demo)
        success = random.random() > 0.1
        
        if success:
            print(f"MTN payment successful: Transaction ID MTN{random.randint(100000, 999999)}")
            return True
        else:
            print("MTN payment failed: Insufficient balance or user cancelled")
            return False
            
    except Exception as e:
        print(f"MTN payment error: {e}")
        return False


def process_airtel_payment(amount, phone_number):
    """
    Process Airtel Money payment
    In production, integrate with Airtel Money API
    """
    try:
        # Simulate API call to Airtel Money
        print(f"Processing Airtel payment: K{amount} from {phone_number}")
        
        # Simulate processing time
        time.sleep(2)
        
        # Simulate success/failure (90% success rate for demo)
        success = random.random() > 0.1
        
        if success:
            print(f"Airtel payment successful: Transaction ID AIR{random.randint(100000, 999999)}")
            return True
        else:
            print("Airtel payment failed: Insufficient balance or user cancelled")
            return False
            
    except Exception as e:
        print(f"Airtel payment error: {e}")
        return False


def process_zamtel_payment(amount, phone_number):
    """
    Process Zamtel Money payment
    In production, integrate with Zamtel Money API
    """
    try:
        # Simulate API call to Zamtel Money
        print(f"Processing Zamtel payment: K{amount} from {phone_number}")
        
        # Simulate processing time
        time.sleep(2)
        
        # Simulate success/failure (90% success rate for demo)
        success = random.random() > 0.1
        
        if success:
            print(f"Zamtel payment successful: Transaction ID ZMT{random.randint(100000, 999999)}")
            return True
        else:
            print("Zamtel payment failed: Insufficient balance or user cancelled")
            return False
            
    except Exception as e:
        print(f"Zamtel payment error: {e}")
        return False


def process_bank_transfer(amount, payment_details):
    """
    Process bank transfer payment
    In production, integrate with bank APIs or manual verification
    """
    try:
        print(f"Processing bank transfer: K{amount}")
        
        # For bank transfers, we typically need manual verification
        # In production, you might:
        # 1. Save the proof of payment file
        # 2. Send notification to admin for verification
        # 3. Mark payment as "pending verification"
        
        # For demo, we'll simulate immediate success
        time.sleep(1)
        
        print(f"Bank transfer received: Reference BNK{random.randint(100000, 999999)}")
        return True
        
    except Exception as e:
        print(f"Bank transfer error: {e}")
        return False


# ==============================
# EMAIL NOTIFICATION FUNCTION
# ==============================
def send_booking_confirmation_email(booking, event, payment_method, payment_details):
    """
    Send booking confirmation email to user
    """
    print("=" * 60)
    print("🔔 SENDING BOOKING CONFIRMATION EMAIL")
    print("=" * 60)
    try:
        user = booking.user
        subject = f'Booking Confirmation - {event.title}'
        
        # Create email message
        message = f"""
Dear {user.get_full_name() or user.username},

Thank you for booking with Momenta!

BOOKING CONFIRMATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Booking Reference: #{booking.id:06d}
Event: {event.title}
Date: {event.date.strftime('%A, %B %d, %Y')}
{'Time: ' + event.time.strftime('%I:%M %p') if event.time else ''}
Location: {event.location}

TICKET DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Ticket Type: {booking.get_ticket_type_display()}
Number of Tickets: {booking.tickets}
Total Amount Paid: K{booking.total_price}

PAYMENT INFORMATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Payment Method: {payment_method}
{'Phone Number: ' + payment_details.get('phone', '') if payment_details.get('phone') else ''}
Payment Status: CONFIRMED ✓

IMPORTANT INFORMATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Please arrive at least 30 minutes before the event starts
• Bring a valid ID for verification
• Your booking reference: #{booking.id:06d}
• Present this email or your booking reference at the entrance

ORGANIZER CONTACT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{event.organizer_name}
Phone: {event.organizer_phone}

For any questions or concerns, please contact us:
Email: nalisaimbula282@gmail.com
Phone: 0978308101

Thank you for choosing Momenta!
We look forward to seeing you at the event.

Best regards,
The Momenta Team

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
This is an automated confirmation email. Please do not reply.
Visit us at: http://127.0.0.1:8000/
        """
        
        # Send email
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        
        print(f"✓ Confirmation email sent to {user.email}")
        print("=" * 60)
        print("📧 EMAIL CONTENT ABOVE (in console mode)")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"✗ Email sending failed: {e}")
        print("=" * 60)
        return False

# ==============================
# ADMIN PAYMENT ACTIONS
# ==============================

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

@staff_member_required
@csrf_exempt
def approve_payment(request, payment_id):
    """Approve a payment transaction"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    try:
        payment = get_object_or_404(PaymentTransaction, id=payment_id)
        
        if payment.status != 'pending':
            return JsonResponse({
                'error': f'Payment is already {payment.get_status_display().lower()}'
            }, status=400)
        
        # Update payment status
        payment.status = 'completed'
        payment.notes += f"\n\nApproved by admin: {request.user.username} on {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}"
        payment.save()
        
        # Reduce seat count when payment is approved
        booking = payment.booking
        event = booking.event
        ticket_type = booking.ticket_type
        tickets = booking.tickets
        
        if ticket_type == 'vip':
            event.vip_seats_left = max(0, (event.vip_seats_left or 0) - tickets)
        elif ticket_type == 'gold':
            event.gold_seats_left = max(0, (event.gold_seats_left or 0) - tickets)
        elif ticket_type == 'standard':
            event.standard_seats_left = max(0, (event.standard_seats_left or 0) - tickets)
        
        event.save()
        
        # Send confirmation email to user
        try:
            send_payment_confirmation_email(payment)
        except Exception as e:
            print(f"Email sending failed: {e}")
        
        return JsonResponse({
            'success': True,
            'message': f'Payment {payment.transaction_id} approved successfully',
            'new_status': 'completed'
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@staff_member_required
@csrf_exempt
def reject_payment(request, payment_id):
    """Reject a payment transaction"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    try:
        payment = get_object_or_404(PaymentTransaction, id=payment_id)
        
        if payment.status != 'pending':
            return JsonResponse({
                'error': f'Payment is already {payment.get_status_display().lower()}'
            }, status=400)
        
        # Update payment status
        payment.status = 'failed'
        payment.notes += f"\n\nRejected by admin: {request.user.username} on {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}"
        payment.save()
        
        # Send rejection email to user
        try:
            send_payment_rejection_email(payment)
        except Exception as e:
            print(f"Email sending failed: {e}")
        
        return JsonResponse({
            'success': True,
            'message': f'Payment {payment.transaction_id} rejected',
            'new_status': 'failed'
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def send_payment_confirmation_email(payment):
    """Send payment confirmation email to user"""
    user = payment.booking.user
    event = payment.booking.event
    
    subject = f'🎉 Payment Confirmed - {event.title}'
    
    # Create HTML email content
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%); padding: 20px; text-align: center; color: white;">
            <h1>🎉 Payment Confirmed!</h1>
            <p>Your booking for {event.title} has been approved</p>
        </div>
        
        <div style="padding: 20px;">
            <h2>✅ Booking Details</h2>
            
            <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 20px 0;">
                <p><strong>Event:</strong> {event.title}</p>
                <p><strong>Date:</strong> {event.date.strftime('%B %d, %Y')}</p>
                <p><strong>Time:</strong> {event.time}</p>
                <p><strong>Location:</strong> {event.location}</p>
                <p><strong>Ticket Type:</strong> {payment.booking.get_ticket_type_display()}</p>
                <p><strong>Quantity:</strong> {payment.booking.tickets}</p>
                <p><strong>Total Paid:</strong> K{float(payment.amount):,.0f}</p>
            </div>
            
            <div style="background: #d4edda; padding: 15px; border-radius: 8px; border-left: 4px solid #28a745;">
                <h3 style="margin-top: 0; color: #155724;">🎫 Your Tickets Are Ready!</h3>
                <p style="color: #155724;">Your payment has been confirmed and your tickets are now valid. Please bring this confirmation email or show it on your phone at the event entrance.</p>
            </div>
            
            <div style="text-align: center; margin-top: 30px;">
                <p><strong>Transaction ID:</strong> {payment.transaction_id}</p>
                <p style="color: #666;">Thank you for choosing Momenta!</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Send email
    email = EmailMessage(
        subject=subject,
        body=html_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    email.content_subtype = 'html'
    email.send()


def send_payment_rejection_email(payment):
    """Send payment rejection email to user"""
    user = payment.booking.user
    event = payment.booking.event
    
    subject = f'❌ Payment Issue - {event.title}'
    
    # Create HTML email content
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background: linear-gradient(135deg, #dc3545 0%, #c82333 100%); padding: 20px; text-align: center; color: white;">
            <h1>❌ Payment Issue</h1>
            <p>There was an issue with your payment for {event.title}</p>
        </div>
        
        <div style="padding: 20px;">
            <h2>Payment Status Update</h2>
            
            <div style="background: #f8d7da; padding: 15px; border-radius: 8px; border-left: 4px solid #dc3545; margin: 20px 0;">
                <h3 style="margin-top: 0; color: #721c24;">Payment Not Approved</h3>
                <p style="color: #721c24;">Unfortunately, we were unable to verify your payment for this booking. This could be due to:</p>
                <ul style="color: #721c24;">
                    <li>Payment verification failed</li>
                    <li>Insufficient payment amount</li>
                    <li>Payment method issues</li>
                </ul>
            </div>
            
            <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 20px 0;">
                <p><strong>Event:</strong> {event.title}</p>
                <p><strong>Transaction ID:</strong> {payment.transaction_id}</p>
                <p><strong>Amount:</strong> K{float(payment.amount):,.0f}</p>
            </div>
            
            <div style="background: #d1ecf1; padding: 15px; border-radius: 8px; border-left: 4px solid #bee5eb;">
                <h3 style="margin-top: 0; color: #0c5460;">What to do next:</h3>
                <p style="color: #0c5460;">Please contact our support team or try booking again with a different payment method. We're here to help!</p>
            </div>
            
            <div style="text-align: center; margin-top: 30px;">
                <p style="color: #666;">Contact us: nalisaimbula282@gmail.com</p>
                <p style="color: #666;">Momenta Team</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Send email
    email = EmailMessage(
        subject=subject,
        body=html_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    email.content_subtype = 'html'
    email.send()
# ==============================
# NEWSLETTER SUBSCRIPTION
# ==============================

def subscribe_newsletter(request):
    """Handle newsletter subscription"""
    if request.method == 'POST':
        email = request.POST.get('email')
        
        if email:
            try:
                # Send welcome email to subscriber
                send_mail(
                    subject='🎉 Welcome to Momenta Newsletter!',
                    message=f'''
                    Hello!
                    
                    Thank you for subscribing to the Momenta newsletter!
                    
                    You'll now receive updates about:
                    ✅ New events in Zambia
                    ✅ Early bird ticket offers
                    ✅ Exclusive event previews
                    ✅ Special promotions
                    
                    Stay tuned for amazing events!
                    
                    Best regards,
                    Momenta Team
                    ''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=True,
                )
                
                # Send notification to admin
                send_mail(
                    subject='📧 New Newsletter Subscription',
                    message=f'New newsletter subscription: {email}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=['nalisaimbula282@gmail.com'],
                    fail_silently=True,
                )
                
                messages.success(request, f'🎉 Successfully subscribed! Check {email} for confirmation.')
                
            except Exception as e:
                messages.error(request, 'Subscription failed. Please try again.')
        else:
            messages.error(request, 'Please enter a valid email address.')
    
    # Redirect back to the previous page or home
    return redirect(request.META.get('HTTP_REFERER', 'events:home'))

# ==============================
# EVENTS LISTING PAGE
# ==============================
def events_list(request):
    """Display all upcoming events with filtering and search"""
    from django.utils import timezone
    from django.db.models import Q
    
    # Get all upcoming events (future events only)
    events = Event.objects.filter(date__gte=timezone.now().date()).order_by('date')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        events = events.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    
    # Category filtering
    category_filter = request.GET.get('category', '')
    if category_filter:
        events = events.filter(category__slug=category_filter)
    
    # Get all categories for filter dropdown
    categories = Category.objects.all()
    
    context = {
        'events': events,
        'categories': categories,
        'search_query': search_query,
        'category_filter': category_filter,
        'total_events': events.count()
    }
    
    return render(request, 'events/events_list.html', context)