#!/usr/bin/env python
"""
Test script for the new Scrapy-based property scraping system
"""

import os
import sys
import django
from pathlib import Path

# Add the Django project to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
django.setup()

from application.models import User
from market_analysis.scrapers import run_market_analysis_scraping
from market_analysis.models import PropertyListing

def test_scraping():
    """Test the scraping functionality"""
    
    print("🚀 Testing Bruce Property Scraping System")
    print("=" * 50)
    
    # Get test user
    try:
        user = User.objects.get(id=9)  # Ashley
        print(f"✅ Found user: {user.name}")
    except User.DoesNotExist:
        print("❌ Test user not found")
        return
    
    # Check initial property count
    initial_count = PropertyListing.objects.count()
    print(f"📊 Properties in database before scraping: {initial_count}")
    
    # Test scraping
    print(f"\n🔍 Starting scraping for {user.property_type} with {user.bedrooms} bedrooms in {user.town}")
    
    try:
        scraped_count = run_market_analysis_scraping(
            user=user,
            property_type=user.property_type.lower(),
            bedrooms=user.bedrooms,
            location=user.town.lower()
        )
        
        final_count = PropertyListing.objects.count()
        new_properties = final_count - initial_count
        
        print(f"✅ Scraping completed!")
        print(f"📈 Properties scraped: {scraped_count}")
        print(f"📊 Total properties now: {final_count}")
        print(f"🆕 New properties added: {new_properties}")
        
        # Show recent properties
        if new_properties > 0:
            print(f"\n🏠 Recently added properties:")
            recent_props = PropertyListing.objects.order_by('-scraped_at')[:5]
            for i, prop in enumerate(recent_props, 1):
                print(f"   {i}. {prop.title[:50]}... - £{prop.weekly_rent}/week")
        
    except Exception as e:
        print(f"❌ Scraping failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Test completed!")

if __name__ == "__main__":
    test_scraping()