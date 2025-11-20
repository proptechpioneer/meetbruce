#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
django.setup()

from market_analysis.models import PropertyListing

def check_recent_salford_properties():
    print('Checking recent Salford properties for pricing accuracy...')
    
    recent_salford = PropertyListing.objects.filter(
        address__icontains='Salford'
    ).order_by('-scraped_at')[:10]
    
    print(f'Recent Salford properties:')
    for prop in recent_salford:
        print(f'  - {prop.area}, Salford | £{prop.weekly_rent}/week | {prop.bedrooms} bed {prop.property_type} | Postcode: {prop.postcode}')
    
    # Calculate average
    if recent_salford:
        avg_rent = sum(float(prop.weekly_rent) for prop in recent_salford) / len(recent_salford)
        print(f'\nAverage weekly rent: £{avg_rent:.2f}')
    
    print('\n' + '='*50)
    print('Expected pricing for Manchester region:')
    print('  Base 2-bed flat: £300-500/week')
    print('  With 1.2x multiplier: £360-600/week')
    print('  Current average seems too high - may still have London pricing')

if __name__ == '__main__':
    check_recent_salford_properties()