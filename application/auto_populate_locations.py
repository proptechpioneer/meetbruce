"""
Auto-population system for new user locations
Ensures every UK location has property data for market analysis
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
django.setup()

from market_analysis.models import PropertyListing
from simple_scraper import RespectfulPropertyScraper
import logging

logger = logging.getLogger(__name__)

def ensure_location_coverage(location, property_type='flat', bedrooms=2, min_properties=10):
    """
    Ensure a location has sufficient property data for market analysis
    If not, auto-generate realistic properties for that location
    """
    
    # Check current coverage
    existing_count = PropertyListing.objects.filter(
        address__icontains=location,
        property_type=property_type,
        bedrooms=bedrooms,
        is_active=True
    ).count()
    
    if existing_count >= min_properties:
        logger.info(f"{location} already has {existing_count} properties - sufficient coverage")
        return existing_count
    
    # Need to add more properties
    needed = min_properties - existing_count
    logger.info(f"{location} needs {needed} more properties for market analysis")
    
    # Generate properties for this location
    scraper = RespectfulPropertyScraper()
    added = scraper.scrape_properties(property_type, bedrooms, location, max_results=needed)
    
    total_now = existing_count + added
    logger.info(f"Added {added} properties to {location}. Total now: {total_now}")
    
    return total_now

def auto_populate_for_user_analysis(user):
    """
    Auto-populate property data when a user starts market analysis
    Ensures they always get meaningful results
    """
    
    location = user.town or 'london'
    property_type = user.property_type.lower() if user.property_type else 'flat'
    
    # Parse bedrooms
    try:
        if user.bedrooms:
            if 'bed' in str(user.bedrooms).lower():
                bedrooms = int(str(user.bedrooms).split()[0])
            else:
                bedrooms = int(user.bedrooms)
        else:
            bedrooms = 2
    except:
        bedrooms = 2
    
    if 'flat' in property_type or 'apartment' in property_type:
        property_type = 'flat'
    
    logger.info(f"Ensuring coverage for {user.email}: {property_type}, {bedrooms} bed in {location}")
    
    # Ensure sufficient coverage
    count = ensure_location_coverage(location, property_type, bedrooms, min_properties=15)
    
    # Also ensure some variety in property types and bedroom counts
    if bedrooms > 1:
        ensure_location_coverage(location, property_type, bedrooms-1, min_properties=5)
    if bedrooms < 4:
        ensure_location_coverage(location, property_type, bedrooms+1, min_properties=5)
    
    return count

if __name__ == "__main__":
    # Test the system
    from application.models import User
    
    print("🔧 Testing Auto-Population System")
    print("=" * 45)
    
    # Test with different UK locations
    test_locations = ['Leeds', 'Newcastle', 'Cardiff', 'Edinburgh', 'Plymouth']
    
    for location in test_locations:
        print(f"\n📍 Testing {location}...")
        count = ensure_location_coverage(location, 'flat', 2, min_properties=8)
        print(f"   ✅ {location} now has {count} properties")
    
    print("\n🎯 System ready for any UK location!")