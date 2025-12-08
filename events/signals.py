# events/signals.py

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import PaymentTransaction


@receiver(pre_save, sender=PaymentTransaction)
def handle_payment_confirmation(sender, instance, **kwargs):
    """
    Handle payment status changes - update seat counts when admin confirms payment
    """
    # Check if this is an update (not a new record)
    if instance.pk:
        try:
            # Get the old instance from database
            old_instance = PaymentTransaction.objects.get(pk=instance.pk)
            
            # Check if status changed from pending to completed
            if old_instance.status == 'pending' and instance.status == 'completed':
                # Payment confirmed by admin - update seat counts
                booking = instance.booking
                event = booking.event
                
                # Update seat counts based on ticket type
                if booking.ticket_type == 'vip':
                    event.vip_seats_left -= booking.tickets
                elif booking.ticket_type == 'gold':
                    event.gold_seats_left -= booking.tickets
                elif booking.ticket_type == 'standard':
                    event.standard_seats_left -= booking.tickets
                
                event.save()
                
                # Add note to transaction
                instance.notes += f"\n\nPayment confirmed by admin. Seats reserved: {booking.tickets} x {booking.get_ticket_type_display()}"
                
                # Send confirmation email to user
                try:
                    send_confirmation_email_to_user(booking, event, instance)
                except Exception as e:
                    print(f"Failed to send confirmation email: {e}")
                    
            # Check if status changed from completed to refunded
            elif old_instance.status == 'completed' and instance.status == 'refunded':
                # Payment refunded - restore seat counts
                booking = instance.booking
                event = booking.event
                
                # Restore seat counts
                if booking.ticket_type == 'vip':
                    event.vip_seats_left += booking.tickets
                elif booking.ticket_type == 'gold':
                    event.gold_seats_left += booking.tickets
                elif booking.ticket_type == 'standard':
                    event.standard_seats_left += booking.tickets
                
                event.save()
                
                # Add note to transaction
                instance.notes += f"\n\nPayment refunded. Seats restored: {booking.tickets} x {booking.get_ticket_type_display()}"
                
        except PaymentTransaction.DoesNotExist:
            pass


def send_confirmation_email_to_user(booking, event, payment_transaction):
    """
    Send confirmation email when admin approves payment
    """
    user = booking.user
    subject = f'✅ Payment Confirmed - {event.title}'
    
    message = f"""
Dear {user.get_full_name() or user.username},

GREAT NEWS! Your payment has been confirmed by our admin team.

BOOKING CONFIRMATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Booking Reference: #{booking.id:06d}
Transaction ID: {payment_transaction.transaction_id}
Status: ✅ CONFIRMED

EVENT DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
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
Payment Method: {payment_transaction.get_payment_method_display()}
Transaction ID: {payment_transaction.transaction_id}
Status: CONFIRMED ✓

IMPORTANT INFORMATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Your tickets are now confirmed and valid
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

Thank you for choosing Nalisa Events!
We look forward to seeing you at the event.

Best regards,
The Nalisa Events Team

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
This is an automated confirmation email. Please do not reply.
Visit us at: http://127.0.0.1:8000/
    """
    
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=True,
    )
    
    print(f"✅ Confirmation email sent to {user.email} for booking #{booking.id:06d}")
