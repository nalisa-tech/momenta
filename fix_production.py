#!/usr/bin/env python3
"""
Quick fix for production database issue
Run this to immediately deploy the database migration fix
"""

import subprocess
import sys
import os

def run_cmd(cmd, description):
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - SUCCESS")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FAILED")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("🚨 FIXING PRODUCTION DATABASE ISSUE")
    print("=" * 40)
    
    print("The production app is showing: 'no such table: events_category'")
    print("This fix will deploy the database migration solution.\n")
    
    # Check git status
    print("📋 Checking git status...")
    if run_cmd("git status --porcelain", "Git status check"):
        # Add all changes
        if run_cmd("git add .", "Adding changes to git"):
            # Commit changes
            commit_msg = "🔧 Fix production database issue - add migrations to startup"
            if run_cmd(f'git commit -m "{commit_msg}"', "Committing changes"):
                # Push to repository
                if run_cmd("git push", "Pushing to repository"):
                    print("\n🎉 SUCCESS! Changes pushed to repository.")
                    print("\n📡 Railway will now automatically redeploy with the fix.")
                    print("⏱️  This will take 2-3 minutes.")
                    print("\n✅ After deployment, the database tables will be created automatically.")
                    print("🌐 Your app will be working at: https://momenta-production.up.railway.app")
                    return True
    
    print("\n❌ Deployment failed. Please check the errors above.")
    print("\n🔧 Manual steps:")
    print("1. git add .")
    print("2. git commit -m 'Fix production database issue'")
    print("3. git push")
    return False

if __name__ == "__main__":
    if main():
        print("\n🎯 The production issue will be resolved in 2-3 minutes!")
    else:
        print("\n⚠️  Please run the manual steps or check your git configuration.")
    
    sys.exit(0)