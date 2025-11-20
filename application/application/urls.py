"""
URL configuration for application project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views 

urlpatterns = [
    # Real admin interface (hidden)
    path('centralmanagementserver/', admin.site.urls),
    # Honeypot admin (fake)
    path('admin/', views.admin_honeypot, name='admin_honeypot'),
    path('admin/login/', views.admin_honeypot, name='admin_honeypot_login'),
    path('' , views.home, name='home'),
    path('about', views.about, name='about'),
    path('rrb', views.rrb, name='rrb'),
    path('login/', views.login_view, name='login'),
    path('accounts/login/', views.login_view, name='accounts_login'),
    path('login/submit/', views.login_submit, name='login_submit'),
    path('logout/', views.logout_view, name='logout'),
    path('onboarding/', views.onboarding, name='onboarding'),
    path('onboarding/save/', views.save_onboarding_data, name='save_onboarding'),
    path('create-account/', views.create_account, name='create_account'),
    path('create-account/submit/', views.create_account_submit, name='create_account_submit'),
    path('dashboard/', include('dashboard.urls')),
    path('reviews/', include('rentreviews.urls')),
    path('market-analysis/', include('market_analysis.urls')),
    path('issues/', include('report_issue.urls')),
]

# Media files serving during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
