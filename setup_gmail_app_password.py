#!/usr/bin/env python3
"""
Gmail App Password Setup Helper for Nalisa Events
=================================================

This script helps you set up Gmail App Password for sending emails.
"""

import os
import re

def setup_gmail_app_password():
    print("🔧 Gmail App Password Setup for Nalisa Events")
    print("=" * 50)
    
    print("\n📋 STEP 1: Enable 2-Step Verification")
    print("1. Go to: https://myaccount.google.com/security")
    print("2. Find '2-Step Verification' and turn it ON")
    print("3. Follow Google's setup process")
    
    print("\n🔑 STEP 2: Generate App Password")
    print("1. Go to: https://myaccount.google.com/apppasswords")
    print("2. Select 'Mail' as the app")
    print("3. Select 'Other (Custom name)' as device")
    print("4. Enter: 'Nalisa Events System'")
    print("5. Click 'Generate'")
    print("6. Copy the 16-character password (format: xxxx xxxx xxxx xxxx)")
    
    print("\n💾 STEP 3: Enter Your App Password")
    while True:
        app_password = input("Enter your 16-character Gmail App Password (spaces will be removed): ").strip()
        
        # Remove spaces and validate
        app_password = re.sub(r'\s+', '', app_password)
        
        if len(app_password) == 16 and app_password.isalnum():
            break
        else:
            print("❌ Invalid format. App password should be 16 alphanumeric characters.")
            print("   Example: abcd efgh ijkl mnop (spaces will be removed)")
    
    # Update .env file
    env_path = '.env'
    
    # Read current .env content
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            content = f.read()
    else:
        content = ""
    
    # Update or add EMAIL_HOST_PASSWORD
    if 'EMAIL_HOST_PASSWORD=' in content:
        # Replace existing
        content = re.sub(r'EMAIL_HOST_PASSWORD=.*', f'EMAIL_HOST_PASSWORD={app_password}', content)
    else:
        # Add new line
        if not content.endswith('\n'):
            content += '\n'
        content += f'EMAIL_HOST_PASSWORD={app_password}\n'
    
    # Write back to .env
    with open(env_path, 'w') as f:
        f.write(content)
    
    print(f"\n✅ SUCCESS! Gmail App Password saved to {env_path}")
    print("\n🔄 STEP 4: Restart Django Server")
    print("1. Stop your Django server (Ctrl+C)")
    print("2. Start it again: python manage.py runserver")
    print("3. The system will now send real emails!")
    
    print("\n📧 STEP 5: Test Email Sending")
    print("You can test by:")
    print("1. Making a booking on your website")
    print("2. Approving a payment in admin")
    print("3. Check the user's email inbox")
    
    print("\n🔒 SECURITY NOTES:")
    print("- Keep your App Password secret")
    print("- Never share your .env file")
    print("- You can revoke the App Password anytime from Google Account settings")

if __name__ == "__main__":
    setup_gmail_app_password()