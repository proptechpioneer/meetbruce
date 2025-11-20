#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
django.setup()

from application.models import User
from market_analysis.models import MarketAnalysis, PropertyListing

def debug_steve_cache():
    print("=== DEBUGGING STEVE'S CACHE ISSUE ===")
    
    # Get Steve
    steve = User.objects.get(name__icontains='Steve')
    print(f"Steve ID: {steve.id}, Location: {steve.town}")
    print(f"Steve Rent: £{steve.weekly_rent}/week")
    
    # Check ALL analyses for Steve
    all_analyses = MarketAnalysis.objects.filter(user=steve).order_by('-created_at')
    print(f"\n📊 Total analyses for Steve: {all_analyses.count()}")
    
    for i, analysis in enumerate(all_analyses):
        print(f"\nAnalysis {i+1}:")
        print(f"  ID: {analysis.id}")
        print(f"  Created: {analysis.created_at}")
        print(f"  Average: £{analysis.average_rent}")
        print(f"  Median: £{analysis.median_rent}")
        print(f"  Min: £{analysis.min_rent}")
        print(f"  Max: £{analysis.max_rent}")
        
        # Check what properties this analysis references
        comparable_props = analysis.comparable_properties.all()
        print(f"  Comparable properties: {comparable_props.count()}")
        
        if comparable_props.exists():
            print(f"  Sample properties from this analysis:")
            for prop in comparable_props[:5]:
                print(f"    - {prop.address}: £{prop.weekly_rent}/week (Source: {prop.source})")
                
            # Calculate stats from these properties
            rents = [float(prop.weekly_rent) for prop in comparable_props]
            print(f"  Analysis property range: £{min(rents):.0f}-£{max(rents):.0f}")
            print(f"  Analysis property average: £{sum(rents)/len(rents):.2f}")
    
    # Check current database state
    print(f"\n🏠 CURRENT DATABASE STATE:")
    salford_props = PropertyListing.objects.filter(address__icontains='Salford')
    print(f"Salford properties in database: {salford_props.count()}")
    
    if salford_props.exists():
        rents = [float(prop.weekly_rent) for prop in salford_props]
        print(f"DB Range: £{min(rents):.0f}-£{max(rents):.0f}/week")
        print(f"DB Average: £{sum(rents)/len(rents):.2f}/week")
        
        print(f"\nSample current database properties:")
        for prop in salford_props[:8]:
            print(f"  - {prop.address}: £{prop.weekly_rent}/week (Source: {prop.source}, ID: {prop.id})")
    
    # Check for overpriced properties still in database
    print(f"\n💰 OVERPRICED PROPERTIES CHECK:")
    overpriced = PropertyListing.objects.filter(
        address__icontains='Salford',
        weekly_rent__gt=400
    )
    print(f"Salford properties over £400/week: {overpriced.count()}")
    
    for prop in overpriced:
        print(f"  - OVERPRICED: {prop.address}: £{prop.weekly_rent}/week (ID: {prop.id})")

if __name__ == "__main__":
    debug_steve_cache()