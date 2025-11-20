from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.hashers import make_password, check_password
from .models import User
import json
import logging
from django.utils import timezone

# Set up logging for security events
logger = logging.getLogger('security')

def admin_honeypot(request):
    """
    Honeypot admin interface to log unauthorized access attempts
    """
    # Log the access attempt
    client_ip = request.META.get('HTTP_X_FORWARDED_FOR', 
                                request.META.get('REMOTE_ADDR', 'Unknown'))
    user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
    
    logger.warning(f"Admin honeypot accessed from IP: {client_ip}, "
                  f"User-Agent: {user_agent}, "
                  f"Time: {timezone.now()}, "
                  f"Path: {request.path}")
    
    # Handle POST requests (login attempts)
    if request.method == 'POST':
        username = request.POST.get('username', 'Unknown')
        password = request.POST.get('password', 'Unknown')
        
        logger.critical(f"Admin honeypot login attempt - "
                       f"IP: {client_ip}, "
                       f"Username: {username}, "
                       f"Password: {password}, "
                       f"User-Agent: {user_agent}")
        
        # Return a fake error message to make it look real
        context = {
            'error': 'Please enter the correct username and password for a staff account. '
                    'Note that both fields may be case-sensitive.'
        }
        return render(request, 'admin/honeypot_login.html', context)
    
    # For GET requests, show the fake admin login page
    return render(request, 'admin/honeypot_login.html')

def home(request):
    # If user is authenticated, redirect to dashboard
    if request.session.get('is_authenticated'):
        return redirect('/dashboard/')
    
    context = {
        'is_authenticated': request.session.get('is_authenticated', False),
        'user_id': request.session.get('user_id'),
        'username': request.session.get('username')
    }
    return render(request, 'home.html', context)

def about(request):
    context = {
        'is_authenticated': request.session.get('is_authenticated', False),
        'user_id': request.session.get('user_id'),
        'username': request.session.get('username')
    }
    return render(request, 'about.html', context)

def rrb(request):
    return render(request, 'rrb.html')

def login_view(request):
    return render(request, 'login.html')

def logout_view(request):
    # Clear session
    request.session.flush()
    return redirect('home')

def onboarding(request):
    return render(request, 'onboarding.html')

def create_account(request):
    # Check if user has completed onboarding
    onboarding_data = request.session.get('onboarding_data', {})
    print(f"DEBUG: create_account view - session data: {onboarding_data}")
    print(f"DEBUG: create_account view - session keys: {list(request.session.keys())}")
    print(f"DEBUG: create_account view - session ID: {request.session.session_key}")
    
    if not onboarding_data:
        # No onboarding data found, redirect to onboarding
        print("DEBUG: No onboarding data found, redirecting to onboarding")
        return redirect('/onboarding/')
    
    print(f"DEBUG: Found onboarding data, proceeding to create account: {onboarding_data}")
    return render(request, 'create_account.html')

@csrf_exempt
@require_http_methods(["POST"])
def save_onboarding_data(request):
    try:
        data = json.loads(request.body)
        print(f"DEBUG: Received onboarding data: {data}")  # Debug logging
        
        # Store onboarding data in session for later use when account is created
        request.session['onboarding_data'] = data
        request.session.save()  # Explicitly save session
        
        print(f"DEBUG: Session data saved: {request.session.get('onboarding_data')}")  # Debug logging
        
        return JsonResponse({
            'success': True,
            'message': 'Onboarding data saved successfully'
        })
    
    except Exception as e:
        print(f"DEBUG: Error saving onboarding data: {str(e)}")  # Debug logging
        return JsonResponse({
            'success': False,
            'message': f'Error saving data: {str(e)}'
        }, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def create_account_submit(request):
    try:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        house_flat_number = request.POST.get('house_flat_number')
        street_number = request.POST.get('street_number')
        street_name = request.POST.get('street_name')
        town = request.POST.get('town')
        post_code = request.POST.get('post_code')
        
        # Get consent fields
        terms_privacy = request.POST.get('terms_privacy') == 'on'
        gdpr_consent = request.POST.get('gdpr_consent') == 'on'
        
        # Get onboarding data from session
        onboarding_data = request.session.get('onboarding_data', {})
        print(f"DEBUG: Retrieved onboarding data from session: {onboarding_data}")  # Debug logging
        print(f"DEBUG: Session keys: {list(request.session.keys())}")  # Show all session keys
        print(f"DEBUG: Full session data: {dict(request.session)}")  # Show full session
        print(f"DEBUG: Session ID: {request.session.session_key}")  # Show session ID
        print(f"DEBUG: Is session empty? {len(onboarding_data) == 0}")  # Check if empty
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                'success': False,
                'message': 'Username already exists. Please choose a different username.'
            })
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            return JsonResponse({
                'success': False,
                'message': 'Email already exists. Please use a different email address.'
            })
        
        # Helper functions to parse onboarding data
        def safe_int(value, default=None):
            if not value:
                return default
            # Extract first number from strings like "2 bedrooms"
            import re
            numbers = re.findall(r'\d+', str(value))
            return int(numbers[0]) if numbers else default
        
        def safe_decimal(value, default=None):
            if not value:
                return default
            # Remove currency symbols and convert to decimal
            import re
            cleaned = re.sub(r'[£$,]', '', str(value))
            try:
                return float(cleaned)
            except (ValueError, TypeError):
                return default
        
        def safe_bool(value):
            if isinstance(value, str):
                return value.lower() in ['yes', 'true', '1', 'on']
            return bool(value)
        
        # Create user with account details and onboarding data
        user = User.objects.create(
            username=username,
            email=email,
            password_hash=make_password(password),
            house_flat_number=house_flat_number,
            street_number=street_number,
            street_name=street_name,
            town=town,
            post_code=post_code,
            terms_privacy=terms_privacy,
            gdpr_consent=gdpr_consent,
            # Add onboarding data with proper type conversion
            name=onboarding_data.get('name', ''),
            phone=onboarding_data.get('phone', ''),
            rental_situation=onboarding_data.get('rental_situation', ''),
            property_type=onboarding_data.get('property_type', ''),
            bedrooms=safe_int(onboarding_data.get('bedrooms')),
            bathrooms=safe_int(onboarding_data.get('bathrooms')),
            has_lounge=safe_bool(onboarding_data.get('has_lounge', '')),
            parking_type=onboarding_data.get('parking_type', ''),
            property_features=onboarding_data.get('property_features', ''),
            property_condition=safe_int(onboarding_data.get('property_condition')),
            weekly_rent=safe_decimal(onboarding_data.get('weekly_rent')),
            included_utilities=onboarding_data.get('included_utilities', ''),
            landlord_contact=onboarding_data.get('landlord_contact', ''),
            rental_duration=onboarding_data.get('rental_duration', ''),
            current_issues=onboarding_data.get('current_issues', ''),
            onboarding_complete=True
        )
        
        # Automatically log in the user
        request.session['user_id'] = user.id
        request.session['username'] = user.username
        request.session['is_authenticated'] = True
        
        # Clear onboarding data from session since it's now saved
        if 'onboarding_data' in request.session:
            del request.session['onboarding_data']
        
        return JsonResponse({
            'success': True,
            'message': 'Account created successfully',
            'user_id': user.id
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error creating account: {str(e)}'
        }, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def login_submit(request):
    try:
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Try to find user by username or email
        user = None
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid username/email or password.'
                })
        
        # Check password
        if user and check_password(password, user.password_hash):
            # Create session
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            request.session['is_authenticated'] = True
            
            return JsonResponse({
                'success': True,
                'message': 'Login successful',
                'user_id': user.id,
                'redirect_url': '/dashboard/'
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Invalid username/email or password.'
            })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Login error: {str(e)}'
        }, status=400)