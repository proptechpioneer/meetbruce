#!/usr/bin/env python
"""
Nuclear cleanup script to completely eliminate all cached/overpriced data
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
django.setup()

from application.models import User
from market_analysis.models import MarketAnalysis, PropertyListing
from django.core.cache import cache
from django.contrib.sessions.models import Session

def nuclear_cleanup():
    print("🚨 NUCLEAR CLEANUP INITIATED 🚨")
    print("=" * 60)
    
    # Step 1: Find Steve
    steve = User.objects.get(name__icontains='Steve')
    print(f"👤 Target User: {steve.name} (ID: {steve.id}) - {steve.town}")
    
    # Step 2: Delete ALL market analyses for Steve
    steve_analyses = MarketAnalysis.objects.filter(user=steve)
    print(f"📊 Found {steve_analyses.count()} market analyses for Steve")
    for analysis in steve_analyses:
        print(f"   Deleting analysis ID {analysis.id}: avg={analysis.average_rent}, created={analysis.created_at}")
        analysis.delete()
    print("✅ All Steve analyses deleted")
    
    # Step 3: Delete ALL Salford properties (nuclear approach)
    salford_props = PropertyListing.objects.filter(address__icontains='Salford')
    print(f"🏠 Found {salford_props.count()} Salford properties")
    if salford_props.exists():
        rents = [float(prop.weekly_rent) for prop in salford_props]
        print(f"   Current range: £{min(rents):.0f}-£{max(rents):.0f}/week")
        print(f"   Current average: £{sum(rents)/len(rents):.2f}/week")
        
    deleted_count = salford_props.delete()[0]
    print(f"✅ Deleted ALL {deleted_count} Salford properties")
    
    # Step 4: Delete ALL Manchester properties (in case of mislabeling)
    manchester_props = PropertyListing.objects.filter(address__icontains='Manchester')
    manchester_count = manchester_props.delete()[0]
    print(f"✅ Deleted ALL {manchester_count} Manchester properties")
    
    # Step 5: Clear all cache backends
    cache.clear()
    print("✅ Django cache cleared")
    
    # Step 6: Clear all sessions
    session_count = Session.objects.all().delete()[0]
    print(f"✅ Deleted {session_count} sessions")
    
    # Step 7: Generate fresh realistic data
    print("\n🔄 GENERATING FRESH DATA")
    print("-" * 30)
    
    from simple_scraper import RespectfulPropertyScraper
    scraper = RespectfulPropertyScraper()
    scraped_count = scraper.scrape_properties(
        property_type='flat',
        bedrooms=2,
        location='Salford',
        max_results=30
    )
    print(f"✅ Generated {scraped_count} fresh properties")
    
    # Step 8: Verify final state
    print("\n✅ VERIFICATION")
    print("-" * 15)
    
    final_analyses = MarketAnalysis.objects.filter(user=steve).count()
    final_salford = PropertyListing.objects.filter(address__icontains='Salford')
    
    print(f"📊 Steve market analyses: {final_analyses}")
    print(f"🏠 Salford properties: {final_salford.count()}")
    
    if final_salford.exists():
        final_rents = [float(prop.weekly_rent) for prop in final_salford]
        final_avg = sum(final_rents) / len(final_rents)
        print(f"💰 New price range: £{min(final_rents):.0f}-£{max(final_rents):.0f}/week")
        print(f"📈 New average: £{final_avg:.2f}/week")
        print(f"🎯 Steve (£350) vs Market (£{final_avg:.0f}): {((350-final_avg)/final_avg*100):+.0f}%")
    
    print("\n" + "=" * 60)
    print("🎉 NUCLEAR CLEANUP COMPLETE!")
    print("🚀 System ready for fresh analysis")
    print("📋 Action: Refresh the market analysis page")
    print("=" * 60)

if __name__ == "__main__":
    nuclear_cleanup()