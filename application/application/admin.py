from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import User

# Customize admin site settings
admin.site.site_header = "Bruce Management System"
admin.site.site_title = "Bruce Admin"
admin.site.index_title = "Central Management Server"

class SecureAdminSite(AdminSite):
    """
    Custom admin site with enhanced security
    """
    site_header = "Bruce Central Management Server"
    site_title = "Bruce CMS"
    index_title = "System Administration"
    
    def each_context(self, request):
        """
        Add custom context to admin templates
        """
        context = super().each_context(request)
        context['site_url'] = None  # Remove "View Site" link for security
        return context

# Create custom admin site instance
# admin_site = SecureAdminSite(name='secure_admin')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'name', 'property_type', 'weekly_rent', 'onboarding_complete', 'created_at')
    list_filter = ('onboarding_complete', 'property_type', 'rental_situation', 'created_at')
    search_fields = ('username', 'email', 'name', 'street_name', 'town', 'post_code')
    readonly_fields = ('id', 'created_at', 'password_hash')
    list_per_page = 25
    
    fieldsets = (
        ('Account Information', {
            'fields': ('id', 'username', 'email', 'password_hash', 'created_at'),
            'classes': ('collapse',)
        }),
        ('Personal Details', {
            'fields': ('name', 'phone')
        }),
        ('Address Information', {
            'fields': ('house_flat_number', 'street_number', 'street_name', 'town', 'post_code'),
            'classes': ('collapse',)
        }),
        ('Property Details', {
            'fields': ('property_type', 'bedrooms', 'bathrooms', 'has_lounge', 'parking_type', 'property_features', 'property_condition')
        }),
        ('Rental Information', {
            'fields': ('rental_situation', 'weekly_rent', 'included_utilities', 'landlord_contact', 'rental_duration'),
            'classes': ('collapse',)
        }),
        ('Onboarding & Issues', {
            'fields': ('current_issues', 'onboarding_complete')
        }),
        ('Legal Compliance', {
            'fields': ('terms_privacy', 'gdpr_consent'),
            'classes': ('collapse',)
        }),
    )
    
    # Make the list display more informative
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-created_at')
    
    # Add custom actions
    actions = ['mark_onboarding_complete', 'mark_onboarding_incomplete']
    
    def mark_onboarding_complete(self, request, queryset):
        queryset.update(onboarding_complete=True)
        self.message_user(request, f'{queryset.count()} users marked as onboarding complete.')
    mark_onboarding_complete.short_description = "Mark selected users as onboarding complete"
    
    def mark_onboarding_incomplete(self, request, queryset):
        queryset.update(onboarding_complete=False)
        self.message_user(request, f'{queryset.count()} users marked as onboarding incomplete.')
    mark_onboarding_incomplete.short_description = "Mark selected users as onboarding incomplete"