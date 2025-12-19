#!/usr/bin/env python
"""
Quick test to verify admin panel booking display is working
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_system.settings')
django.setup()

from events.models import Booking
from events.admin import BookingAdmin
from django.contrib.admin.sites import AdminSite

def test_booking_admin():
    """Test the booking admin display methods"""
    print("🧪 Testing BookingAdmin methods...")
    
    # Get a sample booking
    booking = Booking.objects.first()
    if not booking:
        print("❌ No bookings found to test")
        return
    
    # Create admin instance
    admin_site = AdminSite()
    booking_admin = BookingAdmin(Booking, admin_site)
    
    try:
        # Test the booking_id method that was causing the error
        booking_id_result = booking_admin.booking_id(booking)
        print(f"✅ booking_id method works: {booking_id_result}")
        
        # Test other display methods
        user_info_result = booking_admin.user_info(booking)
        print(f"✅ user_info method works")
        
        ticket_badge_result = booking_admin.ticket_badge(booking)
        print(f"✅ ticket_badge method works")
        
        price_display_result = booking_admin.price_display(booking)
        print(f"✅ price_display method works: {price_display_result}")
        
        print("\n🎉 All BookingAdmin display methods are working correctly!")
        print("✅ Admin panel should now work without errors")
        
    except Exception as e:
        print(f"❌ Error testing admin methods: {e}")
        return False
    
    return True

if __name__ == '__main__':
    test_booking_admin()