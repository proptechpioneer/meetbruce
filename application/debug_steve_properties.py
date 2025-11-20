#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
django.setup()

from application.models import User
from market_analysis.models import PropertyListing

def debug_steve_properties():
    steve = User.objects.get(name__icontains='Steve')
    print(f'Steve details:')
    print(f'  Name: {steve.name}')
    print(f'  Town: {steve.town}')
    print(f'  Property type: "{steve.property_type}"')
    print(f'  Bedrooms: {steve.bedrooms}')
    print()
    
    # Check what properties exist in Salford
    salford_props = PropertyListing.objects.filter(address__icontains='Salford').order_by('-scraped_at')
    print(f'Total Salford properties: {salford_props.count()}')
    
    if salford_props.count() > 0:
        print('Recent Salford properties:')
        for prop in salford_props[:5]:
            print(f'  - {prop.address} | Area: {prop.area} | Type: "{prop.property_type}" | Beds: {prop.bedrooms} | £{prop.weekly_rent}/week')
        
        print('\nUnique property types in Salford:')
        unique_types = salford_props.values_list('property_type', flat=True).distinct()
        for ptype in unique_types:
            print(f'  - "{ptype}"')
        
        print('\nUnique bedroom counts in Salford:')
        unique_beds = salford_props.values_list('bedrooms', flat=True).distinct()
        for beds in unique_beds:
            print(f'  - {beds} bedrooms')

if __name__ == '__main__':
    debug_steve_properties()