#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
django.setup()

from application.models import User
from auto_populate_locations import auto_populate_for_user_analysis
from market_analysis.models import PropertyListing

def test_steve_analysis():
    # Find Steve's user account
    try:
        steve = User.objects.get(name__icontains='Steve')
        print(f'Found Steve: {steve.name} ({steve.email})')
        print(f'Location: {steve.town}')
        print(f'Property: {steve.property_type}, {steve.bedrooms} bedrooms')
        
        # Trigger auto-population for Steve's location
        print('\n🔧 Running auto-population for Steve\'s analysis...')
        properties_added = auto_populate_for_user_analysis(steve)
        print(f'Auto-population complete: {properties_added} properties ensured')
        
        # Check what properties now exist for Steve's location
        location = steve.town or 'Manchester'  # fallback
        property_type = steve.property_type or 'flat'
        bedrooms = steve.bedrooms or 2
        
        print(f'\n📊 Checking properties for: {bedrooms}-bed {property_type} in {location}')
        
        # Find matching properties (handle different property type formats)
        property_type_clean = 'flat' if 'flat' in property_type.lower() else property_type
        
        matching_props = PropertyListing.objects.filter(
            address__icontains=location,
            property_type__in=[property_type, property_type_clean, 'flat'],  # Try multiple formats
            bedrooms=bedrooms,
            is_active=True
        ).order_by('-scraped_at')[:10]
        
        print(f'Found {matching_props.count()} matching properties:')
        for i, prop in enumerate(matching_props):
            print(f'  {i+1}. {prop.address} - Area: {prop.area} - £{prop.weekly_rent}/week')
            
        # Calculate average rent
        if matching_props:
            avg_rent = sum(float(prop.weekly_rent) for prop in matching_props) / len(matching_props)
            print(f'\n💰 Average weekly rent: £{avg_rent:.2f}')
            print(f'Steve\'s current rent: £{steve.weekly_rent}' if steve.weekly_rent else 'Steve\'s rent: Not specified')
        
    except User.DoesNotExist:
        print('❌ Steve not found in database')
        # List available users
        users = User.objects.all()
        print(f'Available users ({users.count()}):')
        for user in users[:10]:
            print(f'  - {user.name} ({user.town})')

if __name__ == '__main__':
    test_steve_analysis()