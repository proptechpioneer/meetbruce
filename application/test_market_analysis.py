#!/usr/bin/env python3
"""
Test the market analysis system with real data
"""
import os
import django
import sys

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
django.setup()

from market_analysis.models import PropertyListing, MarketAnalysis
from application.models import User
from decimal import Decimal

def test_market_analysis():
    """Test the market analysis functionality"""
    
    print("🔍 Testing Market Analysis System")
    print("=" * 50)
    
    # Check PropertyListing count
    total_properties = PropertyListing.objects.count()
    print(f"📊 Total properties in database: {total_properties}")
    
    # Show sample properties
    if total_properties > 0:
        print("\n🏠 Sample properties:")
        sample_properties = PropertyListing.objects.all()[:5]
        for prop in sample_properties:
            print(f"   • {prop.title[:50]}... - £{prop.weekly_rent}/week - {prop.bedrooms} bed - {prop.source}")
        
        print(f"\n💰 Rent range: £{PropertyListing.objects.aggregate(min_rent=django.db.models.Min('weekly_rent'), max_rent=django.db.models.Max('weekly_rent'))}")
    
    # Check for test users
    test_users = User.objects.filter(email__icontains='test')
    if test_users.exists():
        user = test_users.first()
        print(f"\n👤 Test user found: {user.email}")
        print(f"   Property: {user.property_type}, {user.bedrooms} bed in {user.town}")
        print(f"   Current rent: {user.weekly_rent}")
        
        # Find comparable properties for this user
        property_type = user.property_type.lower() if user.property_type else 'flat'
        from market_analysis.views import parse_bedrooms
        bedrooms = parse_bedrooms(user.bedrooms)
        location = user.town or 'london'
        
        comparables = PropertyListing.objects.filter(
            property_type=property_type,
            bedrooms=bedrooms,
            is_active=True,
            is_duplicate=False,
            weekly_rent__gt=0
        )
        
        print(f"\n🔍 Comparable properties for {property_type} with {bedrooms} bedrooms: {comparables.count()}")
        
        if comparables.exists():
            rent_values = [float(prop.weekly_rent) for prop in comparables]
            avg_rent = sum(rent_values) / len(rent_values)
            print(f"   Average rent: £{avg_rent:.0f}/week")
            print(f"   Range: £{min(rent_values):.0f} - £{max(rent_values):.0f}/week")
    else:
        print("\n⚠️  No test users found - create a test account to see market analysis")
    
    # Check existing analyses
    analysis_count = MarketAnalysis.objects.count()
    print(f"\n📈 Existing market analyses: {analysis_count}")
    
    if analysis_count > 0:
        latest = MarketAnalysis.objects.latest('created_at')
        print(f"   Latest analysis: {latest.search_area} - {latest.total_properties_found} properties")
        if latest.average_rent:
            print(f"   Average rent: £{latest.average_rent}/week")
    
    print("\n✅ Market Analysis System Test Complete!")
    print("🌐 Visit http://127.0.0.1:8000/reviews/ to test rent review")
    print("📊 Visit http://127.0.0.1:8000/market-analysis/ to test analysis")

if __name__ == "__main__":
    test_market_analysis()