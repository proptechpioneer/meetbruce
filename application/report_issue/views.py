from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models import Q, Count
import json
from datetime import datetime, timedelta

from application.models import User
from .models import (
    PropertyIssue, IssueCategory, IssuePhoto, IssueEmail, 
    IssueUpdate, IssueTemplate, EmailTemplate
)
from .forms import PropertyIssueForm, IssuePhotoForm, IssueEmailForm, ContactDetailsForm


def require_authentication(view_func):
    """Decorator to require authentication for issue tracking views"""
    def wrapper(request, *args, **kwargs):
        if not request.session.get('is_authenticated'):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


@require_authentication
def issue_dashboard(request):
    """Main dashboard showing all user issues"""
    user = User.objects.get(id=request.session.get('user_id'))
    user_issues = PropertyIssue.objects.filter(user=user)
    
    # Check prerequisite completion status
    contact_details_completed = request.session.get('contact_details') is not None
    compliance_completed = request.session.get('compliance_results') is not None
    prerequisites_completed = contact_details_completed and compliance_completed
    
    # Statistics
    stats = {
        'total': user_issues.count(),
        'open': user_issues.exclude(status__in=['resolved', 'closed']).count(),
        'urgent': user_issues.filter(is_urgent=True).exclude(status__in=['resolved', 'closed']).count(),
        'overdue': sum(1 for issue in user_issues if issue.is_overdue()),
    }
    
    # Recent issues
    recent_issues = user_issues[:5]
    
    # Issues needing attention
    needs_attention = user_issues.filter(
        Q(status='submitted') & 
        Q(submitted_at__lt=timezone.now() - timedelta(days=7))
    ) | user_issues.filter(
        Q(is_urgent=True) & 
        ~Q(status__in=['resolved', 'closed'])
    )
    
    context = {
        'stats': stats,
        'recent_issues': recent_issues,
        'needs_attention': needs_attention[:3],
        'categories': IssueCategory.objects.all(),
        'contact_details_completed': contact_details_completed,
        'compliance_completed': compliance_completed,
        'prerequisites_completed': prerequisites_completed,
    }
    
    return render(request, 'report_issue/dashboard.html', context)


@require_authentication
def issue_list(request):
    """List all user issues with filtering"""
    # Check prerequisites
    contact_details_completed = request.session.get('contact_details') is not None
    compliance_completed = request.session.get('compliance_results') is not None
    
    if not contact_details_completed or not compliance_completed:
        messages.error(request, 'Please complete contact details and landlord compliance checklist first.')
        return redirect('report_issue:dashboard')
    
    user = User.objects.get(id=request.session.get('user_id'))
    issues = PropertyIssue.objects.filter(user=user)
    
    # Filtering
    status_filter = request.GET.get('status')
    priority_filter = request.GET.get('priority')
    category_filter = request.GET.get('category')
    
    if status_filter:
        issues = issues.filter(status=status_filter)
    if priority_filter:
        issues = issues.filter(priority=priority_filter)
    if category_filter:
        issues = issues.filter(category_id=category_filter)
    
    context = {
        'issues': issues,
        'categories': IssueCategory.objects.all(),
        'status_choices': PropertyIssue.STATUS_CHOICES,
        'priority_choices': PropertyIssue.PRIORITY_CHOICES,
        'current_filters': {
            'status': status_filter,
            'priority': priority_filter,
            'category': category_filter,
        }
    }
    
    return render(request, 'report_issue/issue_list.html', context)


@require_authentication
def create_issue(request):
    """Create a new property issue"""
    # Check prerequisites
    contact_details_completed = request.session.get('contact_details') is not None
    compliance_completed = request.session.get('compliance_results') is not None
    
    if not contact_details_completed or not compliance_completed:
        messages.error(request, 'Please complete contact details and landlord compliance checklist first.')
        return redirect('report_issue:dashboard')
    
    if request.method == 'POST':
        form = PropertyIssueForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)
            user = User.objects.get(id=request.session.get('user_id'))
            issue.user = user
            
            # Auto-populate contact info if available
            if hasattr(user, 'landlord_contact') and not issue.landlord_email:
                issue.landlord_email = getattr(user, 'landlord_email', '')
            
            issue.save()
            
            # Handle photo uploads
            photos = request.FILES.getlist('photos')
            for photo in photos:
                IssuePhoto.objects.create(issue=issue, image=photo)
            
            messages.success(request, 'Issue created successfully!')
            return redirect('report_issue:issue_detail', pk=issue.pk)
    else:
        form = PropertyIssueForm()
        
        # Pre-populate from template if specified
        template_id = request.GET.get('template')
        if template_id:
            try:
                template = IssueTemplate.objects.get(id=template_id)
                form.fields['title'].initial = template.title_template
                form.fields['description'].initial = template.description_template
                form.fields['priority'].initial = template.suggested_priority
                form.fields['category'].initial = template.category
                form.fields['is_safety_issue'].initial = template.is_safety_issue
                form.fields['affects_habitability'].initial = template.affects_habitability
            except IssueTemplate.DoesNotExist:
                pass
    
    context = {
        'form': form,
        'templates': IssueTemplate.objects.all(),
        'categories': IssueCategory.objects.all(),
    }
    
    return render(request, 'report_issue/create_issue.html', context)


@require_authentication
def issue_detail(request, pk):
    """View detailed information about a specific issue"""
    user = User.objects.get(id=request.session.get('user_id'))
    issue = get_object_or_404(PropertyIssue, pk=pk, user=user)
    
    # Get related data
    photos = issue.photos.all()
    emails = issue.emails.all()
    updates = issue.updates.all()
    
    context = {
        'issue': issue,
        'photos': photos,
        'emails': emails,
        'updates': updates,
        'can_escalate': issue.status not in ['resolved', 'closed'] and issue.days_open() >= 7,
    }
    
    return render(request, 'report_issue/issue_detail.html', context)


@require_authentication
def edit_issue(request, pk):
    """Edit an existing issue"""
    user = User.objects.get(id=request.session.get('user_id'))
    issue = get_object_or_404(PropertyIssue, pk=pk, user=user)
    
    if request.method == 'POST':
        form = PropertyIssueForm(request.POST, instance=issue)
        if form.is_valid():
            old_status = issue.status
            issue = form.save()
            
            # Log status change
            if old_status != issue.status:
                IssueUpdate.objects.create(
                    issue=issue,
                    update_type='status_change',
                    notes=f'Status changed from {old_status} to {issue.status}',
                    old_status=old_status,
                    new_status=issue.status,
                    created_by=user
                )
            
            messages.success(request, 'Issue updated successfully!')
            return redirect('report_issue:issue_detail', pk=issue.pk)
    else:
        form = PropertyIssueForm(instance=issue)
    
    context = {
        'form': form,
        'issue': issue,
        'categories': IssueCategory.objects.all(),
    }
    
    return render(request, 'report_issue/edit_issue.html', context)


@require_authentication
def compose_email(request, pk):
    """Compose and send email about an issue"""
    user = User.objects.get(id=request.session.get('user_id'))
    issue = get_object_or_404(PropertyIssue, pk=pk, user=user)
    
    if request.method == 'POST':
        form = IssueEmailForm(request.POST)
        if form.is_valid():
            email = form.save(commit=False)
            email.issue = issue
            email.sent_by = user
            
            # Determine recipient
            if issue.contact_preference == 'property_manager' and issue.property_manager_email:
                email.to_email = issue.property_manager_email
            else:
                email.to_email = issue.landlord_email
            
            email.save()
            
            # Send the email if requested
            if form.cleaned_data.get('send_now', False):
                try:
                    send_mail(
                        subject=email.subject,
                        message=email.body,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[email.to_email],
                        fail_silently=False
                    )
                    email.is_sent = True
                    email.save()
                    
                    # Update issue status if it's the first email
                    if issue.status == 'draft':
                        issue.status = 'submitted'
                        issue.save()
                    
                    messages.success(request, 'Email sent successfully!')
                except Exception as e:
                    messages.error(request, f'Failed to send email: {str(e)}')
            else:
                messages.success(request, 'Email draft saved!')
            
            return redirect('report_issue:issue_detail', pk=issue.pk)
    else:
        # Pre-populate email based on type
        email_type = request.GET.get('type', 'initial')
        template = None
        
        try:
            template = EmailTemplate.objects.filter(
                template_type=email_type, 
                is_default=True
            ).first()
        except EmailTemplate.DoesNotExist:
            pass
        
        initial_data = {
            'email_type': email_type,
            'subject': generate_email_subject(issue, email_type, template),
            'body': generate_email_body(issue, email_type, template),
        }
        
        form = IssueEmailForm(initial=initial_data)
    
    context = {
        'form': form,
        'issue': issue,
        'templates': EmailTemplate.objects.filter(template_type=request.GET.get('type', 'initial')),
    }
    
    return render(request, 'report_issue/compose_email.html', context)


@require_authentication
def escalate_issue(request, pk):
    """Escalate an issue to next level"""
    user = User.objects.get(id=request.session.get('user_id'))
    issue = get_object_or_404(PropertyIssue, pk=pk, user=user)
    
    if issue.status in ['resolved', 'closed']:
        messages.error(request, 'Cannot escalate a resolved or closed issue.')
        return redirect('report_issue:issue_detail', pk=issue.pk)
    
    if request.method == 'POST':
        escalation_notes = request.POST.get('escalation_notes', '')
        
        # Increase escalation level
        issue.escalation_level += 1
        issue.last_escalated_at = timezone.now()
        issue.status = 'escalated'
        issue.save()
        
        # Create update log
        IssueUpdate.objects.create(
            issue=issue,
            update_type='escalation',
            notes=f'Issue escalated to level {issue.escalation_level}. Notes: {escalation_notes}',
            created_by=user
        )
        
        messages.success(request, f'Issue escalated to level {issue.escalation_level}!')
        return redirect('report_issue:issue_detail', pk=issue.pk)
    
    context = {
        'issue': issue,
    }
    
    return render(request, 'report_issue/escalate_issue.html', context)


@require_authentication
def add_update(request, pk):
    """Add an update/note to an issue"""
    user = User.objects.get(id=request.session.get('user_id'))
    issue = get_object_or_404(PropertyIssue, pk=pk, user=user)
    
    if request.method == 'POST':
        update_type = request.POST.get('update_type', 'user_note')
        notes = request.POST.get('notes')
        
        if notes:
            IssueUpdate.objects.create(
                issue=issue,
                update_type=update_type,
                notes=notes,
                created_by=user
            )
            messages.success(request, 'Update added successfully!')
        else:
            messages.error(request, 'Please provide update notes.')
    
    return redirect('report_issue:issue_detail', pk=issue.pk)


def generate_email_subject(issue, email_type, template=None):
    """Generate email subject based on type and template"""
    if template and template.subject_template:
        return template.subject_template.format(
            title=issue.title,
            property_address=f"{issue.user.street_number} {issue.user.street_name}",
            issue_id=issue.id
        )
    
    subjects = {
        'initial': f'Property Issue Report: {issue.title}',
        'follow_up': f'Follow-up: {issue.title}',
        'escalation': f'URGENT - Escalated Issue: {issue.title}',
        'reminder': f'Reminder: Outstanding Issue - {issue.title}',
        'final_notice': f'FINAL NOTICE: {issue.title}',
    }
    
    return subjects.get(email_type, f'Property Issue: {issue.title}')


def generate_email_body(issue, email_type, template=None):
    """Generate email body based on type and template"""
    if template and template.body_template:
        return template.body_template.format(
            title=issue.title,
            description=issue.description,
            location=issue.location,
            priority=issue.get_priority_display(),
            property_address=f"{issue.user.street_number} {issue.user.street_name}",
            tenant_name=issue.user.get_full_name() or issue.user.username,
            created_date=issue.created_at.strftime('%Y-%m-%d'),
            issue_id=issue.id,
            days_open=issue.days_open()
        )
    
    # Default email bodies
    base_info = f"""
Property Issue Details:
- Issue: {issue.title}
- Location: {issue.location}
- Priority: {issue.get_priority_display()}
- Description: {issue.description}
- Property: {issue.user.street_number} {issue.user.street_name}
- Reported: {issue.created_at.strftime('%Y-%m-%d')}
"""
    
    bodies = {
        'initial': f"Dear Landlord,\n\nI am writing to report a property issue that requires attention.{base_info}\n\nI would appreciate your prompt attention to this matter.\n\nBest regards,\n{issue.user.get_full_name() or issue.user.username}",
        'follow_up': f"Dear Landlord,\n\nI am following up on the property issue I reported {issue.days_open()} days ago.{base_info}\n\nCould you please provide an update on when this will be addressed?\n\nBest regards,\n{issue.user.get_full_name() or issue.user.username}",
        'escalation': f"Dear Landlord,\n\nI am escalating this property issue as it has been {issue.days_open()} days without resolution.{base_info}\n\nThis matter requires urgent attention. Please respond within 48 hours.\n\nBest regards,\n{issue.user.get_full_name() or issue.user.username}",
        'reminder': f"Dear Landlord,\n\nThis is a reminder about the outstanding property issue reported {issue.days_open()} days ago.{base_info}\n\nPlease provide an update at your earliest convenience.\n\nBest regards,\n{issue.user.get_full_name() or issue.user.username}",
        'final_notice': f"Dear Landlord,\n\nFINAL NOTICE - This property issue has been outstanding for {issue.days_open()} days.{base_info}\n\nThis is my final request before seeking alternative resolution methods.\n\nBest regards,\n{issue.user.get_full_name() or issue.user.username}",
    }
    
    return bodies.get(email_type, base_info)


@require_authentication
def contact_details(request):
    """Confirm contact details for landlord/property manager"""
    if request.method == 'POST':
        form = ContactDetailsForm(request.POST)
        if form.is_valid():
            try:
                current_user = User.objects.get(id=request.session.get('user_id'))
            except User.DoesNotExist:
                return redirect('login')
            
            # Process contact details - store in session for use in issue reporting
            contact_data = form.cleaned_data
            request.session['contact_details'] = contact_data
            
            messages.success(request, 'Contact details confirmed successfully!')
            return redirect('report_issue:issue_list')
    else:
        try:
            current_user = User.objects.get(id=request.session.get('user_id'))
        except User.DoesNotExist:
            return redirect('login')
        
        # Pre-populate form with user's onboarding data
        initial_data = {}
        
        # Map onboarding landlord_contact to our form's primary_contact field
        if current_user.landlord_contact:
            if current_user.landlord_contact.lower() == 'landlord':
                initial_data['primary_contact'] = 'landlord'
            elif current_user.landlord_contact.lower() == 'property manager':
                initial_data['primary_contact'] = 'property_manager'
        
        form = ContactDetailsForm(initial=initial_data)
    
    return render(request, 'report_issue/contact_details.html', {'form': form})


@require_authentication
def landlord_compliance(request):
    """Landlord compliance checklist for tenants to verify legal obligations"""
    # Define compliance checklist items with categories
    compliance_items = {
        'Property Condition': [
            {'id': 'habitability', 'text': 'Property is maintained in habitable condition', 'description': 'Landlord ensures property meets basic health and safety standards'},
            {'id': 'repairs', 'text': 'Repairs are completed in reasonable timeframe', 'description': 'Essential repairs addressed within 24-48 hours, non-essential within 30 days'},
            {'id': 'heating', 'text': 'Adequate heating provided', 'description': 'Heating system maintains at least 68°F during heating season'},
            {'id': 'water_plumbing', 'text': 'Running water and working plumbing', 'description': 'Hot and cold water available, toilets and drains function properly'},
            {'id': 'electrical', 'text': 'Safe electrical systems', 'description': 'Electrical systems are up to code and safely maintained'},
        ],
        'Safety & Security': [
            {'id': 'smoke_detectors', 'text': 'Working smoke detectors installed', 'description': 'Smoke detectors in required locations and batteries maintained'},
            {'id': 'carbon_monoxide', 'text': 'Carbon monoxide detectors (where required)', 'description': 'CO detectors installed near fuel-burning appliances and bedrooms'},
            {'id': 'locks', 'text': 'Proper locks on doors and windows', 'description': 'Secure locks provided for entry doors and accessible windows'},
            {'id': 'emergency_exits', 'text': 'Clear emergency exits', 'description': 'Fire exits are clearly marked and unobstructed'},
        ],
        'Legal Documentation': [
            {'id': 'lease_agreement', 'text': 'Written lease agreement provided', 'description': 'Clear written lease with terms, conditions, and both parties\' obligations'},
            {'id': 'deposit_receipt', 'text': 'Security deposit receipt given', 'description': 'Written receipt for security deposit with terms for return'},
            {'id': 'move_in_inspection', 'text': 'Move-in inspection completed', 'description': 'Property condition documented before tenancy begins'},
            {'id': 'landlord_info', 'text': 'Landlord contact information provided', 'description': 'Name, address, and contact details of landlord or property manager'},
        ],
        'Privacy & Access': [
            {'id': 'notice_entry', 'text': 'Proper notice given for entry', 'description': 'Landlord provides required notice (usually 24-48 hours) before entering'},
            {'id': 'quiet_enjoyment', 'text': 'Right to quiet enjoyment respected', 'description': 'Tenant can use property without unreasonable interference'},
            {'id': 'emergency_contact', 'text': 'Emergency contact information available', 'description': 'Contact available for emergency repairs and urgent situations'},
        ],
        'Financial Obligations': [
            {'id': 'rent_receipts', 'text': 'Rent receipts provided when requested', 'description': 'Written receipts for rent payments when requested by tenant'},
            {'id': 'deposit_interest', 'text': 'Security deposit interest (where required)', 'description': 'Interest paid on security deposits as required by local law'},
            {'id': 'fee_disclosure', 'text': 'All fees and charges disclosed', 'description': 'Transparent disclosure of all fees, charges, and payment terms'},
        ]
    }
    
    # Handle form submission
    if request.method == 'POST':
        try:
            current_user = User.objects.get(id=request.session.get('user_id'))
        except User.DoesNotExist:
            return redirect('login')
        
        # Process checklist responses and create issues for non-compliance
        compliance_results = {}
        total_items = 0
        compliant_items = 0
        issues_created = []
        
        for category, items in compliance_items.items():
            compliance_results[category] = []
            for item in items:
                total_items += 1
                is_compliant = request.POST.get(item['id']) == 'yes'
                if is_compliant:
                    compliant_items += 1
                else:
                    # Create issue for non-compliant item
                    issue = PropertyIssue.objects.create(
                        user=current_user,
                        title=f"Non-compliance: {item['text']}",
                        description=f"Compliance Issue - {category}\n\n{item['description']}\n\nThis issue was automatically created from your landlord compliance assessment. Please review and add any additional details or photos as needed.",
                        location="General Property",
                        priority="medium",
                        status="draft",
                        is_safety_issue=category == "Safety & Security",
                        affects_habitability=category in ["Property Condition", "Safety & Security"],
                        created_from_compliance=True
                    )
                    issues_created.append({
                        'title': item['text'],
                        'category': category,
                        'issue_id': issue.id
                    })
                
                compliance_results[category].append({
                    **item,
                    'compliant': is_compliant
                })
        
        # Calculate compliance percentage
        compliance_percentage = (compliant_items / total_items * 100) if total_items > 0 else 0
        
        # Store results in session
        request.session['compliance_results'] = {
            'results': compliance_results,
            'total_items': total_items,
            'compliant_items': compliant_items,
            'compliance_percentage': round(compliance_percentage, 1),
            'completed_date': timezone.now().isoformat(),
            'issues_created': issues_created
        }
        
        if issues_created:
            messages.success(request, f'Compliance assessment completed. {len(issues_created)} issues were automatically created for non-compliant items.')
        else:
            messages.success(request, 'Compliance assessment completed successfully!')
            
        return redirect('report_issue:compliance_results')
    
    context = {
        'compliance_items': compliance_items,
    }
    
    return render(request, 'report_issue/landlord_compliance.html', context)


@require_authentication
def compliance_results(request):
    """Display compliance checklist results"""
    compliance_data = request.session.get('compliance_results')
    
    if not compliance_data:
        messages.error(request, 'No compliance data found. Please complete the checklist first.')
        return redirect('report_issue:landlord_compliance')
    
    # Generate recommendations based on non-compliant items
    recommendations = []
    non_compliant_items = []
    
    for category, items in compliance_data['results'].items():
        for item in items:
            if not item['compliant']:
                non_compliant_items.append({
                    'category': category,
                    'text': item['text'],
                    'description': item['description']
                })
    
    # Add specific recommendations
    if non_compliant_items:
        recommendations = [
            'Document all non-compliant issues with photos and written records',
            'Contact your landlord in writing to request compliance',
            'Keep copies of all communications with your landlord',
            'Consider contacting local tenant rights organizations for guidance',
            'Research local housing codes and tenant protection laws'
        ]
        
        if len(non_compliant_items) >= 5:
            recommendations.append('Consider consulting with a tenant rights attorney')
        
        if any('safety' in item['text'].lower() or 'smoke' in item['text'].lower() or 'carbon' in item['text'].lower() for item in non_compliant_items):
            recommendations.insert(0, 'PRIORITY: Address safety issues immediately - contact local housing authority if necessary')
    
    context = {
        'compliance_data': compliance_data,
        'non_compliant_items': non_compliant_items,
        'recommendations': recommendations,
    }
    
    return render(request, 'report_issue/compliance_results.html', context)
