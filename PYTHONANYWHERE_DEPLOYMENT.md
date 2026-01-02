# 🚀 PythonAnywhere Manual Deployment for Nalisa13

## 📋 **Your PythonAnywhere Details**
- **Username**: Nalisa13
- **Website URL**: https://Nalisa13.pythonanywhere.com/
- **Admin URL**: https://Nalisa13.pythonanywhere.com/admin/

## 🔧 **Step-by-Step Manual Setup**

### **Step 1: Upload Your Code**
1. Go to **Files** tab in PythonAnywhere dashboard
2. Navigate to `/home/Nalisa13/`
3. Create folder: `momenta`
4. Upload all your project files to `/home/Nalisa13/momenta/`

### **Step 2: Set Up Virtual Environment**
1. Go to **Consoles** tab
2. Start a **Bash console**
3. Run these commands:
```bash
cd /home/Nalisa13
mkvirtualenv --python=/usr/bin/python3.11 momenta
cd momenta
pip install -r requirements.txt
```

### **Step 3: Configure Database**
```bash
# Still in the Bash console
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### **Step 4: Create Web App**
1. Go to **Web** tab
2. Click **"Add a new web app"**
3. Choose **"Manual configuration"**
4. Select **Python 3.11**

### **Step 5: Configure WSGI File**
1. In **Web** tab, click on WSGI configuration file link
2. **Delete all existing content**
3. **Copy and paste** this exact code:

```python
# WSGI configuration for Nalisa13's Momenta Events
import os
import sys

# Add your project directory to the sys.path
path = '/home/Nalisa13/momenta'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'event_system.settings'

from django.core.wsgi import get_wsgi_application
from django.contrib.staticfiles.handlers import StaticFilesHandler

application = StaticFilesHandler(get_wsgi_application())
```

### **Step 6: Configure Static Files**
In the **Web** tab, scroll to **Static files** section and add:

**Static Files Mapping:**
- **URL**: `/static/`
- **Directory**: `/home/Nalisa13/momenta/staticfiles/`

**Media Files Mapping:**
- **URL**: `/media/`
- **Directory**: `/home/Nalisa13/momenta/media/`

### **Step 7: Set Virtual Environment**
In the **Web** tab, find **Virtualenv** section:
- **Path**: `/home/Nalisa13/.virtualenvs/momenta`

### **Step 8: Create Environment File**
1. Go to **Files** tab
2. Navigate to `/home/Nalisa13/momenta/`
3. Create new file: `.env`
4. Add this content:

```env
SECRET_KEY=(9nl9hazytjjz7fxy18zmy-uc**t7t^eqa2e(c=wcdjbz+%5d+)
DEBUG=False
ALLOWED_HOSTS=Nalisa13.pythonanywhere.com
EMAIL_HOST_USER=nalisaimbula282@gmail.com
EMAIL_HOST_PASSWORD=rusmwqgnamxeorho
MTN_NUMBER=0767675748
AIRTEL_NUMBER=0978308101
ZAMTEL_NUMBER=0956183839
BANK_NAME=Standard Chartered Bank
BANK_ACCOUNT_NUMBER=0152516138300
BANK_ACCOUNT_NAME=Momenta
```

### **Step 9: Reload Web App**
1. Go back to **Web** tab
2. Click the big green **"Reload Nalisa13.pythonanywhere.com"** button

## 🌐 **Your Live Website**

After completing all steps, your website will be live at:
- **Main Site**: https://Nalisa13.pythonanywhere.com/
- **Admin Panel**: https://Nalisa13.pythonanywhere.com/admin/

## 🔐 **Admin Login**
- **Username**: admin
- **Password**: admin123 (or whatever you set during createsuperuser)

## 🔄 **Updating Your Site**

To update your site later:
1. Upload new files via **Files** tab
2. Go to **Consoles** → **Bash**
3. Run:
```bash
cd /home/Nalisa13/momenta
python manage.py migrate
python manage.py collectstatic --noinput
```
4. **Reload** web app in **Web** tab

## 🐛 **Troubleshooting**

### **If you get errors:**
1. Check **Error log** in Web tab
2. Make sure all files are uploaded
3. Verify virtual environment path
4. Check WSGI configuration is correct

### **If static files don't load:**
1. Run `python manage.py collectstatic --noinput`
2. Check static files mapping in Web tab

### **If database errors:**
1. Run `python manage.py migrate`
2. Check file permissions

---

**Your Momenta Events website will be live at**: https://Nalisa13.pythonanywhere.com/