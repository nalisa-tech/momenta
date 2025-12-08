#!/usr/bin/env python3
"""
Nalisa Events - Deployment Helper Script
=======================================

This script helps prepare your project for Railway deployment.
"""

import os
import secrets
import subprocess
import sys

def generate_secret_key():
    """Generate a secure secret key for production"""
    return secrets.token_urlsafe(50)

def check_requirements():
    """Check if all required files exist"""
    required_files = [
        'requirements.txt',
        'railway.json', 
        'nixpacks.toml',
        'Procfile',
        '.env.example',
        'manage.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    return missing_files

def main():
    print("🚀 Nalisa Events - Deployment Preparation")
    print("=" * 50)
    
    # Check if all required files exist
    missing_files = check_requirements()
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        print("\nPlease ensure all deployment files are created first.")
        return
    
    print("✅ All deployment files found!")
    
    # Generate new secret key
    new_secret_key = generate_secret_key()
    print(f"\n🔑 Generated new SECRET_KEY:")
    print(f"   {new_secret_key}")
    
    # Check Django project
    try:
        result = subprocess.run([sys.executable, 'manage.py', 'check'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Django project check passed!")
        else:
            print("⚠️  Django project has issues:")
            print(result.stderr)
    except Exception as e:
        print(f"❌ Error checking Django project: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 DEPLOYMENT READY!")
    print("=" * 50)
    
    print("\n📋 Next Steps:")
    print("1. Go to https://railway.app")
    print("2. Create account and connect GitHub")
    print("3. Deploy from your repository")
    print("4. Add environment variables:")
    print(f"   SECRET_KEY={new_secret_key}")
    print("   DEBUG=False")
    print("   ALLOWED_HOSTS=your-app-name.railway.app")
    print("   EMAIL_HOST_USER=nalisaimbula282@gmail.com")
    print("   EMAIL_HOST_PASSWORD=rusmwqgnamxeorho")
    
    print("\n🎉 Your Nalisa Events website will be live!")
    print("📖 See DEPLOYMENT_GUIDE.md for detailed instructions")

if __name__ == "__main__":
    main()