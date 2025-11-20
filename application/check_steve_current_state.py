#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
django.setup()

from application.models import User
from market_analysis.models import PropertyListing, MarketAnalysis

def check_steve_current_state():
    steve = User.objects.get(name__icontains='Steve')
    print(f'Steve: {steve.name} ({steve.email})')
    
    # Check his most recent market analysis
    recent_analysis = MarketAnalysis.objects.filter(user=steve).order_by('-created_at').first()
    
    if recent_analysis:
        print(f'\n=== CURRENT MARKET ANALYSIS (from database) ===')
        print(f'Created: {recent_analysis.created_at}')
        print(f'Average rent: £{recent_analysis.average_rent}')
        print(f'Median rent: £{recent_analysis.median_rent}')
        print(f'Range: £{recent_analysis.min_rent} - £{recent_analysis.max_rent}')
        print(f'Properties found: {recent_analysis.total_properties_found}')
        
        # Check the comparable properties it's using
        comparable_props = recent_analysis.comparable_properties.all()
        print(f'\nComparable properties in this analysis:')
        for prop in comparable_props[:5]:
            print(f'  - {prop.address} | £{prop.weekly_rent}/week | Created: {prop.scraped_at}')
        
        # Check if analysis is using old overpriced data
        high_priced = comparable_props.filter(weekly_rent__gt=500)
        print(f'\nProperties over £500/week: {high_priced.count()}/{comparable_props.count()}')
        if high_priced.count() > 0:
            print('❌ PROBLEM: Analysis is still using old overpriced properties!')
        else:
            print('✅ Analysis using realistic pricing')
    
    # Check what's currently in the database for Salford
    print(f'\n=== CURRENT SALFORD PROPERTIES (in database) ===')
    current_salford = PropertyListing.objects.filter(
        address__icontains='Salford',
        property_type='flat',
        bedrooms=2,
        is_active=True
    ).order_by('-scraped_at')[:5]
    
    print(f'Latest 2-bed Salford flats:')
    for prop in current_salford:
        print(f'  - {prop.address} | £{prop.weekly_rent}/week | {prop.scraped_at}')
    
    if current_salford.count() > 0:
        avg_current = sum(float(p.weekly_rent) for p in current_salford) / current_salford.count()
        print(f'Average of latest properties: £{avg_current:.2f}/week')
        
        if avg_current > 500:
            print('❌ PROBLEM: Even latest properties have high pricing!')
        else:
            print('✅ Latest properties have realistic pricing')

if __name__ == '__main__':
    check_steve_current_state()