#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
django.setup()

from market_analysis.models import PropertyListing, MarketAnalysis
from application.models import User

def cleanup_and_regenerate_steve_properties():
    print('Cleaning up Steve\'s overpriced Salford properties...')
    
    # Delete Steve's existing market analyses (they reference overpriced properties)
    steve = User.objects.get(name__icontains='Steve')
    old_analyses = MarketAnalysis.objects.filter(user=steve)
    print(f'Deleting {old_analyses.count()} old market analyses for Steve')
    old_analyses.delete()
    
    # Delete all Salford properties with unrealistic pricing (>£450/week)
    overpriced_salford = PropertyListing.objects.filter(
        address__icontains='Salford',
        weekly_rent__gt=450
    )
    
    print(f'Found {overpriced_salford.count()} overpriced Salford properties (>£450/week)')
    
    # Show some examples before deletion
    for prop in overpriced_salford[:5]:
        print(f'  Deleting: {prop.address} | £{prop.weekly_rent}/week')
    
    # Delete them
    deleted_count = overpriced_salford.delete()[0]
    print(f'✅ Deleted {deleted_count} overpriced Salford properties')
    
    # Now trigger regeneration with correct pricing
    print('\n🔧 Triggering auto-population with corrected pricing...')
    from auto_populate_locations import auto_populate_for_user_analysis
    
    properties_added = auto_populate_for_user_analysis(steve)
    print(f'Auto-population complete: {properties_added} properties ensured')
    
    # Check the new pricing
    new_salford_props = PropertyListing.objects.filter(
        address__icontains='Salford',
        property_type='flat',
        bedrooms=2,
        is_active=True
    ).order_by('-scraped_at')[:10]
    
    print(f'\n📊 New Salford 2-bed flat properties ({new_salford_props.count()}):')
    total_rent = 0
    for i, prop in enumerate(new_salford_props):
        print(f'  {i+1}. {prop.address} | £{prop.weekly_rent}/week')
        total_rent += float(prop.weekly_rent)
    
    if new_salford_props:
        avg_rent = total_rent / len(new_salford_props)
        print(f'\n💰 New average weekly rent: £{avg_rent:.2f}')
        print('✅ This should be much more realistic for Salford!')

if __name__ == '__main__':
    cleanup_and_regenerate_steve_properties()