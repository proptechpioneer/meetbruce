from django.core.management.base import BaseCommand
from application.models import User

class Command(BaseCommand):
    help = 'Check user data and show what fields are empty'

    def handle(self, *args, **options):
        users = User.objects.all()
        
        self.stdout.write(self.style.SUCCESS(f'Found {users.count()} users:'))
        
        for user in users:
            self.stdout.write(f'\n--- User: {user.username} ---')
            self.stdout.write(f'Email: {user.email}')
            self.stdout.write(f'Name: {user.name or "EMPTY"}')
            self.stdout.write(f'Property Type: {user.property_type or "EMPTY"}')
            self.stdout.write(f'Bedrooms: {user.bedrooms or "EMPTY"}')
            self.stdout.write(f'Weekly Rent: {user.weekly_rent or "EMPTY"}')
            self.stdout.write(f'Property Condition: {user.property_condition or "EMPTY"}')
            self.stdout.write(f'Address: {user.house_flat_number} {user.street_number} {user.street_name}, {user.town} {user.post_code}')
            self.stdout.write(f'Onboarding Complete: {user.onboarding_complete}')
            self.stdout.write(f'Created: {user.created_at}')