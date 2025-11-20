#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
django.setup()

from application.models import User
from market_analysis.models import PropertyListing, MarketAnalysis

def debug_steve_current_analysis():
    # Get Steve
    steve = User.objects.get(name__icontains='Steve')
    print(f'Steve: {steve.name} ({steve.email})')
    print(f'Location: {steve.town}')
    print(f'Property: {steve.property_type}, {steve.bedrooms} bedrooms')
    print()
    
    # Get his most recent market analysis
    recent_analysis = MarketAnalysis.objects.filter(user=steve).order_by('-created_at').first()
    
    if recent_analysis:
        print(f'Most recent analysis: {recent_analysis.created_at}')
        print(f'Properties found: {recent_analysis.total_properties_found}')
        print(f'Average rent: £{recent_analysis.average_rent}')
        print(f'Median rent: £{recent_analysis.median_rent}')
        print(f'Range: £{recent_analysis.min_rent} - £{recent_analysis.max_rent}')
        print()
        
        # Get the actual comparable properties
        comparable_props = recent_analysis.comparable_properties.all()
        print(f'Comparable properties ({comparable_props.count()}):')
        for i, prop in enumerate(comparable_props[:10]):
            print(f'  {i+1}. {prop.address} | Area: {prop.area} | £{prop.weekly_rent}/week | Source: {prop.source}')
        
        print()
        print('Expected for Salford 2-bed flats:')
        print('  Realistic range: £250-500/week')
        print('  Current range: £504-1136/week (TOO HIGH!)')
        
        # Check sources
        sources = comparable_props.values_list('source', flat=True).distinct()
        print(f'\nProperty sources: {list(sources)}')
        
        # Check if any are from our fixed generator
        recent_props = comparable_props.filter(scraped_at__gte='2025-11-19').order_by('-scraped_at')
        print(f'Properties from today (after our fix): {recent_props.count()}')
        
        if recent_props.count() > 0:
            print('Recent properties (should have correct pricing):')
            for prop in recent_props[:3]:
                print(f'  - {prop.address} | £{prop.weekly_rent}/week | {prop.scraped_at}')
    
    else:
        print('No market analysis found for Steve')

if __name__ == '__main__':
    debug_steve_current_analysis()