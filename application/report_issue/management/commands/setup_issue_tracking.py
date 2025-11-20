"""
Django management command to populate the report_issue app with initial data.
Run with: python manage.py setup_issue_tracking
"""

from django.core.management.base import BaseCommand
from report_issue.models import IssueCategory, EmailTemplate


class Command(BaseCommand):
    help = 'Setup initial data for the issue tracking system'

    def handle(self, *args, **options):
        self.stdout.write('Setting up issue tracking system...')
        
        # Create issue categories
        categories = [
            {
                'name': 'Plumbing',
                'description': 'Water leaks, blocked drains, heating issues',
                'icon': 'fas fa-wrench',
                'color': 'blue'
            },
            {
                'name': 'Electrical',
                'description': 'Faulty wiring, power outages, broken appliances',
                'icon': 'fas fa-bolt',
                'color': 'yellow'
            },
            {
                'name': 'Heating',
                'description': 'Broken boiler, radiator issues, no hot water',
                'icon': 'fas fa-fire',
                'color': 'red'
            },
            {
                'name': 'Structural',
                'description': 'Cracks in walls, damaged doors/windows, roof issues',
                'icon': 'fas fa-home',
                'color': 'gray'
            },
            {
                'name': 'Pest Control',
                'description': 'Mice, rats, insects, or other pest problems',
                'icon': 'fas fa-bug',
                'color': 'green'
            },
            {
                'name': 'Security',
                'description': 'Broken locks, security concerns, damaged entry points',
                'icon': 'fas fa-shield-alt',
                'color': 'purple'
            },
            {
                'name': 'Maintenance',
                'description': 'General repairs, cleaning, garden maintenance',
                'icon': 'fas fa-tools',
                'color': 'indigo'
            },
            {
                'name': 'Appliances',
                'description': 'Washing machine, dishwasher, oven issues',
                'icon': 'fas fa-tv',
                'color': 'pink'
            }
        ]

        for category_data in categories:
            category, created = IssueCategory.objects.get_or_create(
                name=category_data['name'],
                defaults={
                    'description': category_data['description'],
                    'icon': category_data['icon'],
                    'color': category_data['color']
                }
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')
            else:
                self.stdout.write(f'Category already exists: {category.name}')

        # Create email templates
        templates = [
            {
                'name': 'Initial Report',
                'template_type': 'initial',
                'subject': 'Property Issue Report - {issue_title}',
                'body': '''Dear Landlord/Property Manager,

I am writing to report an issue with my rental property at {property_address}.

Issue Details:
- Location: {issue_location}
- Category: {issue_category}
- Description: {issue_description}
- Priority: {issue_priority}
- Date Reported: {issue_date}

{has_photos}I have attached photos documenting this issue for your reference.{/has_photos}

Please arrange for this to be resolved as soon as possible. According to my tenancy agreement and landlord obligations, this type of issue should typically be addressed within {expected_resolution_days} days.

I would appreciate confirmation of receipt of this report and an estimated timeline for resolution.

Thank you for your prompt attention to this matter.

Kind regards,
{tenant_name}
{tenant_contact}'''
            },
            {
                'name': 'Follow-up Reminder',
                'template_type': 'follow_up',
                'subject': 'Follow-up: Property Issue - {issue_title}',
                'body': '''Dear Landlord/Property Manager,

I am following up on the property issue I reported on {issue_date} regarding {issue_title} at {property_address}.

Original Issue Details:
- Location: {issue_location}  
- Category: {issue_category}
- Description: {issue_description}
- Days Since Reported: {days_open}

This issue has been outstanding for {days_open} days. According to standard landlord obligations, this type of issue should typically be resolved within {expected_resolution_days} days.

Could you please provide an update on the status of this repair and when I can expect it to be resolved?

I look forward to your prompt response.

Kind regards,
{tenant_name}
{tenant_contact}'''
            },
            {
                'name': 'Urgent Reminder',
                'template_type': 'reminder',
                'subject': 'URGENT: Overdue Property Issue - {issue_title}',
                'body': '''Dear Landlord/Property Manager,

I am writing regarding the unresolved property issue at {property_address} that I initially reported on {issue_date}.

Issue Details:
- Title: {issue_title}
- Location: {issue_location}
- Category: {issue_category}
- Days Outstanding: {days_open}
- Expected Resolution Time: {expected_resolution_days} days

This issue is now OVERDUE and requires immediate attention. As my landlord, you have a legal obligation to maintain the property in good repair.

{is_safety_issue}This is a SAFETY ISSUE that poses potential risk to occupants and requires urgent resolution.{/is_safety_issue}

Please treat this as urgent and provide immediate action to resolve this matter. If this issue is not addressed promptly, I may need to consider further action including:

- Contacting the local housing authority
- Seeking advice from Citizens Advice
- Exploring legal options under housing regulations

I expect immediate confirmation of when this will be resolved.

Kind regards,
{tenant_name}
{tenant_contact}'''
            },
            {
                'name': 'Escalation Notice',
                'template_type': 'escalation',
                'subject': 'ESCALATION NOTICE: Unresolved Property Issue - {issue_title}',
                'body': '''Dear Landlord/Property Manager,

RE: ESCALATION NOTICE - Property Issue at {property_address}

This is formal notice that the property issue I reported on {issue_date} remains unresolved after {days_open} days.

Issue Summary:
- Title: {issue_title}
- Location: {issue_location}
- Category: {issue_category}
- Initial Report Date: {issue_date}
- Days Outstanding: {days_open}
- Previous Communications: {email_count} emails sent

Despite multiple attempts to resolve this matter through normal channels, no satisfactory action has been taken. This constitutes a breach of your obligations as a landlord under housing regulations.

NOTICE OF INTENDED ACTION:

Unless this issue is resolved within 7 days of this notice, I will be forced to take the following actions:

1. Report this matter to the local housing authority
2. Seek advice from Citizens Advice regarding my rights as a tenant
3. Consider legal action for breach of landlord obligations
4. Explore options for withholding rent until repairs are completed (where legally permitted)
5. Consider early termination of tenancy due to uninhabitable conditions

{is_safety_issue}This is a SAFETY ISSUE that poses immediate risk and requires URGENT resolution.{/is_safety_issue}

This is your final opportunity to resolve this matter before formal escalation procedures begin.

I require immediate written confirmation of when this issue will be resolved.

Kind regards,
{tenant_name}
{tenant_contact}

CC: [Housing Authority/Legal Advisor as applicable]'''
            }
        ]

        for template_data in templates:
            template, created = EmailTemplate.objects.get_or_create(
                name=template_data['name'],
                template_type=template_data['template_type'],
                defaults={
                    'subject_template': template_data['subject'],
                    'body_template': template_data['body']
                }
            )
            if created:
                self.stdout.write(f'Created email template: {template.name}')
            else:
                self.stdout.write(f'Email template already exists: {template.name}')

        self.stdout.write(self.style.SUCCESS('Successfully setup issue tracking system!'))
        self.stdout.write('Categories created: 8')
        self.stdout.write('Email templates created: 4')
        self.stdout.write('\nYou can now:')
        self.stdout.write('- Visit /issues/ to access the dashboard')
        self.stdout.write('- Create new property issues with photo uploads')
        self.stdout.write('- Generate professional emails to landlords')
        self.stdout.write('- Track issue progress and responses')
        self.stdout.write('- Escalate issues when necessary')