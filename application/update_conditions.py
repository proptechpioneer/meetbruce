import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
django.setup()
from application.models import User

# Update user 'as' with a property condition rating
user_as = User.objects.get(username='as')
user_as.property_condition = 8  # Rating out of 10
user_as.save()

print(f'Updated user {user_as.username}:')
print(f'  Property Condition: {user_as.property_condition}/10')

# Update other users with sample ratings
users_to_update = [
    ('ash', 7),
    ('Ashley', 7),
]

for username, rating in users_to_update:
    try:
        user = User.objects.get(username=username)
        user.property_condition = rating
        user.save()
        print(f'Updated {username}: condition = {rating}/10')
    except User.DoesNotExist:
        print(f'User {username} not found')

print('All property condition ratings updated!')