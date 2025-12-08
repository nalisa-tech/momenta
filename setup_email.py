#!/usr/bin/env python3
"""
Email setup script for Nalisa Events
Creates a working email configuration
"""

import os
import sys

def setup_email():
    """Setup email configuration"""
    
    print("🔧 Setting up email configuration...")
    
    # Update .env file with working email settings
    env_content = """# Django Settings
SECRET_KEY=(9nl9hazytjjz7fxy18zmy-uc**t7t^eqa2e(c=wcdjbz+%5d+)
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,*

# Email Configuration (Working Outlook setup)
EMAIL_HOST=smtp-mail.outlook.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=nalisaevents2025@outlook.com
EMAIL_HOST_PASSWORD=NalisaEvents2025!
DEFAULT_FROM_EMAIL=Nalisa Events <nalisaevents2025@outlook.com>

# Payment Gateway API Keys
MTN_API_KEY=
MTN_API_SECRET=
AIRTEL_API_KEY=
AIRTEL_API_SECRET=
ZAMTEL_API_KEY=
ZAMTEL_API_SECRET=

# SMS Gateway (Optional)
SMS_API_KEY=
SMS_SENDER_ID=NALISA
"""
    
    # Write to .env file
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Email configuration updated!")
    print("📧 Using: nalisaevents2025@outlook.com")
    print("🚀 Restart your server: python manage.py runserver")
    print("📬 Users will now receive real emails!")

if __name__ == "__main__":
    setup_email()