from django.db import models
from application.models import User
from django.utils import timezone
from PIL import Image
import uuid
import os


def issue_photo_upload_path(instance, filename):
    """Generate upload path for issue photos"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('issue_photos', str(instance.issue.id), filename)


class IssueCategory(models.Model):
    """Categories for different types of property issues"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, help_text="CSS class or icon name")
    color = models.CharField(max_length=20, default="blue")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Issue Categories"


class PropertyIssue(models.Model):
    """Main model for tracking property issues"""
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('acknowledged', 'Acknowledged'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
        ('escalated', 'Escalated'),
    ]
    
    # Basic Info
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='property_issues')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(IssueCategory, on_delete=models.SET_NULL, null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Location
    location = models.CharField(max_length=200, help_text="e.g., Kitchen, Bathroom, Living Room")
    
    # Contact Info
    landlord_email = models.EmailField(blank=True, help_text="Landlord's email address")
    property_manager_email = models.EmailField(blank=True, help_text="Property manager's email address")
    contact_preference = models.CharField(
        max_length=20,
        choices=[('landlord', 'Contact Landlord'), ('property_manager', 'Contact Property Manager')],
        default='landlord'
    )
    
    # Timestamps
    # Compliance tracking
    created_from_compliance = models.BooleanField(default=False, help_text="Issue created from landlord compliance assessment")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    deadline = models.DateField(null=True, blank=True, help_text="Expected resolution date")
    
    # Escalation tracking
    escalation_level = models.IntegerField(default=0, help_text="0=Normal, 1=First escalation, 2=Second escalation, etc.")
    last_escalated_at = models.DateTimeField(null=True, blank=True)
    
    # Additional info
    cost_estimate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_urgent = models.BooleanField(default=False)
    is_safety_issue = models.BooleanField(default=False)
    affects_habitability = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"
    
    def save(self, *args, **kwargs):
        if self.status == 'submitted' and not self.submitted_at:
            self.submitted_at = timezone.now()
        super().save(*args, **kwargs)
    
    def days_open(self):
        """Calculate how many days the issue has been open"""
        if self.submitted_at:
            return (timezone.now() - self.submitted_at).days
        return 0
    
    def is_overdue(self):
        """Check if issue is past its deadline"""
        if self.deadline and self.status not in ['resolved', 'closed']:
            return timezone.now().date() > self.deadline
        return False
    
    def get_priority_color(self):
        """Get color for priority display"""
        colors = {
            'low': 'green',
            'medium': 'yellow',
            'high': 'orange',
            'urgent': 'red'
        }
        return colors.get(self.priority, 'gray')
    
    def get_status_color(self):
        """Get color for status display"""
        colors = {
            'draft': 'gray',
            'submitted': 'blue',
            'acknowledged': 'indigo',
            'in_progress': 'yellow',
            'resolved': 'green',
            'closed': 'gray',
            'escalated': 'red'
        }
        return colors.get(self.status, 'gray')
    
    class Meta:
        ordering = ['-created_at']


class IssuePhoto(models.Model):
    """Photos attached to property issues"""
    issue = models.ForeignKey(PropertyIssue, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to=issue_photo_upload_path)
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Photo for {self.issue.title}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Resize image if it's too large
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 800 or img.width > 800:
                output_size = (800, 800)
                img.thumbnail(output_size)
                img.save(self.image.path)


class IssueEmail(models.Model):
    """Track emails sent regarding issues"""
    
    EMAIL_TYPES = [
        ('initial', 'Initial Report'),
        ('follow_up', 'Follow Up'),
        ('escalation', 'Escalation'),
        ('reminder', 'Reminder'),
        ('final_notice', 'Final Notice'),
    ]
    
    issue = models.ForeignKey(PropertyIssue, on_delete=models.CASCADE, related_name='emails')
    email_type = models.CharField(max_length=20, choices=EMAIL_TYPES)
    
    # Email details
    to_email = models.EmailField()
    cc_email = models.EmailField(blank=True)
    subject = models.CharField(max_length=300)
    body = models.TextField()
    
    # Tracking
    sent_at = models.DateTimeField(auto_now_add=True)
    is_sent = models.BooleanField(default=False)
    sent_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    # Response tracking
    response_received = models.BooleanField(default=False)
    response_date = models.DateTimeField(null=True, blank=True)
    response_notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.email_type.title()} - {self.issue.title}"
    
    class Meta:
        ordering = ['-sent_at']


class IssueUpdate(models.Model):
    """Track updates and progress on issues"""
    
    UPDATE_TYPES = [
        ('status_change', 'Status Change'),
        ('landlord_response', 'Landlord Response'),
        ('user_note', 'User Note'),
        ('escalation', 'Escalation'),
        ('resolution', 'Resolution'),
    ]
    
    issue = models.ForeignKey(PropertyIssue, on_delete=models.CASCADE, related_name='updates')
    update_type = models.CharField(max_length=20, choices=UPDATE_TYPES)
    notes = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Status change tracking
    old_status = models.CharField(max_length=20, blank=True)
    new_status = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return f"{self.update_type.title()} - {self.issue.title}"
    
    class Meta:
        ordering = ['-created_at']


class IssueTemplate(models.Model):
    """Pre-written templates for common issues"""
    name = models.CharField(max_length=200)
    category = models.ForeignKey(IssueCategory, on_delete=models.SET_NULL, null=True, blank=True)
    title_template = models.CharField(max_length=200)
    description_template = models.TextField()
    suggested_priority = models.CharField(max_length=10, choices=PropertyIssue.PRIORITY_CHOICES)
    is_safety_issue = models.BooleanField(default=False)
    affects_habitability = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name


class EmailTemplate(models.Model):
    """Templates for different types of emails"""
    
    TEMPLATE_TYPES = [
        ('initial', 'Initial Report'),
        ('follow_up', 'Follow Up'),
        ('escalation', 'Escalation'),
        ('reminder', 'Reminder'),
        ('final_notice', 'Final Notice'),
    ]
    
    name = models.CharField(max_length=200)
    template_type = models.CharField(max_length=20, choices=TEMPLATE_TYPES)
    subject_template = models.CharField(max_length=300)
    body_template = models.TextField()
    is_default = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} ({self.get_template_type_display()})"
