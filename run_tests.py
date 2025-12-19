#!/usr/bin/env python
"""
Django Test Runner for Momenta Event Management System
Run comprehensive tests for all components
"""

import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_system.settings')
    django.setup()
    
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    
    print("🧪 Running Django Tests for Momenta Event Management System")
    print("=" * 60)
    
    # Run tests by individual modules to avoid discovery issues
    test_modules = [
        "events.tests.test_models",
        "events.tests.test_views", 
        "events.tests.test_forms",
        "events.tests.test_integration"
    ]
    
    total_failures = 0
    
    for module in test_modules:
        print(f"\n📋 Running {module}...")
        try:
            failures = test_runner.run_tests([module])
            total_failures += failures
            if failures == 0:
                print(f"✅ {module} - All tests passed!")
            else:
                print(f"❌ {module} - {failures} test(s) failed!")
        except Exception as e:
            print(f"⚠️ {module} - Error running tests: {e}")
            total_failures += 1
    
    print("\n" + "=" * 60)
    if total_failures == 0:
        print("🎉 ALL TESTS PASSED SUCCESSFULLY!")
        print("✅ Django Test Framework implementation complete!")
        sys.exit(0)
    else:
        print(f"❌ {total_failures} test(s) failed across all modules!")
        sys.exit(1)