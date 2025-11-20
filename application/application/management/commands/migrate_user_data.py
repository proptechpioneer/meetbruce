from django.core.management.base import BaseCommand
from django.db import connection
import re

class Command(BaseCommand):
    help = 'Migrate user data from string to proper data types'

    def handle(self, *args, **options):
        def safe_int(value):
            if not value or value == '':
                return None
            numbers = re.findall(r'\d+', str(value))
            return int(numbers[0]) if numbers else None

        def safe_decimal(value):
            if not value or value == '':
                return None
            cleaned = re.sub(r'[£$,]', '', str(value))
            try:
                return float(cleaned)
            except:
                return None

        def safe_bool(value):
            if isinstance(value, str):
                return value.lower() in ['yes', 'true', '1', 'on']
            return bool(value)

        # Use raw SQL to update the data
        with connection.cursor() as cursor:
            # Get all users
            cursor.execute('SELECT id, weekly_rent, bedrooms, bathrooms, has_lounge FROM application_user')
            users = cursor.fetchall()
            
            for user_id, weekly_rent, bedrooms, bathrooms, has_lounge in users:
                # Convert values
                new_weekly_rent = safe_decimal(weekly_rent)
                new_bedrooms = safe_int(bedrooms)
                new_bathrooms = safe_int(bathrooms)
                new_has_lounge = safe_bool(has_lounge)
                
                # Update the user
                cursor.execute('''
                    UPDATE application_user 
                    SET weekly_rent = ?, bedrooms = ?, bathrooms = ?, has_lounge = ?
                    WHERE id = ?
                ''', [new_weekly_rent, new_bedrooms, new_bathrooms, new_has_lounge, user_id])
                
                self.stdout.write(f'Updated user {user_id}: rent={new_weekly_rent}, bedrooms={new_bedrooms}, bathrooms={new_bathrooms}, lounge={new_has_lounge}')

        self.stdout.write(self.style.SUCCESS('Successfully migrated user data'))