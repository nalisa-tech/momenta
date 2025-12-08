# 🚀 Quick Start Guide

Get your Nalisa Event Management System running in 5 minutes!

## Prerequisites

- Python 3.8 or higher installed
- Internet connection (for downloading packages)

## Setup (Choose One Method)

### Method 1: Automated Setup (Windows) ⚡

Double-click `setup.bat` and follow the prompts. That's it!

### Method 2: Manual Setup (All Platforms) 📝

Open terminal/command prompt in the project folder and run:

```bash
# Step 1: Install dependencies
pip install -r requirement.txt

# Step 2: Setup database
python manage.py migrate

# Step 3: Add sample data (optional but recommended)
python manage.py populate_data

# Step 4: Create admin account
python manage.py createsuperuser
# Enter username, email, and password when prompted

# Step 5: Start server
python manage.py runserver
```

## Access the Application

Open your browser and visit:

- **Main Site**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## First Steps

### As a User:
1. Click "Sign Up" to create an account
2. Browse events on the homepage
3. Click "View Details" on any event
4. Click "BOOK TICKETS NOW"
5. Select ticket type and quantity
6. Complete payment

### As an Admin:
1. Go to http://127.0.0.1:8000/admin/
2. Login with superuser credentials
3. Click "Events" → "Add Event"
4. Fill in event details and save
5. View bookings in "Bookings" section

## Sample Data Included

After running `populate_data`, you'll have:
- 4 Categories (Music, Tech, Food, Business)
- 4 Sample Events with different dates and venues
- All events have VIP, Gold, and Standard seats

## Common Commands

```bash
# Start server
python manage.py runserver

# Create admin user
python manage.py createsuperuser

# Add sample data
python manage.py populate_data

# Check for issues
python manage.py check
```

## Need Help?

- **Full Documentation**: See `readme` file
- **Commands Reference**: See `COMMANDS.md`
- **Troubleshooting**: See `TROUBLESHOOTING.md`
- **Contact**: nalisaimbula282@gmail.com | 0978308101

## What's Next?

1. ✅ Explore the site and test booking flow
2. ✅ Add your own events via admin panel
3. ✅ Customize branding and colors
4. ✅ Upload event images
5. ✅ Share with users and start taking bookings!

---

**That's it! You're ready to go! 🎉**
