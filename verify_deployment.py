#!/usr/bin/env python3
"""
Deployment Verification Script
Verifies that the production deployment is working correctly
"""

import requests
import sys
import time

def test_url(url, expected_status=200, expected_content=None):
    """Test a URL and return success status"""
    try:
        print(f"🔍 Testing: {url}")
        response = requests.get(url, timeout=10)
        
        if response.status_code == expected_status:
            print(f"✅ Status: {response.status_code}")
            
            if expected_content:
                if expected_content in response.text:
                    print(f"✅ Content: Found '{expected_content}'")
                    return True
                else:
                    print(f"❌ Content: Missing '{expected_content}'")
                    return False
            return True
        else:
            print(f"❌ Status: {response.status_code} (expected {expected_status})")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run deployment verification tests"""
    print("🚀 MOMENTA DEPLOYMENT VERIFICATION")
    print("=" * 50)
    
    base_url = "https://momenta-production.up.railway.app"
    
    # Test cases
    tests = [
        {
            "url": f"{base_url}/",
            "expected_content": "Zambia's #1 Event Platform",
            "description": "Homepage"
        },
        {
            "url": f"{base_url}/categories/",
            "expected_content": "Event Categories",
            "description": "Categories page"
        },
        {
            "url": f"{base_url}/events/",
            "expected_content": "Browse Events",
            "description": "Events list"
        },
        {
            "url": f"{base_url}/login/",
            "expected_content": "Login",
            "description": "Login page"
        },
        {
            "url": f"{base_url}/admin/",
            "expected_content": "Django administration",
            "description": "Admin panel"
        }
    ]
    
    print(f"🌐 Testing deployment at: {base_url}")
    print("⏱️  Please wait while we verify all endpoints...\n")
    
    results = []
    for i, test in enumerate(tests, 1):
        print(f"📋 Test {i}/{len(tests)}: {test['description']}")
        success = test_url(
            test["url"], 
            expected_content=test["expected_content"]
        )
        results.append(success)
        print()
        
        # Small delay between tests
        time.sleep(1)
    
    # Summary
    print("=" * 50)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"🎉 ALL TESTS PASSED ({passed}/{total})")
        print("✅ Deployment is successful and fully functional!")
        print("\n🔗 Your app is live at:")
        print(f"   {base_url}")
        print("\n🔐 Admin access:")
        print(f"   {base_url}/admin/")
        print("   Username: admin")
        print("   Password: admin123")
        print("\n⚠️  Remember to change the admin password!")
        return True
    else:
        print(f"❌ {passed}/{total} tests passed")
        print("🔧 Some endpoints may still be deploying or have issues")
        print("⏱️  Try again in a few minutes if deployment just completed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)