# 📧 Email Setup Guide

## How to Enable Real Email Notifications

Your system is configured to send booking confirmation emails, but you need to set up Gmail App Password first.

## 🔐 Step-by-Step Gmail Setup

### Step 1: Enable 2-Factor Authentication

1. Go to your Google Account: https://myaccount.google.com/security
2. Click on "2-Step Verification"
3. Follow the prompts to enable it (you'll need your phone)
4. Complete the setup

### Step 2: Generate App Password

1. Go to: https://myaccount.google.com/apppasswords
2. You might need to sign in again
3. In the "Select app" dropdown, choose **"Mail"**
4. In the "Select device" dropdown, choose **"Windows Computer"** or **"Other"**
5. Click **"Generate"**
6. You'll see a 16-digit password like: `abcd efgh ijkl mnop`
7. **Copy this password** (remove spaces: `abcdefghijklmnop`)

### Step 3: Update Django Settings

1. Open `event_system/settings.py`
2. Find this line:
   ```python
   EMAIL_HOST_PASSWORD = 'YOUR_16_DIGIT_APP_PASSWORD'
   ```
3. Replace `YOUR_16_DIGIT_APP_PASSWORD` with your generated app password:
   ```python
   EMAIL_HOST_PASSWORD = 'abcdefghijklmnop'
   ```
4. Save the file
5. Restart your Django server

### Step 4: Test It!

1. Make a test booking
2. Complete the payment
3. Check your email inbox (nalisaimbula282@gmail.com)
4. You should receive a confirmation email!

## 📧 Email Content

Users will receive an email with:
- ✅ Booking reference number
- ✅ Event details (title, date, time, location)
- ✅ Ticket information (type, quantity, price)
- ✅ Payment confirmation
- ✅ Organizer contact information
- ✅ Important instructions for event day

## 🔧 Alternative Email Providers

### Using Outlook/Hotmail
```python
EMAIL_HOST = 'smtp-mail.outlook.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@outlook.com'
EMAIL_HOST_PASSWORD = 'your-password'
```

### Using Yahoo Mail
```python
EMAIL_HOST = 'smtp.mail.yahoo.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@yahoo.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

### Using Custom SMTP Server
```python
EMAIL_HOST = 'mail.yourdomain.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'noreply@yourdomain.com'
EMAIL_HOST_PASSWORD = 'your-password'
```

## 🧪 Testing Email Configuration

Test if email is working:

```bash
python manage.py shell
```

Then run:
```python
from django.core.mail import send_mail

send_mail(
    'Test Email',
    'This is a test email from Nalisa Events.',
    'nalisaimbula282@gmail.com',
    ['nalisaimbula282@gmail.com'],
    fail_silently=False,
)
```

If you see "1" returned, the email was sent successfully!

## ⚠️ Common Issues

### "SMTPAuthenticationError"
**Problem**: Wrong email or password  
**Solution**: 
- Make sure you're using App Password, not your regular Gmail password
- Verify 2-Factor Authentication is enabled
- Generate a new App Password

### "SMTPServerDisconnected"
**Problem**: Connection issues  
**Solution**:
- Check your internet connection
- Verify EMAIL_HOST and EMAIL_PORT are correct
- Try EMAIL_PORT = 465 with EMAIL_USE_SSL = True instead of TLS

### "Connection refused"
**Problem**: Firewall or network blocking SMTP  
**Solution**:
- Check firewall settings
- Try different network
- Contact your ISP if port 587 is blocked

### Emails going to Spam
**Problem**: Gmail marking emails as spam  
**Solution**:
- Add sender to contacts
- Mark as "Not Spam"
- Set up SPF/DKIM records (for production)

## 🔒 Security Best Practices

### For Development
- Use App Password, never your main Gmail password
- Don't commit passwords to Git
- Use environment variables

### For Production
1. **Use Environment Variables**:
   ```python
   import os
   EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')
   ```

2. **Create .env file**:
   ```
   EMAIL_PASSWORD=your-app-password-here
   ```

3. **Add to .gitignore**:
   ```
   .env
   ```

4. **Use python-decouple**:
   ```bash
   pip install python-decouple
   ```
   
   ```python
   from decouple import config
   EMAIL_HOST_PASSWORD = config('EMAIL_PASSWORD')
   ```

## 📱 Email on Mobile Devices

Once configured, emails will be sent to the user's registered email address. They can receive them on:
- ✅ Phone (Gmail app, Outlook app, etc.)
- ✅ Tablet
- ✅ Computer
- ✅ Any device with email access

The email is sent to whatever email address the user registered with!

## ✅ Quick Setup Checklist

- [ ] Enable 2-Factor Authentication on Gmail
- [ ] Generate Gmail App Password
- [ ] Update EMAIL_HOST_PASSWORD in settings.py
- [ ] Restart Django server
- [ ] Make a test booking
- [ ] Check email inbox
- [ ] Verify email received

## 📞 Need Help?

If you're having trouble setting up email:
- Email: nalisaimbula282@gmail.com
- Phone: 0978308101

---

**Once configured, all booking confirmations will be sent to users' email addresses automatically! 📧**
