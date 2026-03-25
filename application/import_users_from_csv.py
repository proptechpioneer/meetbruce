#!/usr/bin/env python
"""
Import users from a CSV export file into the database.
Usage: python manage.py shell < import_users_from_csv.py
Or: python import_users_from_csv.py <csv_filename>
"""

import os
import sys
import csv
from pathlib import Path

# Only setup Django if not already done
if 'django' not in sys.modules:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
    import django
    django.setup()

from application.models import User
from django.utils.dateparse import parse_datetime

def import_users_from_csv(csv_filename):
    """Import users from CSV file."""
    
    csv_path = Path(csv_filename)
    
    if not csv_path.exists():
        print(f"Error: File {csv_filename} not found")
        return False
    
    imported = 0
    skipped = 0
    updated = 0
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            if not reader.fieldnames:
                print("Error: CSV file is empty or has no headers")
                return False
            
            for row_num, row in enumerate(reader, start=2):  # start=2 because row 1 is header
                try:
                    # Get or create user based on username (unique identifier)
                    username = row.get('username', '').strip()
                    
                    if not username:
                        print(f"Row {row_num}: Skipped (no username)")
                        skipped += 1
                        continue
                    
                    user_id = row.get('id', '').strip()
                    
                    # Try to update existing user, or create new
                    user, created = User.objects.get_or_create(
                        username=username,
                        defaults={k: (parse_datetime(v) if k in ['created_at', 'updated_at'] else v) or None 
                                  for k, v in row.items() if k != 'id'}
                    )
                    
                    if not created:
                        # Update existing user with CSV data
                        for key, value in row.items():
                            if key != 'id' and hasattr(user, key):
                                if key in ['created_at', 'updated_at']:
                                    value = parse_datetime(value) or value
                                elif key in ['onboarding_complete', 'has_lounge', 'terms_privacy', 'gdpr_consent']:
                                    value = value.lower() in ['true', '1', 'yes', 'on']
                                elif key in ['bedrooms', 'bathrooms', 'property_condition']:
                                    value = int(value) if value else None
                                elif key in ['weekly_rent']:
                                    value = float(value) if value else None
                                setattr(user, key, value or '')
                        user.save()
                        updated += 1
                    else:
                        imported += 1
                    
                except Exception as e:
                    print(f"Row {row_num}: Error - {str(e)}")
                    skipped += 1
                    continue
    
    except Exception as e:
        print(f"Error reading CSV: {str(e)}")
        return False
    
    print(f"\n✓ Import complete:")
    print(f"  Imported: {imported}")
    print(f"  Updated: {updated}")
    print(f"  Skipped: {skipped}")
    return True

if __name__ == '__main__':
    import glob
    
    # Allow specifying CSV filename as argument
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    else:
        # Auto-find the most recent export file
        export_files = sorted(glob.glob('users_export_*.csv'), reverse=True)
        if export_files:
            csv_file = export_files[0]
            print(f"Using latest export: {csv_file}")
        else:
            print("Error: No CSV file specified and no export files found")
            print("Usage: python import_users_from_csv.py <filename.csv>")
            sys.exit(1)
    
    success = import_users_from_csv(csv_file)
    sys.exit(0 if success else 1)
