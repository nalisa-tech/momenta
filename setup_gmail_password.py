#!/usr/bin/env python3
"""
Gmail App Password Setup Helper for Nalisa Events
"""

import os
import sys

def setup_gmail_password():
    """Interactive setup for Gmail App Password"""
    
    print("🔧 Gmail App Password Setup for tygayt625@gmail.com")
    print("=" * 60)
    
    print("\n📋 Steps to complete:")
    print("1. Go to: https://myaccount.google.com/security")
    print("2. Enable 2-Step Verification (if not already enabled)")
    print("3. Go to: https://myaccount.google.com/apppasswords")
    print("4. Create App Password for 'Mail' → 'Nalisa Events'")
    print("5. Copy the 16-digit password")
    
    print("\n" + "=" * 60)
    
    # Get password from user
    password = input("📧 Enter your 16-digit Gmail App Password (or press Enter to skip): ").strip()
    
    if not password:
        print("\n⏭️  Skipping password setup.")
        print("📧 System will continue using console mode (safe fallback)")
        print("🔄 Run this script again when you have the App Password")
        return
    
    # Remove spaces and validate
    password = password.replace(" ", "")
    
    if len(password) != 16:
        print(f"\n❌ Invalid password length: {len(password)} characters")
        print("📧 Gmail App Passwords are exactly 16 characters")
        print("🔄 Please try again with the correct password")
        return
    
    # Update .env file
    try:
        # Read current .env
        env_path = '.env'
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                content = f.read()
            
            # Replace password line
            lines = content.split('\n')
            updated_lines = []
            
            for line in lines:
                if line.startswith('EMAIL_HOST_PASSWORD='):
                    updated_lines.append(f'EMAIL_HOST_PASSWORD={password}')
                    print(f"✅ Updated EMAIL_HOST_PASSWORD in .env")
                else:
                    updated_lines.append(line)
            
            # Write back to file
            with open(env_path, 'w') as f:
                f.write('\n'.join(updated_lines))
            
            print("\n🎉 Gmail App Password configured successfully!")
            print("📧 From: Nalisa Events <tygayt625@gmail.com>")
            print("🚀 Restart your server: python manage.py runserver")
            print("📬 Users will now receive real emails!")
            
        else:
            print("❌ .env file not found")
            print("📁 Make sure you're in the project directory")
            
    except Exception as e:
        print(f"❌ Error updating .env file: {e}")
        print("📝 Please manually update EMAIL_HOST_PASSWORD in .env file")

def test_email_setup():
    """Test the email configuration"""
    
    print("\n🧪 Testing email configuration...")
    
    try:
        # Import Django settings
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_system.settings')
        import django
        django.setup()
        
        from django.core.mail import send_mail
        from django.conf import settings
        
        print(f"📧 Email Backend: {settings.EMAIL_BACKEND}")
        print(f"📧 Email Host: {settings.EMAIL_HOST}")
        print(f"📧 Email User: {settings.EMAIL_HOST_USER}")
        print(f"📧 Password Set: {'Yes' if settings.EMAIL_HOST_PASSWORD else 'No'}")
        
        # Send test email
        send_mail(
            'Test Email from Nalisa Events',
            'This is a test email to verify Gmail setup is working.',
            settings.EMAIL_HOST_USER,
            ['nalisaimbula282@gmail.com'],
            fail_silently=False,
        )
        
        print("✅ Test email sent successfully!")
        
    except Exception as e:
        print(f"❌ Email test failed: {e}")
        print("🔧 Check your Gmail App Password and try again")

if __name__ == "__main__":
    print("🎯 Nalisa Events - Gmail Setup Helper")
    print("=" * 60)
    
    choice = input("\nChoose an option:\n1. Setup Gmail App Password\n2. Test email configuration\n3. Exit\n\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        setup_gmail_password()
    elif choice == "2":
        test_email_setup()
    elif choice == "3":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice. Please run the script again.")