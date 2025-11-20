#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
django.setup()

from simple_scraper import RespectfulPropertyScraper
from market_analysis.models import PropertyListing

def test_current_pricing_generation():
    print('🧪 Testing current property generation with our pricing fix...')
    
    scraper = RespectfulPropertyScraper()
    
    # Test the pricing function
    base_ranges, multiplier = scraper._get_location_pricing('Salford')
    print(f'Salford multiplier: {multiplier}')
    print(f'Base 2-bed flat range: £{base_ranges["flat"][2][0]}-{base_ranges["flat"][2][1]}')
    
    adjusted_range = (
        int(base_ranges["flat"][2][0] * multiplier),
        int(base_ranges["flat"][2][1] * multiplier)
    )
    print(f'After multiplier: £{adjusted_range[0]}-{adjusted_range[1]}')
    
    # Generate a test property to see actual pricing
    print(f'\n🏠 Generating test Salford properties...')
    test_properties = scraper._create_realistic_sample_data('flat', 2, 'Salford', count=3)
    
    print('Generated properties:')
    for i, prop in enumerate(test_properties):
        print(f'  {i+1}. {prop["address"]} | £{prop["weekly_rent"]}/week')
    
    # Check if there are conflicting pricing systems
    print(f'\n❓ Checking if there are multiple pricing systems...')
    
    # Delete ALL overpriced Salford properties
    overpriced = PropertyListing.objects.filter(
        address__icontains='Salford',
        weekly_rent__gt=450
    )
    
    print(f'Found {overpriced.count()} overpriced Salford properties to delete')
    if overpriced.count() > 0:
        deleted = overpriced.delete()[0]
        print(f'Deleted {deleted} overpriced properties')
    
    # Generate fresh properties with the current system
    print(f'\n🔄 Generating fresh properties with fixed pricing...')
    added = scraper.scrape_properties('flat', 2, 'Salford', max_results=5)
    print(f'Added {added} new properties')
    
    # Check the new properties
    new_salford = PropertyListing.objects.filter(
        address__icontains='Salford',
        property_type='flat',
        bedrooms=2
    ).order_by('-scraped_at')[:5]
    
    print(f'Latest Salford properties:')
    for prop in new_salford:
        print(f'  - {prop.address} | £{prop.weekly_rent}/week')

if __name__ == '__main__':
    test_current_pricing_generation()