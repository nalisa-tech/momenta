#!/usr/bin/env python3
"""
🚀 Momenta - Railway Deployment Script
Automated deployment to Railway.app with mobile money payment system
"""

import os
import sys
import subprocess
import secrets
from pathlib import Path

def print_header():
    print("=" * 60)
    print("🚀 MOMENTA - RAILWAY DEPLOYMENT")
    print("=" * 60)
    print("📱 Mobile Money Payment System Ready!")
    print("💳 Airtel: 0978308101 | MTN: 0767675748 | Zamtel: 0956183839")
    print("=" * 60)

def check_requirements():
    """Check if all required files exist"""
    print("\n🔍 Checking deployment requirements...")
    
    required_files = [
        'requirements.txt',
        'railway.json', 
        'nixpacks.toml',
        'Procfile',
        'manage.py',
        '.env'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
        else:
            print(f"✅ {file}")
    
    if missing_files:
        print(f"\n❌ Missing files: {', '.join(missing_files)}")
        return False
    
    print("\n✅ All deployment files ready!")
    return True

def generate_secret_key():
    """Generate a new Django secret key"""
    return secrets.token_urlsafe(50)

def create_production_env():
    """Create production environment variables template"""
    print("\n📝 Creating production environment variables...")
    
    secret_key = generate_secret_key()
    
    prod_env = f"""# 🚀 PRODUCTION ENVIRONMENT VARIABLES FOR RAILWAY
# Copy these to Railway Dashboard > Variables

# Django Settings
SECRET_KEY={secret_key}
DEBUG=False
ALLOWED_HOSTS=your-app-name.railway.app

# Email Configuration (Gmail - nalisaimbula@gmail.com)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=nalisaimbula282@gmail.com
EMAIL_HOST_PASSWORD=rusmwqgnamxeorho
DEFAULT_FROM_EMAIL=Momenta <nalisaimbula282@gmail.com>

# Mobile Money Numbers (Already configured in code)
MTN_NUMBER=0767675748
AIRTEL_NUMBER=0978308101
ZAMTEL_NUMBER=0956183839

# Bank Transfer Details
BANK_NAME=Standard Chartered Bank
BANK_ACCOUNT_NUMBER=0152516138300
BANK_ACCOUNT_NAME=Momenta

# SMS Gateway (Optional)
SMS_API_KEY=
SMS_SENDER_ID=MOMENTA
"""
    
    with open('.env.production', 'w', encoding='utf-8') as f:
        f.write(prod_env)
    
    print("✅ Created .env.production with new secret key")
    print("📋 Copy these variables to Railway Dashboard")

def run_pre_deployment_checks():
    """Run Django system checks"""
    print("\n🔧 Running pre-deployment checks...")
    
    try:
        result = subprocess.run([
            sys.executable, 'manage.py', 'check', '--deploy'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Django system check passed")
            return True
        else:
            print(f"❌ System check failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error running checks: {e}")
        return False

def collect_static_files():
    """Collect static files for production"""
    print("\n📦 Collecting static files...")
    
    try:
        result = subprocess.run([
            sys.executable, 'manage.py', 'collectstatic', '--noinput'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Static files collected successfully")
            return True
        else:
            print(f"❌ Static collection failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error collecting static files: {e}")
        return False

def print_deployment_instructions():
    """Print step-by-step deployment instructions"""
    print("\n" + "=" * 60)
    print("🚀 READY TO DEPLOY TO RAILWAY!")
    print("=" * 60)
    
    print("\n📋 DEPLOYMENT STEPS:")
    print("\n1️⃣ CREATE RAILWAY ACCOUNT:")
    print("   • Go to https://railway.app")
    print("   • Sign up with GitHub")
    
    print("\n2️⃣ DEPLOY FROM GITHUB:")
    print("   • Click 'Deploy from GitHub repo'")
    print("   • Select your Momenta repository")
    print("   • Click 'Deploy Now'")
    
    print("\n3️⃣ SET ENVIRONMENT VARIABLES:")
    print("   • Go to Railway Dashboard > Variables")
    print("   • Copy variables from .env.production file")
    print("   • Update ALLOWED_HOSTS with your Railway URL")
    
    print("\n4️⃣ VERIFY DEPLOYMENT:")
    print("   • Visit your Railway URL")
    print("   • Test mobile money payment display")
    print("   • Create admin user via Railway terminal")
    
    print("\n💳 MOBILE MONEY NUMBERS CONFIGURED:")
    print("   ✅ Airtel Money: 0978308101")
    print("   ✅ MTN Mobile Money: 0767675748") 
    print("   ✅ Zamtel Money: 0956183839")
    
    print("\n🎉 Your event management system will be live!")
    print("=" * 60)

def main():
    """Main deployment preparation function"""
    print_header()
    
    # Check if we're in the right directory
    if not Path('manage.py').exists():
        print("❌ Error: manage.py not found. Run this script from your Django project root.")
        sys.exit(1)
    
    # Run all checks
    if not check_requirements():
        print("❌ Deployment requirements not met. Please fix missing files.")
        sys.exit(1)
    
    # Generate production environment
    create_production_env()
    
    # Run Django checks
    if not run_pre_deployment_checks():
        print("⚠️  Warning: System checks failed. Review issues before deploying.")
    
    # Collect static files
    collect_static_files()
    
    # Print deployment instructions
    print_deployment_instructions()
    
    print("\n🚀 Ready to deploy! Follow the steps above.")

if __name__ == "__main__":
    main()