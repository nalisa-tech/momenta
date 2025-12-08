# 📧 Setup Gmail for tygayt625@gmail.com

## 🎯 Goal: Enable Real Email Sending

I've configured the system to use **tygayt625@gmail.com** for sending booking confirmations to users.

## 📋 Required Steps (5 minutes)

### Step 1: Enable 2-Step Verification
1. **Login to Gmail**: Go to https://gmail.com with tygayt625@gmail.com
2. **Go to Security**: https://myaccount.google.com/security
3. **Find "2-Step Verification"** in the "Signing in to Google" section
4. **Click "2-Step Verification"** and follow setup if not already enabled
5. **Use phone number** for verification method

### Step 2: Generate App Password
1. **Go to App Passwords**: https://myaccount.google.com/apppasswords
   - (This link only works AFTER 2-Step Verification is enabled)
2. **Select "Mail"** from the dropdown
3. **Select "Other (Custom name)"** and type: **"Nalisa Events System"**
4. **Click "Generate"**
5. **Copy the 16-digit password** (example: `abcd efgh ijkl mnop`)

### Step 3: Update .env File
1. **Open `.env` file** in your project
2. **Find this line:**
   ```
   EMAIL_HOST_PASSWORD=YOUR_GMAIL_APP_PASSWORD_HERE
   ```
3. **Replace with your actual password (remove spaces):**
   ```
   EMAIL_HOST_PASSWORD=abcdefghijklmnop
   ```

### Step 4: Restart Server
```bash
# Stop current server (Ctrl+C in terminal)
# Then restart:
python manage.py runserver
```

## ✅ Test Email System

After setup, test with this command:
```bash
python manage.py shell
```

Then paste:
```python
from django.core.mail import send_mail
send_mail(
    'Test from Nalisa Events',
    'This is a test email from tygayt625@gmail.com',
    'tygayt625@gmail.com',
    ['nalisaimbula282@gmail.com'],  # Replace with your test email
    fail_silently=False,
)
print("✅ Test email sent successfully!")
```

## 🎉 What Happens After Setup

### For Users:
- ✅ **Real emails** sent to their inbox
- ✅ **Professional sender**: "Nalisa Events <tygayt625@gmail.com>"
- ✅ **Complete booking confirmations** with all details
- ✅ **No more console-only messages**

### Email Content Includes:
- Booking reference number
- Event details (date, time, location)
- Ticket information (type, quantity, price)
- Payment confirmation
- Contact information
- Professional formatting

## 🚨 Troubleshooting

### "App passwords" not showing?
- Make sure you're logged into tygayt625@gmail.com
- Ensure 2-Step Verification is fully enabled
- Wait 5-10 minutes after enabling 2-Step Verification
- Try refreshing the page

### Still getting errors?
- Double-check the App Password (16 characters, no spaces)
- Verify EMAIL_HOST_USER matches exactly: tygayt625@gmail.com
- Make sure Gmail account is not locked

### Quick verification:
- Login to https://gmail.com with tygayt625@gmail.com
- Check if account is working normally
- Verify 2-Step Verification is active

## 📞 Need Help?

If you get stuck:
- **Email**: nalisaimbula282@gmail.com
- **Phone**: 0978308101

## 🔐 Security Notes

- **App Password is safe**: It's designed for applications
- **Can be revoked**: Delete anytime from Google Account
- **Account stays secure**: 2-Step Verification protects main account
- **Only for this app**: Password only works for email sending

---

## ⚡ Quick Summary

1. **Enable 2-Step Verification** on tygayt625@gmail.com
2. **Generate App Password** at myaccount.google.com/apppasswords
3. **Update .env file** with the 16-digit password
4. **Restart server**: `python manage.py runserver`
5. **Test booking**: Users will receive real emails!

**After this setup, all booking confirmations will be sent to users' actual email addresses!**