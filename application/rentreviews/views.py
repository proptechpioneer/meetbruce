from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import RentReview
from application.models import User


def require_authentication(view_func):
    """Decorator to require authentication for review views"""
    def wrapper(request, *args, **kwargs):
        if not request.session.get('is_authenticated'):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


def review_list(request):
    """Public view showing all published rent reviews"""
    reviews = RentReview.objects.filter(is_published=True)
    
    # Filter by search parameters
    search_query = request.GET.get('search', '')
    if search_query:
        reviews = reviews.filter(property_address__icontains=search_query)
    
    # Filter by rating
    min_rating = request.GET.get('min_rating')
    if min_rating:
        reviews = reviews.filter(overall_rating__gte=min_rating)
    
    context = {
        'reviews': reviews,
        'search_query': search_query,
        'min_rating': min_rating,
    }
    return render(request, 'rentreviews/rr_home.html', context)


def review_detail(request, review_id):
    """Show detailed view of a specific review"""
    review = get_object_or_404(RentReview, id=review_id, is_published=True)
    
    context = {
        'review': review,
    }
    return render(request, 'rentreviews/review_detail.html', context)


@require_authentication
def create_review(request):
    """Create a new rent review"""
    if request.method == 'GET':
        context = {
            'user_id': request.session.get('user_id'),
        }
        return render(request, 'rentreviews/create_review.html', context)


@csrf_exempt
@require_http_methods(["POST"])
@require_authentication
def create_review_submit(request):
    """Handle review creation form submission"""
    try:
        user_id = request.session.get('user_id')
        user = User.objects.get(id=user_id)
        
        # Get form data
        review_data = {
            'user': user,
            'property_address': request.POST.get('property_address'),
            'property_type': request.POST.get('property_type', ''),
            'bedrooms': request.POST.get('bedrooms', ''),
            'landlord_name': request.POST.get('landlord_name', ''),
            'landlord_type': request.POST.get('landlord_type', 'unknown'),
            'overall_rating': int(request.POST.get('overall_rating')),
            'title': request.POST.get('title'),
            'review_text': request.POST.get('review_text'),
            'rent_amount': request.POST.get('rent_amount', ''),
            'tenancy_duration': request.POST.get('tenancy_duration', ''),
            'would_recommend': request.POST.get('would_recommend') == 'on',
            'issues_reported': request.POST.get('issues_reported', ''),
        }
        
        # Optional specific ratings
        for rating_field in ['property_condition_rating', 'landlord_communication_rating', 
                           'value_for_money_rating', 'maintenance_response_rating']:
            rating_value = request.POST.get(rating_field)
            if rating_value:
                review_data[rating_field] = int(rating_value)
        
        # Create review
        review = RentReview.objects.create(**review_data)
        
        return JsonResponse({
            'success': True,
            'message': 'Review submitted successfully!',
            'review_id': review.id
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error submitting review: {str(e)}'
        }, status=400)


@require_authentication
def my_reviews(request):
    """Show current user's reviews"""
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, id=user_id)
    
    reviews = RentReview.objects.filter(user=user)
    
    context = {
        'reviews': reviews,
        'user': user,
    }
    return render(request, 'rentreviews/my_reviews.html', context)


@require_authentication
def review_my_rent(request):
    """Display rent review options page."""
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, id=user_id)
    
    context = {
        'user': user,
    }
    return render(request, 'rentreviews/review_my_rent.html', context)
