#!/usr/bin/env python3
"""
Debug Nick's rent review issue
"""
import os
import django
import sys

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
django.setup()

from application.models import User
from market_analysis.models import PropertyListing, MarketAnalysis
from market_analysis.views import parse_bedrooms, create_market_analysis

def debug_nick_rent_review():
    """Debug Nick's rent review issues"""
    
    print("🔍 Debugging Nick's Rent Review")
    print("=" * 50)
    
    # Find Nick user
    try:
        nick_users = User.objects.filter(email__icontains='nick')
        if not nick_users.exists():
            print("❌ No user with 'nick' in email found")
            
            # Show all users
            all_users = User.objects.all().order_by('-id')[:10]
            print(f"\n👥 Found {User.objects.count()} total users:")
            for user in all_users:
                print(f"   • {user.email} (ID: {user.id})")
            return
        
        nick = nick_users.first()
        print(f"✅ Found Nick: {nick.email} (ID: {nick.id})")
        
        # Check Nick's property details
        print(f"\n🏠 Nick's Property Details:")
        print(f"   • Property Type: '{nick.property_type}' (type: {type(nick.property_type)})")
        print(f"   • Bedrooms: '{nick.bedrooms}' (type: {type(nick.bedrooms)})")
        print(f"   • Town: '{nick.town}' (type: {type(nick.town)})")
        print(f"   • Weekly Rent: '{nick.weekly_rent}' (type: {type(nick.weekly_rent)})")
        print(f"   • House/Flat Number: '{nick.house_flat_number}'")
        
        # Process Nick's data like the view does
        property_type = nick.property_type.lower() if nick.property_type else 'flat'
        bedrooms = parse_bedrooms(nick.bedrooms)
        location = nick.town or 'london'
        
        print(f"\n🔄 Processed for Market Analysis:")
        print(f"   • Property Type: '{property_type}'")
        print(f"   • Bedrooms: {bedrooms}")
        print(f"   • Location: '{location}'")
        
        # Check available properties in database
        total_properties = PropertyListing.objects.count()
        print(f"\n📊 Property Database Status:")
        print(f"   • Total properties: {total_properties}")
        
        if total_properties > 0:
            # Check for comparable properties
            comparable_properties = PropertyListing.objects.filter(
                property_type=property_type,
                bedrooms=bedrooms,
                is_active=True,
                is_duplicate=False,
                weekly_rent__gt=0
            )
            
            print(f"   • Comparable properties ({property_type}, {bedrooms} bed): {comparable_properties.count()}")
            
            # Show some samples
            if comparable_properties.exists():
                print(f"   • Sample comparables:")
                for prop in comparable_properties[:3]:
                    print(f"     - {prop.title[:40]}... £{prop.weekly_rent}/week in {prop.address}")
            
            # Check location-specific properties
            if location and location != 'london':
                location_props = PropertyListing.objects.filter(
                    address__icontains=location,
                    property_type=property_type,
                    bedrooms=bedrooms
                ).count()
                print(f"   • Properties in {location}: {location_props}")
        
        # Check for existing market analysis
        existing_analyses = MarketAnalysis.objects.filter(user=nick)
        print(f"\n📈 Existing Market Analyses:")
        if existing_analyses.exists():
            for analysis in existing_analyses:
                print(f"   • {analysis.created_at.strftime('%Y-%m-%d %H:%M')} - {analysis.total_properties_found} properties")
                print(f"     Average rent: £{analysis.average_rent}/week" if analysis.average_rent else "     No average rent calculated")
        else:
            print("   • No existing analyses found")
        
        # Try to create a market analysis
        print(f"\n🚀 Testing Market Analysis Creation:")
        try:
            analysis, comparable_props = create_market_analysis(nick, property_type, bedrooms, location)
            print(f"   ✅ Analysis created successfully!")
            print(f"   • Found {len(comparable_props)} comparable properties")
            if analysis.average_rent:
                print(f"   • Average rent: £{analysis.average_rent}/week")
        except Exception as e:
            print(f"   ❌ Error creating analysis: {e}")
            import traceback
            print(f"   Full error: {traceback.format_exc()}")
        
        # Check if we need to generate more property data
        if total_properties < 50:
            print(f"\n💡 Recommendation: Generate more property data")
            print(f"   Run: python simple_scraper.py to add more properties")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        print(f"Full traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    debug_nick_rent_review()