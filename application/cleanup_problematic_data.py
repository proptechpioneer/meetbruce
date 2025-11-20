#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
django.setup()

from market_analysis.models import PropertyListing

def cleanup_problematic_data():
    print('Cleaning up problematic Manchester/Salford properties...')
    
    london_areas = [
        'Westminster', 'Camden', 'Islington', 'Hackney', 'Tower Hamlets', 'Greenwich',
        'Lambeth', 'Southwark', 'Kensington', 'Chelsea', 'Fulham', 'Hammersmith',
        'Wandsworth', 'Battersea', 'Clapham', 'Putney', 'Richmond', 'Wimbledon',
        'Tooting', 'Streatham', 'Croydon', 'Ealing', 'Acton', 'Chiswick'
    ]
    
    # Find Manchester properties with London areas
    manchester_to_delete = PropertyListing.objects.filter(
        address__icontains='Manchester'
    ).filter(
        area__in=london_areas
    )
    
    # Find Salford properties with London areas
    salford_to_delete = PropertyListing.objects.filter(
        address__icontains='Salford'
    ).filter(
        area__in=london_areas
    )
    
    print(f'Found {manchester_to_delete.count()} Manchester properties to delete')
    print(f'Found {salford_to_delete.count()} Salford properties to delete')
    
    total_before = PropertyListing.objects.count()
    
    # Delete the problematic properties
    manchester_deleted = manchester_to_delete.delete()[0]
    salford_deleted = salford_to_delete.delete()[0]
    
    total_after = PropertyListing.objects.count()
    total_deleted = total_before - total_after
    
    print(f'Deleted {total_deleted} problematic properties')
    print(f'Database now has {total_after} total properties')
    print('✅ Cleanup complete!')

if __name__ == '__main__':
    cleanup_problematic_data()