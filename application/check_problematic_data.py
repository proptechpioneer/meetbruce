#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
django.setup()

from market_analysis.models import PropertyListing

def check_problematic_data():
    print('Checking for Manchester properties with London areas...')
    manchester_props = PropertyListing.objects.filter(address__icontains='Manchester')
    
    london_areas = [
        'Westminster', 'Camden', 'Islington', 'Hackney', 'Tower Hamlets', 'Greenwich',
        'Lambeth', 'Southwark', 'Kensington', 'Chelsea', 'Fulham', 'Hammersmith',
        'Wandsworth', 'Battersea', 'Clapham', 'Putney', 'Richmond', 'Wimbledon',
        'Tooting', 'Streatham', 'Croydon', 'Ealing', 'Acton', 'Chiswick'
    ]
    
    problematic = []
    for prop in manchester_props:
        if any(area in prop.area for area in london_areas):
            problematic.append(prop)
    
    print(f'Found {len(problematic)} Manchester properties with London areas:')
    for i, prop in enumerate(problematic[:10]):  # Show first 10
        print(f'  {i+1}. {prop.address} - Area: {prop.area} - Rent: £{prop.weekly_rent}')
    
    if len(problematic) > 0:
        print(f'\nTotal problematic Manchester properties: {len(problematic)}')
        print('These should be deleted and regenerated with correct Manchester areas.')
    
    print('\nChecking Salford properties...')
    salford_props = PropertyListing.objects.filter(address__icontains='Salford')
    salford_with_london = []
    for prop in salford_props:
        if any(area in prop.area for area in london_areas):
            salford_with_london.append(prop)
    
    print(f'Found {len(salford_with_london)} Salford properties with London areas:')
    for i, prop in enumerate(salford_with_london[:5]):
        print(f'  {i+1}. {prop.address} - Area: {prop.area} - Rent: £{prop.weekly_rent}')

if __name__ == '__main__':
    check_problematic_data()