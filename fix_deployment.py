#!/usr/bin/env python3
"""
Quick deployment fix for Railway
"""
import os
import subprocess
import sys

def run_command(cmd):
    """Run a command and return success status"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {cmd}")
            return True
        else:
            print(f"❌ {cmd}")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {cmd} - Exception: {e}")
        return False

def main():
    print("🔧 Fixing deployment issues...")
    
    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print("❌ Not in Django project directory")
        sys.exit(1)
    
    # Run basic checks
    checks = [
        "python manage.py check --deploy",
        "python manage.py collectstatic --noinput --dry-run",
        "python manage.py migrate --dry-run"
    ]
    
    all_passed = True
    for check in checks:
        if not run_command(check):
            all_passed = False
    
    if all_passed:
        print("✅ All deployment checks passed!")
        print("🚀 Ready for deployment")
    else:
        print("❌ Some checks failed - fix issues before deploying")
        sys.exit(1)

if __name__ == "__main__":
    main()