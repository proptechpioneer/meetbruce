#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
django.setup()

from simple_scraper import RespectfulPropertyScraper

def test_salford_pricing_step_by_step():
    scraper = RespectfulPropertyScraper()
    
    print('=== DEBUGGING SALFORD PRICING ===')
    
    # Step 1: Check location pricing
    print('Step 1: Location pricing')
    base_rent_ranges, area_multiplier = scraper._get_location_pricing('Salford')
    print(f'  Area multiplier for Salford: {area_multiplier}')
    print(f'  Base 2-bed flat range: £{base_rent_ranges["flat"][2][0]}-{base_rent_ranges["flat"][2][1]}/week')
    
    adjusted_range = (
        int(base_rent_ranges["flat"][2][0] * area_multiplier),
        int(base_rent_ranges["flat"][2][1] * area_multiplier)
    )
    print(f'  After location multiplier: £{adjusted_range[0]}-{adjusted_range[1]}/week')
    
    # Step 2: Check areas and quality
    print('\nStep 2: Area quality assignment')
    areas = scraper._get_location_areas('Salford')
    print(f'  Available areas: {areas}')
    
    # Simulate the quality assignment logic from _create_realistic_sample_data
    location_areas = []
    area_multipliers = {
        'premium': 1.15,
        'high': 1.1, 
        'good': 1.05,
        'standard': 1.0,
        'affordable': 0.95,
        'budget': 0.9
    }
    
    for i, area in enumerate(areas):
        if i < 2:
            quality = 'premium'
        elif i < 4:
            quality = 'high'
        elif i < 6:
            quality = 'good'
        elif i < 8:
            quality = 'standard'
        else:
            quality = 'affordable'
        location_areas.append((area, quality))
        print(f'    {area}: {quality} (multiplier: {area_multipliers[quality]}x)')
    
    # Step 3: Calculate final price ranges
    print('\nStep 3: Final price ranges after quality multipliers')
    for area, quality in location_areas[:5]:  # Show first 5
        quality_mult = area_multipliers[quality]
        final_min = int(adjusted_range[0] * quality_mult)
        final_max = int(adjusted_range[1] * quality_mult)
        print(f'  {area} ({quality}): £{final_min}-{final_max}/week')
    
    print('\n' + '='*50)
    print('DIAGNOSIS:')
    print(f'Base range £300-650 becomes £{adjusted_range[0]}-{adjusted_range[1]} after location')
    print('Even "affordable" areas end up £285-618/week which is still too high!')
    print('The BASE RENT RANGES are too high for regional cities like Salford.')

if __name__ == '__main__':
    test_salford_pricing_step_by_step()