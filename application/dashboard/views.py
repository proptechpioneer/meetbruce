from django.shortcuts import render, redirect
from application.models import User


def require_authentication(view_func):
    """Decorator to require authentication for dashboard views"""
    def wrapper(request, *args, **kwargs):
        if not request.session.get('is_authenticated'):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


@require_authentication
def dashboard_home(request):
    """
    Main dashboard view - shows user's rental property information
    and provides access to Bruce features
    """
    try:
        user_id = request.session.get('user_id')
        print(f"DEBUG: User ID from session: {user_id}")  # Debug logging
        
        user = User.objects.get(id=user_id)
        print(f"DEBUG: User found: {user.username}")  # Debug logging
        print(f"DEBUG: User name: {user.name}")  # Debug logging
        print(f"DEBUG: Property type: {user.property_type}")  # Debug logging
        print(f"DEBUG: Weekly rent: {user.weekly_rent}")  # Debug logging
        print(f"DEBUG: Bedrooms: {user.bedrooms}")  # Debug logging
        print(f"DEBUG: Onboarding complete: {user.onboarding_complete}")  # Debug logging
        
        # Check if user has meaningful data with proper data types
        has_meaningful_data = (
            user.onboarding_complete and 
            user.property_type and 
            user.weekly_rent is not None and 
            user.bedrooms is not None
        )
        
        context = {
            'user': user,
            'has_data': has_meaningful_data
        }
        print(f"DEBUG: has_data: {context['has_data']}")  # Debug logging
        
    except (User.DoesNotExist, TypeError):
        print("DEBUG: User not found or session error")  # Debug logging
        return redirect('login')
    
    return render(request, 'dashboard/home.html', context)


@require_authentication
def property_details(request):
    """
    View showing detailed property information
    """
    try:
        user_id = request.session.get('user_id')
        user = User.objects.get(id=user_id)
        context = {'user': user}
    except (User.DoesNotExist, TypeError):
        return redirect('login')
    
    return render(request, 'dashboard/property_details.html', context)


@require_authentication
def rental_insights(request):
    """
    View showing rental insights and analytics
    """
    try:
        user_id = request.session.get('user_id')
        user = User.objects.get(id=user_id)
        context = {'user': user}
    except (User.DoesNotExist, TypeError):
        return redirect('login')
    
    return render(request, 'dashboard/rental_insights.html', context)


@require_authentication
def chat_with_bruce(request):
    """
    Chat interface with Bruce AI
    """
    try:
        user_id = request.session.get('user_id')
        user = User.objects.get(id=user_id)
        context = {'user': user}
    except (User.DoesNotExist, TypeError):
        return redirect('login')
    
    return render(request, 'dashboard/chat.html', context)
