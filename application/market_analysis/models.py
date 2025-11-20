from django.db import models
from application.models import User

class PropertyListing(models.Model):
    """Model for storing scraped property listings for market analysis"""
    
    PROPERTY_TYPES = [
        ('flat', 'Flat/Apartment'),
        ('house', 'House'),
        ('studio', 'Studio'),
        ('room', 'Room'),
        ('maisonette', 'Maisonette'),
        ('bungalow', 'Bungalow'),
    ]
    
    LISTING_SOURCES = [
        ('rightmove', 'Rightmove'),
        ('openrent', 'OpenRent'),
        ('spareroom', 'SpareRoom'),
        ('zoopla', 'Zoopla'),
    ]
    
    # Basic Property Information
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES)
    bedrooms = models.IntegerField()
    bathrooms = models.FloatField(blank=True, null=True)
    
    # Location
    address = models.CharField(max_length=500)
    postcode = models.CharField(max_length=20, blank=True)
    area = models.CharField(max_length=200, blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    
    # Rental Information
    weekly_rent = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
    deposit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    furnished = models.CharField(max_length=50, blank=True)
    available_from = models.DateField(blank=True, null=True)
    
    # Property Features
    has_garden = models.BooleanField(default=False)
    has_parking = models.BooleanField(default=False)
    has_balcony = models.BooleanField(default=False)
    pets_allowed = models.BooleanField(default=False)
    
    # Scraping Metadata
    source = models.CharField(max_length=50, choices=LISTING_SOURCES)
    source_url = models.URLField()
    source_id = models.CharField(max_length=200)  # ID from the source website
    scraped_at = models.DateTimeField(auto_now_add=True)
    
    # Images
    main_image_url = models.URLField(blank=True)
    images_data = models.JSONField(default=list)  # Store multiple image URLs
    
    # Analysis flags
    is_active = models.BooleanField(default=True)
    is_duplicate = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-scraped_at']
        unique_together = ['source', 'source_id']  # Prevent duplicate listings
    
    def __str__(self):
        return f"{self.title} - £{self.weekly_rent}/week ({self.source})"


class MarketAnalysis(models.Model):
    """Model for storing market analysis results for a specific user request"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Search criteria used
    property_type = models.CharField(max_length=50)
    bedrooms = models.IntegerField()
    search_area = models.CharField(max_length=200)
    search_radius_miles = models.FloatField(default=2.0)
    
    # Analysis results
    comparable_properties = models.ManyToManyField(PropertyListing)
    average_rent = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    median_rent = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    min_rent = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    max_rent = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Market insights
    total_properties_found = models.IntegerField(default=0)
    rent_percentile = models.FloatField(blank=True, null=True)  # Where user's rent falls
    market_summary = models.TextField(blank=True)
    
    def __str__(self):
        return f"Market Analysis for {self.user.name} - {self.created_at.date()}"


class ScrapingJob(models.Model):
    """Model for tracking scraping jobs"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Search parameters
    property_type = models.CharField(max_length=50)
    bedrooms = models.IntegerField()
    location = models.CharField(max_length=200)
    max_radius = models.FloatField(default=2.0)
    
    # Job tracking
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    properties_scraped = models.IntegerField(default=0)
    error_message = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Scraping Job {self.id} - {self.status}"
