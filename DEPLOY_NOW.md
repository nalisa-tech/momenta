# 🚀 DEPLOY MOMENTA TO RAILWAY

## ✅ SYSTEM READY FOR DEPLOYMENT!

Your **Momenta** event management system with mobile money payments is ready to go live!

### 📱 Mobile Money Numbers Configured:
- **Airtel Money: 0978308101**
- **MTN Mobile Money: 0767675748** 
- **Zamtel Money: 0956183839**

---

## 🚀 QUICK DEPLOYMENT STEPS

### 1. Create Railway Account
- Go to **https://railway.app**
- Click **"Start a New Project"**
- Sign up with **GitHub**

### 2. Deploy Your Repository
- Click **"Deploy from GitHub repo"**
- Select your **Momenta** repository
- Click **"Deploy Now"**

### 3. Set Environment Variables
In Railway Dashboard → **Variables**, add these:

```
SECRET_KEY=NzNP5o7H8zUxXiL4EoAFFUTyErFY0F2Ep6HvnY0WBlalgaHl0kXtAs0Pt0nS58vYenQ
DEBUG=False
ALLOWED_HOSTS=your-app-name.railway.app
EMAIL_HOST_USER=nalisaimbula282@gmail.com
EMAIL_HOST_PASSWORD=rusmwqgnamxeorho
MTN_NUMBER=0767675748
AIRTEL_NUMBER=0978308101
ZAMTEL_NUMBER=0956183839
BANK_NAME=Standard Chartered Bank
BANK_ACCOUNT_NUMBER=0152516138300
BANK_ACCOUNT_NAME=Momenta
```

**Important:** Replace `your-app-name.railway.app` with your actual Railway URL!

### 4. Create Admin User
Once deployed, use Railway's terminal:
```bash
python manage.py createsuperuser
```

---

## 🎯 WHAT HAPPENS AFTER DEPLOYMENT

✅ **Users can book events**  
✅ **Mobile money numbers are displayed clearly**  
✅ **Payment instructions are shown**  
✅ **Email confirmations are sent**  
✅ **Admin can manage bookings**  

---

## 📱 MOBILE MONEY PAYMENT FLOW

1. **User selects event** → Clicks "Book Tickets"
2. **Chooses ticket type** → Proceeds to payment
3. **Selects payment method** → Sees mobile money number
4. **Sends money** → Gets booking confirmation
5. **Admin approves** → User gets final confirmation

---

## 🔧 POST-DEPLOYMENT TASKS

1. **Test the website** - Visit your Railway URL
2. **Add events** - Use admin panel to create events
3. **Test booking flow** - Make a test booking
4. **Verify mobile money numbers** - Check payment page displays correctly
5. **Test email system** - Confirm booking emails work

---

## 🎉 YOUR LIVE WEBSITE WILL HAVE:

- **Professional event listings**
- **Mobile-responsive design**
- **Secure payment system**
- **Mobile money integration**
- **Email notifications**
- **Admin management panel**
- **Fast loading with Railway CDN**
- **Automatic HTTPS security**

---

## 🆘 NEED HELP?

If you encounter issues:
1. Check Railway logs in the dashboard
2. Verify all environment variables are set
3. Ensure ALLOWED_HOSTS matches your Railway URL
4. Test locally first with `python manage.py runserver`

---

## 🚀 DEPLOY NOW!

Your Momenta system is ready to serve customers in Zambia! 🇿🇲

**Go to Railway.app and deploy your repository now!**