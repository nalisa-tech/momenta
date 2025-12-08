# 🚀 Temporary Email Solution

## Option 1: Use a Different Email Service (Immediate)

If Gmail setup is taking too long, you can use a simpler email service:

### Using Gmail with "Less Secure Apps" (Not Recommended)
This is easier but less secure:

1. Go to: https://myaccount.google.com/lesssecureapps
2. Turn ON "Allow less secure apps"
3. Update `.env`:
   ```
   EMAIL_HOST_PASSWORD=your-regular-gmail-password
   ```

**Warning:** This is less secure and Google may disable it.

### Using Outlook/Hotmail (Alternative)
1. Create a new Outlook account
2. Update `.env`:
   ```
   EMAIL_HOST=smtp-mail.outlook.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@outlook.com
   EMAIL_HOST_PASSWORD=your-outlook-password
   ```

## Option 2: Use SendGrid (Professional)

1. Sign up at: https://sendgrid.com (free tier: 100 emails/day)
2. Get API key
3. Install: `pip install sendgrid`
4. Update settings:
   ```python
   EMAIL_BACKEND = 'sendgrid_backend.SendgridBackend'
   SENDGRID_API_KEY = 'your-api-key'
   ```

## Option 3: Test Mode (For Development)

Keep console mode for now and add a note to users:

Update the success message in `events/views.py`:

```python
messages.success(request, f"Booking confirmed! Reference: #{booking.id:06d}. Confirmation details have been logged.")
```

## 🎯 Recommended: Stick with Gmail

Gmail is the most reliable option. The App Password setup takes 5 minutes and works perfectly.

Follow `GMAIL_SETUP_STEPS.md` for the proper solution.