from django.urls import path
from . import views

app_name = 'report_issue'

urlpatterns = [
    # Dashboard and main views
    path('', views.issue_dashboard, name='dashboard'),
    path('issues/', views.issue_list, name='issue_list'),
    path('contact-details/', views.contact_details, name='contact_details'),
    path('landlord-compliance/', views.landlord_compliance, name='landlord_compliance'),
    path('compliance-results/', views.compliance_results, name='compliance_results'),
    
    # Issue management
    path('create/', views.create_issue, name='create_issue'),
    path('issue/<int:pk>/', views.issue_detail, name='issue_detail'),
    path('issue/<int:pk>/edit/', views.edit_issue, name='edit_issue'),
    
    # Email management
    path('issue/<int:pk>/email/', views.compose_email, name='compose_email'),
    
    # Issue actions
    path('issue/<int:pk>/escalate/', views.escalate_issue, name='escalate_issue'),
    path('issue/<int:pk>/update/', views.add_update, name='add_update'),
]