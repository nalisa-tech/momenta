# 🚀 PythonAnywhere Deployment Guide

## 📋 **Pre-Deployment Setup**

### **Step 1: Create PythonAnywhere Account**
1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Sign up for a free account
3. Choose a username (this will be part of your URL)

### **Step 2: Upload Your Code**
1. **Option A: Git Clone (Recommended)**
   ```bash
   git clone https://github.com/nalisa-tech/momenta.git
   cd momenta
   ```

2. **Option B: Upload Files**
   - Use the Files tab in PythonAnywhere dashboard
   - Upload your project files

## 🔧 **Configuration Steps**

### **Step 3: Set Up Virtual Environment**
```bash
# In PythonAnywhere Bash console
mkvirtualenv --python=/usr/bin/python3.10 momenta
pip install -r requirements.txt
```

### **Step 4: Configure Database**
```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic
```

### **Step 5: Configure Web App**
1. Go to **Web** tab in PythonAnywhere dashboard
2. Click **"Add a new web app"**
3. Choose **"Manual configuration"**
4. Select **Python 3.10**

### **Step 6: Update WSGI Configuration**
1. In the **Web** tab, click on the WSGI configuration file
2. Replace the contents with the code from `pythonanywhere_wsgi.py`
3. Update the path to match your project location

### **Step 7: Set Static Files**
In the **Web** tab, add these static file mappings:
- **URL**: `/static/`
- **Directory**: `/home/yourusername/momenta/staticfiles/`

- **URL**: `/media/`
- **Directory**: `/home/yourusername/momenta/media/`

## 🌐 **Your Website URLs**

After deployment, your website will be available at:
- **Main Site**: `https://yourusername.pythonanywhere.com/`
- **Admin Panel**: `https://yourusername.pythonanywhere.com/admin/`

## 🔐 **Environment Variables**

Create a `.env` file in your project directory with:
```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourusername.pythonanywhere.com
EMAIL_HOST_USER=nalisaimbula282@gmail.com
EMAIL_HOST_PASSWORD=rusmwqgnamxeorho
```

## 🔄 **Updating Your Site**

To update your deployed site:
```bash
# Pull latest changes
git pull origin main

# Install any new requirements
pip install -r requirements.txt

# Run migrations if needed
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Reload web app (in Web tab, click "Reload")
```

## 🐛 **Troubleshooting**

### **Common Issues:**

1. **500 Server Error**
   - Check error logs in Web tab
   - Ensure DEBUG=False in production
   - Verify all paths are correct

2. **Static Files Not Loading**
   - Run `python manage.py collectstatic`
   - Check static file mappings in Web tab

3. **Database Issues**
   - Run `python manage.py migrate`
   - Check database file permissions

4. **Import Errors**
   - Ensure virtual environment is activated
   - Check all requirements are installed

## 📞 **Support**

- PythonAnywhere Help: [help.pythonanywhere.com](https://help.pythonanywhere.com)
- Django Documentation: [docs.djangoproject.com](https://docs.djangoproject.com)

---

**Your Momenta Events website will be live at**: `https://yourusername.pythonanywhere.com/`