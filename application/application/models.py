from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    rental_situation = models.CharField(max_length=100, blank=True)
    property_type = models.CharField(max_length=50, blank=True)
    bedrooms = models.IntegerField(null=True, blank=True)
    bathrooms = models.IntegerField(null=True, blank=True)
    has_lounge = models.BooleanField(default=False)
    parking_type = models.CharField(max_length=100, blank=True)
    property_features = models.TextField(blank=True)
    property_condition = models.IntegerField(null=True, blank=True, help_text="Property condition rating (1-10)")
    weekly_rent = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    included_utilities = models.CharField(max_length=200, blank=True)
    landlord_contact = models.CharField(max_length=50, blank=True)
    username = models.CharField(max_length=150, blank=True, unique=True)
    password_hash = models.CharField(max_length=255, blank=True)
    house_flat_number = models.CharField(max_length=20, null=True, blank=True)
    street_number = models.CharField(max_length=20, blank=True)
    street_name = models.CharField(max_length=100, blank=True)
    town = models.CharField(max_length=100, blank=True)
    post_code = models.CharField(max_length=20, blank=True)
    rental_duration = models.CharField(max_length=50, blank=True)
    current_issues = models.TextField(blank=True)
    
    # Legal compliance fields
    terms_privacy = models.BooleanField(default=False)
    gdpr_consent = models.BooleanField(default=False)
    
    onboarding_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name if self.name else f"User {self.id}"