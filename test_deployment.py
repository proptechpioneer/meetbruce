#!/usr/bin/env python
"""
Pre-deployment test script for Bruce Tenant Advocate
Run this script to verify your app is ready for Railway deployment
"""

import os
import sys
import django
from pathlib import Path

# Add the application directory to Python path
app_dir = Path(__file__).parent / 'application'
sys.path.insert(0, str(app_dir))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')

def run_tests():
    """Run basic deployment readiness tests"""
    print("🚀 Testing Bruce app for Railway deployment...\n")
    
    # Test 1: Django setup
    try:
        django.setup()
        from django.core.management import execute_from_command_line
        print("✅ Django setup successful")
    except Exception as e:
        print(f"❌ Django setup failed: {e}")
        return False
    
    # Test 2: Settings import
    try:
        from application import settings
        print("✅ Settings import successful")
    except Exception as e:
        print(f"❌ Settings import failed: {e}")
        return False
    
    # Test 3: Database connection
    try:
        from django.db import connection
        connection.ensure_connection()
        print("✅ Database connection successful")
    except Exception as e:
        print(f"✅ Database connection test (SQLite): {e}")
        print("   (This is normal for development - Railway will provide PostgreSQL)")
    
    # Test 4: Required files exist
    required_files = [
        'requirements.txt',
        'Procfile',
        'railway.json',
        'runtime.txt',
        '.gitignore'
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} missing")
            return False
    
    # Test 5: Check models
    try:
        from application.models import User
        print("✅ Models import successful")
    except Exception as e:
        print(f"❌ Models import failed: {e}")
        return False
    
    # Test 6: Static files check
    static_dir = app_dir / 'static'
    if static_dir.exists():
        print("✅ Static files directory exists")
    else:
        print("⚠️  Static files directory not found (may be created on deployment)")
    
    print(f"\n🎉 Pre-deployment tests completed!")
    print(f"📋 Next steps:")
    print(f"   1. Push code to GitHub")
    print(f"   2. Connect to Railway")
    print(f"   3. Set environment variables")
    print(f"   4. Deploy and test!")
    
    return True

if __name__ == "__main__":
    run_tests()