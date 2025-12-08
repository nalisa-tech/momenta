#!/usr/bin/env python3
"""
Simple Email Test - Direct SMTP without Django
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_direct_smtp():
    """Test direct SMTP connection to Gmail"""
    
    email_user = 'nalisaimbula282@gmail.com'
    email_password = os.getenv('EMAIL_HOST_PASSWORD', '')
    
    print(f"📧 Testing direct SMTP connection...")
    print(f"📧 Email: {email_user}")
    print(f"📧 Password: {'*' * len(email_password)} ({len(email_password)} chars)")
    
    if len(email_password) != 16:
        print("❌ Gmail App Password should be exactly 16 characters!")
        return False
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = email_user  # Send to yourself
        msg['Subject'] = "🎉 Momenta - Direct SMTP Test"
        
        body = """
        Hello!
        
        This is a test email sent directly via SMTP from your Momenta system.
        
        If you receive this email, your Gmail configuration is working perfectly!
        
        Best regards,
        Momenta System
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Connect to Gmail SMTP
        print("🔗 Connecting to Gmail SMTP...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Enable TLS
        
        print("🔐 Authenticating...")
        server.login(email_user, email_password)
        
        print("📤 Sending email...")
        text = msg.as_string()
        server.sendmail(email_user, email_user, text)
        server.quit()
        
        print("✅ Email sent successfully!")
        print(f"📬 Check your inbox: {email_user}")
        return True
        
    except Exception as e:
        print(f"❌ SMTP Error: {e}")
        return False

if __name__ == "__main__":
    print("🎯 Direct SMTP Test for Momenta")
    print("=" * 40)
    
    success = test_direct_smtp()
    
    if success:
        print("\n🎉 SUCCESS! Your Gmail configuration works!")
        print("The issue might be with Django's email backend.")
    else:
        print("\n❌ FAILED! Check your Gmail App Password.")
        print("Make sure you:")
        print("1. Enabled 2-Step Verification")
        print("2. Generated a 16-character App Password")
        print("3. Updated your .env file correctly")