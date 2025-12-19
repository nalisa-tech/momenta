# 🚀 URGENT: Fix Production Database Issue

## ❌ Current Problem
The production app is showing: `no such table: events_category`

This means the database migrations haven't been run on Railway.

## ✅ Solution Applied

### 1. Updated Dockerfile
- Added startup script that runs migrations before starting the server
- Ensures database is properly initialized

### 2. Created start.sh Script
- Runs `python manage.py migrate --noinput` 
- Creates admin superuser automatically
- Starts Gunicorn server

### 3. Updated nixpacks.toml
- Configured to use the startup script

## 🔧 Deploy the Fix

### Option 1: Automatic Deployment (Recommended)
If you have auto-deploy enabled on Railway:
1. Push these changes to your GitHub repository
2. Railway will automatically redeploy with the fixes
3. The startup script will run migrations automatically

### Option 2: Manual Railway CLI Deployment
```bash
# Install Railway CLI if not installed
npm install -g @railway/cli

# Login to Railway
railway login

# Deploy the updated code
railway up
```

### Option 3: Use the Deployment Script
```bash
python deploy_to_railway.py
```

## 🎯 What Will Happen After Deployment

1. **Database Setup**: Migrations will run automatically
2. **Admin User**: An admin user will be created (username: `admin`)
3. **Tables Created**: All necessary database tables will be created
4. **App Working**: The `/categories/` page and all other pages will work

## 🔐 Environment Variables to Set (Optional)

In Railway dashboard, you can set:
- `ADMIN_EMAIL`: Email for the admin user (default: admin@momenta.zm)
- `ADMIN_PASSWORD`: Password for admin user (default: admin123)
- `DJANGO_SECRET_KEY`: Your secret key (if not already set)

## 🚨 Immediate Action Required

**Push these changes to your repository NOW** to fix the production issue.

The error will be resolved once the new deployment runs the database migrations.

## 📞 Support

If you encounter any issues:
1. Check Railway deployment logs
2. Ensure all files are committed to git
3. Verify Railway has access to your repository

**Status**: Ready to deploy ✅