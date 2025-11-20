#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
django.setup()

from application.models import User
from market_analysis.models import PropertyListing, MarketAnalysis

def debug_latest_analysis():
    steve = User.objects.get(name__icontains='Steve')
    
    # Get the very latest market analysis
    latest_analysis = MarketAnalysis.objects.filter(user=steve).order_by('-created_at').first()
    
    if latest_analysis:
        print(f'=== LATEST MARKET ANALYSIS ===')
        print(f'Created: {latest_analysis.created_at}')
        print(f'Average: £{latest_analysis.average_rent}')
        print(f'Median: £{latest_analysis.median_rent}')
        print(f'Range: £{latest_analysis.min_rent} - £{latest_analysis.max_rent}')
        print(f'Total properties: {latest_analysis.total_properties_found}')
        
        # Get ALL comparable properties in this analysis
        comparable_props = latest_analysis.comparable_properties.all().order_by('weekly_rent')
        
        print(f'\n=== ALL COMPARABLE PROPERTIES ({comparable_props.count()}) ===')
        for i, prop in enumerate(comparable_props):
            print(f'{i+1:2d}. {prop.address:<25} | £{prop.weekly_rent:>6}/week | {prop.scraped_at} | {prop.source}')
        
        print(f'\n=== ANALYSIS ===')
        high_priced = comparable_props.filter(weekly_rent__gt=450)
        print(f'Properties over £450/week: {high_priced.count()}/{comparable_props.count()}')
        
        if high_priced.count() > 0:
            print('\n❌ HIGH-PRICED PROPERTIES STILL BEING USED:')
            for prop in high_priced:
                print(f'  - {prop.address} | £{prop.weekly_rent}/week | {prop.source}')
        
    else:
        print('No market analysis found for Steve - this might be the issue!')
        
    print(f'\n=== CURRENT SALFORD DATABASE STATE ===')
    all_salford = PropertyListing.objects.filter(
        address__icontains='Salford',
        property_type='flat', 
        bedrooms=2,
        is_active=True
    ).order_by('weekly_rent')
    
    print(f'All Salford 2-bed flats in database ({all_salford.count()}):')
    for prop in all_salford:
        print(f'  - {prop.address} | £{prop.weekly_rent}/week | {prop.scraped_at}')

if __name__ == '__main__':
    debug_latest_analysis()