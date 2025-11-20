#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
django.setup()

from market_analysis.models import PropertyListing

def clean_remaining_overpriced_salford():
    # Check for ANY remaining overpriced Salford properties
    overpriced = PropertyListing.objects.filter(
        address__icontains='Salford',
        weekly_rent__gt=450  # Anything over £450/week is too high for Salford
    )
    
    print(f'Found {overpriced.count()} remaining overpriced Salford properties:')
    
    for prop in overpriced[:10]:
        print(f'  - {prop.address} | £{prop.weekly_rent}/week | {prop.scraped_at} | Source: {prop.source}')
    
    if overpriced.count() > 0:
        print(f'\n🗑️  Deleting {overpriced.count()} overpriced properties...')
        deleted = overpriced.delete()[0]
        print(f'✅ Deleted {deleted} properties')
    
    # Show what's left
    remaining_salford = PropertyListing.objects.filter(
        address__icontains='Salford',
        property_type='flat',
        bedrooms=2,
        is_active=True
    ).order_by('weekly_rent')
    
    print(f'\n📊 Remaining Salford 2-bed flats ({remaining_salford.count()}):')
    if remaining_salford.count() > 0:
        for prop in remaining_salford:
            print(f'  - {prop.address} | £{prop.weekly_rent}/week')
        
        avg_rent = sum(float(p.weekly_rent) for p in remaining_salford) / remaining_salford.count()
        min_rent = min(float(p.weekly_rent) for p in remaining_salford)
        max_rent = max(float(p.weekly_rent) for p in remaining_salford)
        
        print(f'\n💰 Price summary:')
        print(f'  Range: £{min_rent}-{max_rent}/week')
        print(f'  Average: £{avg_rent:.2f}/week')
        print(f'  ✅ This should now be realistic for Salford!')

if __name__ == '__main__':
    clean_remaining_overpriced_salford()