#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
django.setup()

from simple_scraper import RespectfulPropertyScraper

def test_location_pricing():
    scraper = RespectfulPropertyScraper()
    
    locations = ['Salford', 'Manchester', 'London', 'Birmingham']
    
    for location in locations:
        print(f'\n=== {location.upper()} ===')
        base_rent_ranges, multiplier = scraper._get_location_pricing(location)
        print(f'Multiplier: {multiplier}')
        
        # Test 2-bed flat pricing
        flat_2_bed_base = base_rent_ranges['flat'][2]
        flat_2_bed_final = (int(flat_2_bed_base[0] * multiplier), int(flat_2_bed_base[1] * multiplier))
        print(f'2-bed flat range: £{flat_2_bed_base[0]}-{flat_2_bed_base[1]} -> £{flat_2_bed_final[0]}-{flat_2_bed_final[1]}/week')
        
        # Test 3-bed flat pricing
        flat_3_bed_base = base_rent_ranges['flat'][3]
        flat_3_bed_final = (int(flat_3_bed_base[0] * multiplier), int(flat_3_bed_base[1] * multiplier))
        print(f'3-bed flat range: £{flat_3_bed_base[0]}-{flat_3_bed_base[1]} -> £{flat_3_bed_final[0]}-{flat_3_bed_final[1]}/week')

if __name__ == '__main__':
    test_location_pricing()