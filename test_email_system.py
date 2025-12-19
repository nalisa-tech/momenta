#!/usr/bin/env python3
"""
Email System Test for Momenta
===================================

This script tests if your email configuration is working properly.
"""

import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_system.settings')
django.setup()

from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def test_basic_email():
    """Test basic email sending"""
    print("📧 Testing Basic Email...")
    
    try:
        send_mail(
            subject='🎉 Momenta - Email Test',
            message='This is a test email from your Momenta system. If you receive this, your email configuration is working perfectly!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['nalisaimbula282@gmail.com'],  # Send to yourself for testing
            fail_silently=False,
        )
        print("✅ Basic email sent successfully!")
        return True
    except Exception as e:
        print(f"❌ Basic email failed: {e}")
        return False

def test_html_email():
    """Test HTML email sending"""
    print("📧 Testing HTML Email...")
    
    try:
        html_content = """
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; text-align: center; color: white;">
                <h1>🎉 Momenta</h1>
                <p>Email System Test</p>
            </div>
            <div style="padding: 20px;">
                <h2>✅ Email Configuration Working!</h2>
                <p>Congratulations! Your Momenta email system is properly configured and working.</p>
                
                <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <h3>📊 System Information:</h3>
                    <ul>
                        <li><strong>Email Backend:</strong> Gmail SMTP</li>
                        <li><strong>From Address:</strong> nalisaimbula282@gmail.com</li>
                        <li><strong>Status:</strong> Active</li>
                    </ul>
                </div>
                
                <p>Your users will now receive:</p>
                <ul>
                    <li>✅ Booking confirmations</li>
                    <li>✅ Payment confirmations</li>
                    <li>✅ Event reminders</li>
                    <li>✅ Admin notifications</li>
                </ul>
                
                <div style="text-align: center; margin-top: 30px;">
                    <p style="color: #666;">This is an automated test email from Momenta System</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = strip_tags(html_content)
        
        email = EmailMessage(
            subject='🎉 Momenta - HTML Email Test',
            body=html_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=['nalisaimbula282@gmail.com'],
        )
        email.content_subtype = 'html'
        email.send()
        
        print("✅ HTML email sent successfully!")
        return True
    except Exception as e:
        print(f"❌ HTML email failed: {e}")
        return False

def check_email_settings():
    """Check current email configuration"""
    print("🔍 Checking Email Configuration...")
    print(f"📧 Email Backend: {settings.EMAIL_BACKEND}")
    print(f"📧 SMTP Host: {settings.EMAIL_HOST}")
    print(f"📧 SMTP Port: {settings.EMAIL_PORT}")
    print(f"📧 Use TLS: {settings.EMAIL_USE_TLS}")
    print(f"📧 Host User: {settings.EMAIL_HOST_USER}")
    print(f"📧 From Email: {settings.DEFAULT_FROM_EMAIL}")
    
    # Check if password is set
    password = getattr(settings, 'EMAIL_HOST_PASSWORD', '')
    if password:
        print(f"📧 Password: {'*' * len(password)} (Set)")
    else:
        print("📧 Password: Not set")
    
    return bool(password)

def main():
    print("🎯 Momenta - Email System Test")
    print("=" * 40)
    
    # Check configuration
    has_password = check_email_settings()
    
    if not has_password:
        print("\n❌ EMAIL_HOST_PASSWORD not set!")
        print("Run: python setup_gmail_app_password.py")
        return
    
    if 'console' in settings.EMAIL_BACKEND:
        print("\n⚠️  Email backend is in console mode")
        print("Emails will be printed to terminal, not sent")
        print("Set EMAIL_HOST_PASSWORD in .env to enable real sending")
        return
    
    print("\n" + "=" * 40)
    
    # Test emails
    basic_success = test_basic_email()
    html_success = test_html_email()
    
    print("\n" + "=" * 40)
    print("📊 TEST RESULTS:")
    print(f"Basic Email: {'✅ PASS' if basic_success else '❌ FAIL'}")
    print(f"HTML Email:  {'✅ PASS' if html_success else '❌ FAIL'}")
    
    if basic_success and html_success:
        print("\n🎉 ALL TESTS PASSED!")
        print("Your email system is ready for production!")
    else:
        print("\n❌ SOME TESTS FAILED")
        print("Check your Gmail App Password and internet connection")

if __name__ == "__main__":
    main()