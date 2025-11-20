from django.contrib import admin
from .models import (
    IssueCategory, PropertyIssue, IssuePhoto, IssueEmail,
    IssueUpdate, IssueTemplate, EmailTemplate
)


@admin.register(IssueCategory)
class IssueCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'description']
    search_fields = ['name']


class IssuePhotoInline(admin.TabularInline):
    model = IssuePhoto
    extra = 0


class IssueEmailInline(admin.TabularInline):
    model = IssueEmail
    extra = 0
    readonly_fields = ['sent_at']


class IssueUpdateInline(admin.TabularInline):
    model = IssueUpdate
    extra = 0
    readonly_fields = ['created_at']


@admin.register(PropertyIssue)
class PropertyIssueAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'category', 'status', 'priority', 'created_at', 'days_open']
    list_filter = ['status', 'priority', 'category', 'is_urgent', 'is_safety_issue']
    search_fields = ['title', 'description', 'user__username']
    readonly_fields = ['created_at', 'updated_at', 'submitted_at']
    inlines = [IssuePhotoInline, IssueEmailInline, IssueUpdateInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'title', 'description', 'category', 'location')
        }),
        ('Status & Priority', {
            'fields': ('status', 'priority', 'is_urgent', 'is_safety_issue', 'affects_habitability')
        }),
        ('Contact Information', {
            'fields': ('contact_preference', 'landlord_email', 'property_manager_email')
        }),
        ('Dates & Deadlines', {
            'fields': ('deadline', 'created_at', 'updated_at', 'submitted_at')
        }),
        ('Escalation', {
            'fields': ('escalation_level', 'last_escalated_at')
        }),
        ('Additional Info', {
            'fields': ('cost_estimate',)
        }),
    )


@admin.register(IssueEmail)
class IssueEmailAdmin(admin.ModelAdmin):
    list_display = ['issue', 'email_type', 'to_email', 'is_sent', 'sent_at', 'response_received']
    list_filter = ['email_type', 'is_sent', 'response_received']
    search_fields = ['issue__title', 'to_email', 'subject']
    readonly_fields = ['sent_at']


@admin.register(IssueUpdate)
class IssueUpdateAdmin(admin.ModelAdmin):
    list_display = ['issue', 'update_type', 'created_by', 'created_at']
    list_filter = ['update_type']
    search_fields = ['issue__title', 'notes']
    readonly_fields = ['created_at']


@admin.register(IssueTemplate)
class IssueTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'suggested_priority', 'is_safety_issue']
    list_filter = ['category', 'suggested_priority', 'is_safety_issue']
    search_fields = ['name', 'title_template']


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'template_type', 'is_default']
    list_filter = ['template_type', 'is_default']
    search_fields = ['name', 'subject_template']
