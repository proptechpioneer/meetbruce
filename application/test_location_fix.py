#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
django.setup()

from simple_scraper import RespectfulPropertyScraper

def test_location_specific_properties():
    scraper = RespectfulPropertyScraper()
    
    print('=== Testing Manchester Property Generation ===')
    manchester_properties = scraper._create_realistic_sample_data('flat', 2, 'Manchester', count=3)
    
    for i, prop in enumerate(manchester_properties):
        print(f'Property {i+1}:')
        print(f'  Address: {prop["address"]}')
        print(f'  Area: {prop["area"]}')
        print(f'  Weekly Rent: £{prop["weekly_rent"]}')
        print(f'  Postcode: {prop["postcode"]}')
        print()
    
    print('=== Testing London Property Generation ===')
    london_properties = scraper._create_realistic_sample_data('flat', 2, 'London', count=2)
    
    for i, prop in enumerate(london_properties):
        print(f'Property {i+1}:')
        print(f'  Address: {prop["address"]}')
        print(f'  Area: {prop["area"]}')
        print(f'  Weekly Rent: £{prop["weekly_rent"]}')
        print(f'  Postcode: {prop["postcode"]}')
        print()

if __name__ == '__main__':
    test_location_specific_properties()