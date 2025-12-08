# 📧 Gmail App Password Setup - Step by Step

## 🎯 Goal: Send Real Emails to Users

Currently emails are not reaching users because Gmail requires an App Password for security.

## 📋 Step-by-Step Instructions

### Step 1: Enable 2-Step Verification

1. **Go to Google Account Security:**
   - Visit: https://myaccount.google.com/security
   - Login with: nalisaimbula282@gmail.com

2. **Find "2-Step Verification":**
   - Look for "Signing in to Google" section
   - Click "2-Step Verification"

3. **Enable it if not already enabled:**
   - Follow the setup wizard
   - Use your phone number for verification

### Step 2: Generate App Password

1. **Go to App Passwords:**
   - Visit: https://myaccount.google.com/apppasswords
   - (This only appears AFTER 2-Step Verification is enabled)

2. **Create New App Password:**
   - Select "Mail" from dropdown
   - Select "Other (Custom name)" 
   - Type: "Nalisa Events Django"
   - Click "Generate"

3. **Copy the 16-digit password:**
   - Example: `abcd efgh ijkl mnop`
   - **Important:** Copy it exactly, including spaces

### Step 3: Update Your .env File

1. **Open the `.env` file in your project**

2. **Find this line:**
   ```
   EMAIL_HOST_PASSWORD=YOUR_16_DIGIT_APP_PASSWORD_HERE
   ```

3. **Replace with your actual password (remove spaces):**
   ```
   EMAIL_HOST_PASSWORD=abcdefghijklmnop
   ```

### Step 4: Restart Server

```bash
# Stop current server (Ctrl+C)
# Then restart:
python manage.py runserver
```

### Step 5: Test Email

1. Make a booking on your website
2. User should receive actual email in their inbox
3. Check spam folder if not in inbox

## 🚨 Troubleshooting

### "App passwords" option not showing?
- Make sure 2-Step Verification is fully enabled
- Wait 5-10 minutes after enabling 2-Step Verification
- Try refreshing the page

### Still getting email errors?
- Double-check the App Password (16 characters, no spaces)
- Make sure EMAIL_HOST_USER matches your Gmail exactly
- Check if Gmail account is locked/suspended

### Quick Test Command:
```bash
python manage.py shell
```

Then paste:
```python
from django.core.mail import send_mail
send_mail(
    'Test from Nalisa Events',
    'This is a test email to verify Gmail setup.',
    'nalisaimbula282@gmail.com',
    ['your-test-email@gmail.com'],  # Replace with your email
    fail_silently=False,
)
print("Email sent successfully!")
```

## ✅ Success Indicators

When working correctly:
- No error messages in terminal
- Users receive emails in their inbox
- Booking confirmations arrive within 1-2 minutes

## 📞 Need Help?

If you're stuck on any step:
- Email: nalisaimbula282@gmail.com
- Phone: 0978308101

## 🔐 Security Note

- Never share your App Password
- App Passwords are specific to applications
- You can revoke/regenerate them anytime