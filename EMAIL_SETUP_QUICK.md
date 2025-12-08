# 📧 Quick Email Setup Guide

## Problem: "Confirmation email could not be sent"

This happens because Gmail requires an App Password for security.

## 🔧 Quick Fix (2 Options)

### Option 1: Use Console Email (Temporary - for testing)

1. Open `event_system/settings.py`
2. Find the email settings section
3. Comment out the SMTP backend and use console:

```python
# For testing - emails print to console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Comment out SMTP settings temporarily:
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
# EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
# EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
# EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'nalisaimbula282@gmail.com')
# EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
```

4. Restart server: `python manage.py runserver`
5. Now emails will print to your console/terminal instead of sending

### Option 2: Setup Gmail App Password (Permanent solution)

#### Step 1: Enable 2-Step Verification
1. Go to: https://myaccount.google.com/security
2. Click "2-Step Verification"
3. Follow setup instructions

#### Step 2: Generate App Password
1. Go to: https://myaccount.google.com/apppasswords
2. Select "Mail" and your device
3. Click "Generate"
4. Copy the 16-digit password (example: abcd efgh ijkl mnop)

#### Step 3: Update .env File
1. Open `.env` file
2. Replace `YOUR_16_DIGIT_APP_PASSWORD_HERE` with your actual password
3. Remove spaces: `abcdefghijklmnop`

```env
EMAIL_HOST_PASSWORD=abcdefghijklmnop
```

#### Step 4: Restart Server
```bash
python manage.py runserver
```

## ✅ Test Email

1. Make a booking
2. Check if you receive confirmation email
3. If using console backend, check terminal output

## 🚨 Troubleshooting

### Still not working?
- Double-check Gmail App Password (16 digits, no spaces)
- Verify 2-Step Verification is enabled
- Make sure EMAIL_HOST_USER matches your Gmail address

### Quick test command:
```bash
python manage.py shell
```

Then:
```python
from django.core.mail import send_mail
send_mail('Test', 'This is a test email', 'nalisaimbula282@gmail.com', ['your-email@gmail.com'])
```

## 📞 Need Help?
Contact: nalisaimbula282@gmail.com | 0978308101