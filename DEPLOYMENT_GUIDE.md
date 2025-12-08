# 🚀 Nalisa Events - Railway Deployment Guide

## ✅ **Pre-Deployment Checklist**

Your project is **READY FOR DEPLOYMENT**! All files have been prepared:

- ✅ `requirements.txt` - All dependencies listed
- ✅ `railway.json` - Railway deployment configuration
- ✅ `nixpacks.toml` - Build configuration
- ✅ `Procfile` - Process configuration
- ✅ `production_settings.py` - Production-ready settings
- ✅ `.env.example` - Environment variables template
- ✅ Static files configuration
- ✅ Database configuration (PostgreSQL ready)
- ✅ Security settings enabled

## 🚀 **Step-by-Step Deployment**

### **Step 1: Create Railway Account**
1. Go to [railway.app](https://railway.app)
2. Click **"Start a New Project"**
3. Sign up with **GitHub** (recommended)

### **Step 2: Deploy from GitHub**
1. **Connect Repository:**
   - Click **"Deploy from GitHub repo"**
   - Select your Nalisa Events repository
   - Click **"Deploy Now"**

2. **Railway will automatically:**
   - ✅ Detect it's a Django project
   - ✅ Install dependencies from `requirements.txt`
   - ✅ Set up PostgreSQL database
   - ✅ Run migrations
   - ✅ Collect static files

### **Step 3: Configure Environment Variables**
In Railway dashboard, go to **Variables** tab and add:

```env
SECRET_KEY=your-new-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app-name.railway.app
EMAIL_HOST_USER=nalisaimbula282@gmail.com
EMAIL_HOST_PASSWORD=rusmwqgnamxeorho
BANK_NAME=Standard Chartered Bank
BANK_ACCOUNT_NUMBER=0152516138300
BANK_ACCOUNT_NAME=Nalisa Events
```

**Generate a new SECRET_KEY:**
```python
# Run this in Python to generate a new secret key
import secrets
print(secrets.token_urlsafe(50))
```

### **Step 4: Custom Domain (Optional)**
1. In Railway dashboard, go to **Settings**
2. Click **"Domains"**
3. Add your custom domain (e.g., `nalisaevents.com`)
4. Update DNS records as instructed

### **Step 5: Final Steps**
1. **Test the deployment** - Visit your Railway URL
2. **Create superuser** - Use Railway's terminal:
   ```bash
   python manage.py createsuperuser
   ```
3. **Upload event data** - Add events through admin panel

## 🎯 **Your Deployment URLs**

- **Railway URL:** `https://your-app-name.railway.app`
- **Admin Panel:** `https://your-app-name.railway.app/admin/`
- **Custom Domain:** `https://yourdomain.com` (if configured)

## 🔧 **Post-Deployment Tasks**

### **1. Test All Features:**
- ✅ Homepage loads correctly
- ✅ Event browsing works
- ✅ User registration/login
- ✅ Booking system functional
- ✅ Payment system working
- ✅ Email notifications sending
- ✅ Admin panel accessible

### **2. Add Content:**
- ✅ Create event categories
- ✅ Add sample events
- ✅ Upload event images
- ✅ Add video galleries for music events
- ✅ Test booking flow

### **3. Configure Email:**
- ✅ Verify Gmail App Password works
- ✅ Test newsletter subscription
- ✅ Test booking confirmations
- ✅ Test payment notifications

## 🎉 **Success Indicators**

Your deployment is successful when:
- ✅ Website loads without errors
- ✅ Static files (CSS/JS) load correctly
- ✅ Images upload and display properly
- ✅ Database operations work
- ✅ Email system functional
- ✅ Admin panel accessible
- ✅ All buttons and navigation work

## 🆘 **Troubleshooting**

### **Common Issues:**

**1. Static Files Not Loading:**
```bash
# In Railway terminal:
python manage.py collectstatic --noinput
```

**2. Database Issues:**
```bash
# In Railway terminal:
python manage.py migrate
```

**3. Email Not Working:**
- Check Gmail App Password is correct
- Verify EMAIL_HOST_PASSWORD in Railway variables

**4. 500 Server Error:**
- Check Railway logs in dashboard
- Ensure DEBUG=False in production
- Verify all environment variables set

## 🎯 **Final Result**

Your **Nalisa Events** website will be live at:
- **Professional URL** with your branding
- **Fast loading** with Railway's CDN
- **Secure HTTPS** automatically enabled
- **PostgreSQL database** for reliability
- **Email notifications** working
- **Mobile responsive** design
- **Admin panel** for easy management

## 🚀 **Go Live!**

Your event management system is ready to serve users in Zambia and beyond! 🇿🇲✨