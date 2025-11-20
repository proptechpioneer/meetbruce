from django.contrib import admin
from .models import RentReview

@admin.register(RentReview)
class RentReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'property_address', 'user', 'overall_rating', 'is_published', 'is_verified', 'created_at')
    list_filter = ('is_published', 'is_verified', 'overall_rating', 'landlord_type', 'would_recommend', 'created_at')
    search_fields = ('title', 'property_address', 'landlord_name', 'user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at', 'average_rating')
    
    fieldsets = (
        ('Review Information', {
            'fields': ('user', 'title', 'review_text', 'overall_rating', 'average_rating')
        }),
        ('Property Details', {
            'fields': ('property_address', 'property_type', 'bedrooms', 'rent_amount', 'tenancy_duration')
        }),
        ('Landlord Information', {
            'fields': ('landlord_name', 'landlord_type')
        }),
        ('Detailed Ratings', {
            'fields': ('property_condition_rating', 'landlord_communication_rating', 
                      'value_for_money_rating', 'maintenance_response_rating')
        }),
        ('Additional Information', {
            'fields': ('would_recommend', 'issues_reported')
        }),
        ('Moderation', {
            'fields': ('is_published', 'is_verified', 'moderator_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    # Make the list display more informative
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
    
    # Add custom actions
    actions = ['mark_as_verified', 'mark_as_unverified', 'publish_reviews', 'unpublish_reviews']
    
    def mark_as_verified(self, request, queryset):
        queryset.update(is_verified=True)
        self.message_user(request, f'{queryset.count()} reviews marked as verified.')
    mark_as_verified.short_description = "Mark selected reviews as verified"
    
    def mark_as_unverified(self, request, queryset):
        queryset.update(is_verified=False)
        self.message_user(request, f'{queryset.count()} reviews marked as unverified.')
    mark_as_unverified.short_description = "Mark selected reviews as unverified"
    
    def publish_reviews(self, request, queryset):
        queryset.update(is_published=True)
        self.message_user(request, f'{queryset.count()} reviews published.')
    publish_reviews.short_description = "Publish selected reviews"
    
    def unpublish_reviews(self, request, queryset):
        queryset.update(is_published=False)
        self.message_user(request, f'{queryset.count()} reviews unpublished.')
    unpublish_reviews.short_description = "Unpublish selected reviews"
