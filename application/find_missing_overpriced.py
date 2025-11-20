#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
django.setup()

from market_analysis.models import PropertyListing

def find_missing_overpriced_properties():
    print('🔍 Searching for ALL Salford properties in database...')
    
    # Try different search patterns
    search_patterns = [
        'Salford',
        'salford', 
        'SALFORD',
        'Salford'  # exact match
    ]
    
    for pattern in search_patterns:
        props = PropertyListing.objects.filter(address__icontains=pattern)
        print(f'Pattern "{pattern}": {props.count()} properties')
    
    # Get ALL properties and check which have Salford in address
    print('\n🔍 Checking ALL properties for Salford mentions...')
    all_props = PropertyListing.objects.filter(
        weekly_rent__gt=500  # Only high-priced ones
    ).order_by('-scraped_at')[:50]  # Recent high-priced properties
    
    salford_props = []
    for prop in all_props:
        if 'salford' in prop.address.lower():
            salford_props.append(prop)
    
    print(f'Found {len(salford_props)} high-priced Salford properties:')
    for prop in salford_props[:10]:
        print(f'  - "{prop.address}" | £{prop.weekly_rent}/week | {prop.scraped_at}')
    
    # Check recent property generation
    print('\n🕒 Recent properties (last 30 minutes):')
    from django.utils import timezone
    from datetime import timedelta
    
    recent_cutoff = timezone.now() - timedelta(minutes=30)
    recent_props = PropertyListing.objects.filter(
        scraped_at__gte=recent_cutoff,
        weekly_rent__gt=500
    ).order_by('-scraped_at')
    
    print(f'Recent high-priced properties: {recent_props.count()}')
    for prop in recent_props[:10]:
        print(f'  - {prop.address} | £{prop.weekly_rent}/week | {prop.scraped_at}')

if __name__ == '__main__':
    find_missing_overpriced_properties()