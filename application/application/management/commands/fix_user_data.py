from django.core.management.base import BaseCommand
from application.models import User

class Command(BaseCommand):
    help = 'Fix user data by adding sample onboarding information'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username of the user to update')

    def handle(self, *args, **options):
        username = options['username']
        
        try:
            user = User.objects.get(username=username)
            
            # Add sample data
            user.name = "Ashley Osborne"
            user.property_type = "Flat/apartment"
            user.bedrooms = "2 bedrooms"
            user.weekly_rent = "£650"
            user.property_condition = "8 - Excellent condition"
            user.rental_situation = "Renting by myself"
            user.bathrooms = "1 bathroom"
            user.parking_type = "No parking"
            user.property_features = "Balcony, Garden"
            user.included_utilities = "Gas, Electricity"
            user.landlord_contact = "Property manager"
            user.rental_duration = "6-12 months"
            user.current_issues = "None"
            
            user.save()
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully updated user {username} with sample data')
            )
            
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'User {username} not found')
            )