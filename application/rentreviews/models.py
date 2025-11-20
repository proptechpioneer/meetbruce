from django.db import models
from application.models import User

class RentReview(models.Model):
    """Model for rent reviews submitted by tenants"""
    
    # Review details
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rent_reviews')
    
    # Property information
    property_address = models.CharField(max_length=300, help_text="Full property address")
    property_type = models.CharField(max_length=100, blank=True)
    bedrooms = models.CharField(max_length=50, blank=True)
    
    # Landlord/Agent information
    landlord_name = models.CharField(max_length=200, blank=True)
    landlord_type = models.CharField(max_length=100, choices=[
        ('landlord', 'Direct Landlord'),
        ('agent', 'Property Agent'),
        ('unknown', 'Unknown')
    ], default='unknown')
    
    # Review content
    overall_rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], help_text="1-5 star rating")
    title = models.CharField(max_length=200, help_text="Brief title for your review")
    review_text = models.TextField(help_text="Detailed review content")
    
    # Specific ratings
    property_condition_rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], blank=True, null=True)
    landlord_communication_rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], blank=True, null=True)
    value_for_money_rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], blank=True, null=True)
    maintenance_response_rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], blank=True, null=True)
    
    # Additional details
    rent_amount = models.CharField(max_length=100, blank=True, help_text="Weekly/Monthly rent")
    tenancy_duration = models.CharField(max_length=100, blank=True)
    would_recommend = models.BooleanField(default=True)
    
    # Issues reported
    issues_reported = models.TextField(blank=True, help_text="Any issues during tenancy")
    
    # Moderation
    is_verified = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    moderator_notes = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Rent Review"
        verbose_name_plural = "Rent Reviews"
    
    def __str__(self):
        return f"{self.title} - {self.property_address} ({self.overall_rating}★)"
    
    @property
    def average_rating(self):
        """Calculate average of all specific ratings"""
        ratings = [
            self.property_condition_rating,
            self.landlord_communication_rating,
            self.value_for_money_rating,
            self.maintenance_response_rating
        ]
        valid_ratings = [r for r in ratings if r is not None]
        return round(sum(valid_ratings) / len(valid_ratings), 1) if valid_ratings else self.overall_rating
