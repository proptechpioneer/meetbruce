#!/usr/bin/env python
"""Script to generate fresh property data after cache clearing"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
django.setup()

from scrapers.auto_populate_locations import ensure_location_coverage
from market_analysis.models import PropertyListing

def main():
    print("=== GENERATING FRESH SALFORD DATA ===")
    
    # Generate fresh Salford data with realistic pricing
    print("Generating 25 fresh Salford properties...")
    ensure_location_coverage('Salford', property_count=25)
    
    # Verify the new data
    salford_props = PropertyListing.objects.filter(address__icontains='Salford')
    print(f"\nNew Salford properties: {salford_props.count()}")
    
    if salford_props.exists():
        rents = [float(prop.weekly_rent) for prop in salford_props]
        print(f"Price range: £{min(rents):.0f}-£{max(rents):.0f}/week")
        print(f"Average: £{sum(rents)/len(rents):.2f}/week")
        
        print("\nFirst 5 properties:")
        for prop in salford_props[:5]:
            print(f"  {prop.address[:40]} - £{prop.weekly_rent}/week")
    
    print("\n=== FRESH DATA GENERATED ===")
    print("Now refresh the market analysis page to see realistic pricing!")

if __name__ == "__main__":
    main()