#!/usr/bin/env python3
"""
Railway Deployment Script for Momenta Event Management System
This script helps deploy the application to Railway with proper database setup.
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(f"Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("🚀 Momenta Railway Deployment Script")
    print("=" * 50)
    
    # Check if Railway CLI is installed
    if not run_command("railway --version", "Checking Railway CLI"):
        print("❌ Railway CLI not found. Please install it first:")
        print("   npm install -g @railway/cli")
        sys.exit(1)
    
    # Login to Railway (if not already logged in)
    print("\n📝 Please ensure you're logged into Railway:")
    print("   Run: railway login")
    
    # Deploy to Railway
    print("\n🚀 Deploying to Railway...")
    if run_command("railway up", "Deploying application"):
        print("\n🎉 Deployment initiated successfully!")
        print("\n📋 Next steps:")
        print("1. Check Railway dashboard for deployment status")
        print("2. Set environment variables if needed:")
        print("   - DJANGO_SECRET_KEY")
        print("   - DATABASE_URL (if using external DB)")
        print("   - ADMIN_EMAIL")
        print("   - ADMIN_PASSWORD")
        print("3. The app will automatically run migrations on startup")
        print("4. Access your app at the Railway-provided URL")
    else:
        print("❌ Deployment failed. Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()