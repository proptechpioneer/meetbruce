from django import forms
from django.core.exceptions import ValidationError
from .models import PropertyIssue, IssuePhoto, IssueEmail, IssueUpdate


class PropertyIssueForm(forms.ModelForm):
    """Form for creating and editing property issues"""
    
    class Meta:
        model = PropertyIssue
        fields = [
            'title', 'description', 'category', 'location', 'priority',
            'landlord_email', 'property_manager_email', 'contact_preference',
            'deadline', 'cost_estimate', 'is_urgent', 'is_safety_issue',
            'affects_habitability'
        ]
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Brief description of the issue'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'rows': 4,
                'placeholder': 'Detailed description of the issue...'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'e.g., Kitchen, Bathroom, Living Room'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'priority': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'contact_preference': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'landlord_email': forms.EmailInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'landlord@example.com'
            }),
            'property_manager_email': forms.EmailInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'manager@example.com'
            }),
            'deadline': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'cost_estimate': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'is_urgent': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500'
            }),
            'is_safety_issue': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-red-600 border-gray-300 rounded focus:ring-red-500'
            }),
            'affects_habitability': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-yellow-600 border-gray-300 rounded focus:ring-yellow-500'
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        contact_preference = cleaned_data.get('contact_preference')
        landlord_email = cleaned_data.get('landlord_email')
        property_manager_email = cleaned_data.get('property_manager_email')
        
        if contact_preference == 'landlord' and not landlord_email:
            raise ValidationError('Landlord email is required when landlord is selected as contact preference.')
        
        if contact_preference == 'property_manager' and not property_manager_email:
            raise ValidationError('Property manager email is required when property manager is selected as contact preference.')
        
        return cleaned_data


class IssuePhotoForm(forms.ModelForm):
    """Form for uploading photos to issues"""
    
    class Meta:
        model = IssuePhoto
        fields = ['image', 'caption']
        
        widgets = {
            'image': forms.ClearableFileInput(attrs={
                'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100',
                'accept': 'image/*'
            }),
            'caption': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Optional caption for this photo'
            })
        }


class MultipleFileInput(forms.ClearableFileInput):
    """Widget for multiple file upload"""
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    """Field for multiple file upload"""
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class IssueEmailForm(forms.ModelForm):
    """Form for composing emails about issues"""
    
    send_now = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500'
        }),
        help_text='Send email immediately (uncheck to save as draft)'
    )
    
    class Meta:
        model = IssueEmail
        fields = ['email_type', 'subject', 'body', 'cc_email']
        
        widgets = {
            'email_type': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Email subject line'
            }),
            'body': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'rows': 10,
                'placeholder': 'Email content...'
            }),
            'cc_email': forms.EmailInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Optional CC email address'
            }),
        }


class IssueUpdateForm(forms.ModelForm):
    """Form for adding updates to issues"""
    
    class Meta:
        model = IssueUpdate
        fields = ['update_type', 'notes']
        
        widgets = {
            'update_type': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'rows': 3,
                'placeholder': 'Add update notes...'
            }),
        }


class IssueFilterForm(forms.Form):
    """Form for filtering issues in the list view"""
    
    status = forms.ChoiceField(
        choices=[('', 'All Statuses')] + PropertyIssue.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
        })
    )
    
    priority = forms.ChoiceField(
        choices=[('', 'All Priorities')] + PropertyIssue.PRIORITY_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
        })
    )
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Search issues...'
        })
    )


class ContactDetailsForm(forms.Form):
    """Form for confirming landlord/property manager contact details"""
    
    CONTACT_TYPE_CHOICES = [
        ('landlord', 'Landlord'),
        ('property_manager', 'Property Manager'),
        ('both', 'Both Landlord and Property Manager'),
    ]
    
    # Who do they deal with
    primary_contact = forms.ChoiceField(
        choices=CONTACT_TYPE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'mr-2'}),
        label="Who do you primarily deal with?"
    )
    
    # Landlord Details
    landlord_company_name = forms.CharField(
        max_length=200, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'e.g., ABC Properties Ltd'}),
        label="Landlord Company Name"
    )
    landlord_contact_name = forms.CharField(
        max_length=200, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'e.g., John Smith'}),
        label="Landlord Contact Name"
    )
    landlord_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'landlord@example.com'}),
        label="Landlord Email"
    )
    landlord_phone = forms.CharField(
        max_length=20, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': '07123 456789'}),
        label="Landlord Phone"
    )
    landlord_address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500', 'rows': 3, 'placeholder': 'Landlord postal address'}),
        label="Landlord Address"
    )
    
    # Property Manager Details
    property_manager_company_name = forms.CharField(
        max_length=200, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'e.g., XYZ Property Management'}),
        label="Property Manager Company Name"
    )
    property_manager_contact_name = forms.CharField(
        max_length=200, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'e.g., Jane Doe'}),
        label="Property Manager Contact Name"
    )
    property_manager_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'manager@example.com'}),
        label="Property Manager Email"
    )
    property_manager_phone = forms.CharField(
        max_length=20, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': '07123 456789'}),
        label="Property Manager Phone"
    )
    property_manager_address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500', 'rows': 3, 'placeholder': 'Property manager postal address'}),
        label="Property Manager Address"
    )