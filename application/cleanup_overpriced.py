#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
django.setup()

from market_analysis.models import PropertyListing

def cleanup_high_priced_manchester_salford():
    print('Cleaning up overpriced Manchester/Salford properties...')
    
    # Find Manchester properties with unrealistically high pricing (over £600/week)
    manchester_overpriced = PropertyListing.objects.filter(
        address__icontains='Manchester',
        weekly_rent__gt=600
    )
    
    # Find Salford properties with unrealistically high pricing (over £550/week)
    salford_overpriced = PropertyListing.objects.filter(
        address__icontains='Salford', 
        weekly_rent__gt=550
    )
    
    print(f'Found {manchester_overpriced.count()} overpriced Manchester properties (>£600/week)')
    print(f'Found {salford_overpriced.count()} overpriced Salford properties (>£550/week)')
    
    # Show some examples
    print('\nExample overpriced Manchester properties:')
    for prop in manchester_overpriced[:3]:
        print(f'  - {prop.address} | £{prop.weekly_rent}/week | {prop.bedrooms} bed')
    
    print('\nExample overpriced Salford properties:')
    for prop in salford_overpriced[:3]:
        print(f'  - {prop.address} | £{prop.weekly_rent}/week | {prop.bedrooms} bed')
    
    total_before = PropertyListing.objects.count()
    
    # Delete overpriced properties
    manchester_deleted = manchester_overpriced.delete()[0]
    salford_deleted = salford_overpriced.delete()[0]
    
    total_after = PropertyListing.objects.count() 
    total_deleted = total_before - total_after
    
    print(f'\n✅ Deleted {total_deleted} overpriced properties')
    print(f'Database now has {total_after} total properties')

if __name__ == '__main__':
    cleanup_high_priced_manchester_salford()