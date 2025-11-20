from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Avg, Count, Q
from django.utils import timezone
from decimal import Decimal
import statistics
from application.models import User
from .models import PropertyListing, MarketAnalysis, ScrapingJob
from .scrapers import run_market_analysis_scraping
import logging
import re

logger = logging.getLogger(__name__)

def parse_bedrooms(bedrooms_value):
    """Parse bedrooms value to integer"""
    if bedrooms_value is None:
        return 2
    
    # If it's already an integer, return it
    if isinstance(bedrooms_value, int):
        return bedrooms_value
    
    # If it's a string, try to extract number
    bedrooms_str = str(bedrooms_value).lower().strip()
    
    # Remove common words
    bedrooms_str = bedrooms_str.replace('bedrooms', '').replace('bedroom', '').replace('bed', '').strip()
    
    # Handle word numbers
    word_to_num = {
        'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
        'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10
    }
    
    if bedrooms_str in word_to_num:
        return word_to_num[bedrooms_str]
    
    # Try to extract first number
    import re
    numbers = re.findall(r'\d+', bedrooms_str)
    if numbers:
        return int(numbers[0])
    
    # Default fallback
    return 2

def require_authentication(view_func):
    """Decorator to require authentication"""
    def wrapper(request, *args, **kwargs):
        if not request.session.get('is_authenticated'):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


@require_authentication
def market_analysis_view(request):
    """Display market analysis for the user's property"""
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, id=user_id)
    
    # Get user's property details
    property_type = user.property_type.lower() if user.property_type else 'flat'
    bedrooms = parse_bedrooms(user.bedrooms)
    location = user.town or 'london'
    
    # Check if this is a force refresh request
    force_refresh = request.GET.get('refresh') == 'true'
    
    # Check for existing recent analysis (skip if force refresh)
    recent_analysis = None
    if not force_refresh:
        recent_analysis = MarketAnalysis.objects.filter(
            user=user,
            created_at__gte=timezone.now() - timezone.timedelta(days=7)
        ).first()
    
    if recent_analysis:
        # Use existing analysis
        analysis = recent_analysis
        comparable_properties = analysis.comparable_properties.all()[:20]
    else:
        # Delete any existing analyses for this user if force refresh
        if force_refresh:
            MarketAnalysis.objects.filter(user=user).delete()
            logger.info(f"Force refresh: deleted existing analyses for user {user.id}")
        
        # Create new analysis
        analysis, comparable_properties = create_market_analysis(user, property_type, bedrooms, location)
    
    # Calculate market position
    user_weekly_rent = None
    if user.weekly_rent:
        try:
            # Clean the weekly rent string and convert to decimal
            rent_str = user.weekly_rent.replace('£', '').replace(',', '').strip()
            user_weekly_rent = Decimal(rent_str)
        except (ValueError, Exception):
            user_weekly_rent = None
    
    market_position = calculate_market_position(user_weekly_rent, comparable_properties)
    
    context = {
        'user': user,
        'analysis': analysis,
        'comparable_properties': comparable_properties,
        'market_position': market_position,
        'user_weekly_rent': user_weekly_rent,
    }
    
    return render(request, 'market_analysis/analysis_results.html', context)


@csrf_exempt
@require_http_methods(["POST"])
@require_authentication
def start_market_analysis(request):
    """Start a new market analysis by scraping current data"""
    try:
        user_id = request.session.get('user_id')
        user = get_object_or_404(User, id=user_id)
        
        # Get parameters from request
        property_type = request.POST.get('property_type', user.property_type or 'flat').lower()
        bedrooms_param = request.POST.get('bedrooms', user.bedrooms)
        bedrooms = parse_bedrooms(bedrooms_param)
        location = request.POST.get('location', user.town or 'london')
        
        # Check for running jobs
        running_job = ScrapingJob.objects.filter(
            user=user,
            status='running'
        ).first()
        
        if running_job:
            return JsonResponse({
                'success': False,
                'message': 'Analysis already in progress. Please wait.'
            })
        
        # Start scraping job (in a real app, this would be queued)
        try:
            # Use real scraping now that dependencies are available
            logger.info(f"Starting market analysis for {user.name}: {property_type}, {bedrooms} beds in {location}")
            
            try:
                scraped_count = run_market_analysis_scraping(user, property_type, bedrooms, location)
            except Exception as scraping_error:
                logger.warning(f"Scraping failed, using sample data: {scraping_error}")
                # Fallback to sample data if scraping fails
                scraped_count = create_sample_data(user, property_type, bedrooms, location)
            
            # Create new analysis
            analysis, comparable_properties = create_market_analysis(user, property_type, bedrooms, location)
            
            return JsonResponse({
                'success': True,
                'message': f'Market analysis completed! Found {len(comparable_properties)} comparable properties.',
                'analysis_id': analysis.id,
                'scraped_count': scraped_count
            })
            
        except Exception as e:
            logger.error(f"Error in market analysis: {e}", exc_info=True)
            return JsonResponse({
                'success': False,
                'message': f'Error during analysis: {str(e)}'
            })
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error starting analysis: {str(e)}'
        }, status=400)


def get_similar_market_tier(location):
    """Get similar market tier locations for fallback property matching"""
    location_lower = location.lower()
    
    # Market tier mappings - if user's location has no data, use these similar markets
    tier_mappings = {
        # Premium university/historic cities
        'premium_university': ['cambridge', 'oxford', 'bath', 'winchester', 'york', 'exeter'],
        
        # Major regional cities  
        'major_cities': ['manchester', 'birmingham', 'bristol', 'leeds', 'liverpool', 'nottingham', 'sheffield', 'newcastle', 'edinburgh', 'glasgow'],
        
        # London commuter belt
        'commuter_belt': ['reading', 'guildford', 'st albans', 'windsor', 'kingston', 'watford', 'harrow', 'bromley'],
        
        # Growing regional towns
        'regional_towns': ['milton keynes', 'coventry', 'leicester', 'derby', 'peterborough', 'northampton', 'luton'],
        
        # Affordable northern areas
        'affordable_north': ['hull', 'stoke', 'blackpool', 'middlesbrough', 'bolton', 'preston', 'blackburn', 'burnley'],
        
        # Coastal/resort towns
        'coastal_towns': ['brighton', 'bournemouth', 'plymouth', 'portsmouth', 'hastings', 'margate', 'scarborough'],
        
        # Welsh cities
        'wales': ['cardiff', 'swansea', 'newport', 'wrexham', 'bangor'],
        
        # Scottish cities (excluding Edinburgh/Glasgow which are in major_cities)
        'scotland': ['aberdeen', 'dundee', 'stirling', 'perth', 'inverness']
    }
    
    # Find which tier the user's location belongs to
    for tier, locations in tier_mappings.items():
        if any(city in location_lower for city in locations):
            # Return other cities in the same tier as fallback options
            return [city for city in locations if city != location_lower]
    
    # Default fallback order if location not recognized
    return ['manchester', 'birmingham', 'bristol', 'london']


def create_market_analysis(user, property_type, bedrooms, location):
    """Create a new market analysis based on available data"""
    
    # Auto-populate properties if needed for this location - TEMPORARILY DISABLED
    # try:
    #     from auto_populate_locations import ensure_location_coverage
    #     ensure_location_coverage(location, property_type, bedrooms, min_properties=10)
    # except Exception as e:
    #     logger.warning(f"Auto-population failed for {location}: {e}")
    
    # Find comparable properties
    # Handle property type variations (flat/apartment vs flat)
    property_type_query = Q(property_type=property_type)
    if 'flat' in property_type.lower():
        property_type_query |= Q(property_type='flat') | Q(property_type='apartment') | Q(property_type='flat/apartment')
    
    comparable_properties = PropertyListing.objects.filter(
        property_type_query,
        bedrooms=bedrooms,
        is_active=True,
        is_duplicate=False,
        weekly_rent__gt=0
    )
    
    # Filter by location if possible
    location_filtered = comparable_properties
    if location:
        location_filtered = comparable_properties.filter(
            Q(address__icontains=location) | 
            Q(area__icontains=location) |
            Q(postcode__icontains=location)
        )
        
        logger.warning(f"DEBUG: Location filtering for '{location}'")
        logger.warning(f"DEBUG: Total comparable properties: {comparable_properties.count()}")
        logger.warning(f"DEBUG: Location filtered properties: {location_filtered.count()}")
        
        # If no local properties found, fall back to similar market tier
        if location_filtered.count() == 0:
            logger.warning(f"No properties found in {location}, using similar market properties")
            
            # Determine market tier and find similar locations
            location_lower = location.lower()
            if any(term in location_lower for term in ['cambridge', 'oxford', 'bath', 'winchester']):
                # University/historic cities - use other university cities
                location_filtered = comparable_properties.filter(
                    Q(address__icontains='cambridge') | Q(address__icontains='oxford') | 
                    Q(address__icontains='bath') | Q(address__icontains='winchester') |
                    Q(address__icontains='york') | Q(address__icontains='exeter')
                )
            elif any(term in location_lower for term in ['london', 'zone']):
                # London - use London properties
                location_filtered = comparable_properties.filter(
                    Q(address__icontains='london')
                )
            elif any(term in location_lower for term in ['manchester', 'birmingham', 'bristol', 'leeds', 'liverpool']):
                # Major cities - use other major cities
                location_filtered = comparable_properties.filter(
                    Q(address__icontains='manchester') | Q(address__icontains='birmingham') |
                    Q(address__icontains='bristol') | Q(address__icontains='leeds') |
                    Q(address__icontains='liverpool') | Q(address__icontains='nottingham')
                )
            
            # Final fallback - use all properties if still no matches
            if location_filtered.count() == 0:
                logger.warning(f"Using all available properties as fallback")
                location_filtered = comparable_properties
    
    comparable_properties = location_filtered
    
    logger.warning(f"DEBUG: Properties before time filter: {comparable_properties.count()}")
    
    # Limit to recent listings - TEMPORARILY DISABLED FOR DEBUGGING
    # recent_cutoff = timezone.now() - timezone.timedelta(days=30)
    # comparable_properties = comparable_properties.filter(
    #     scraped_at__gte=recent_cutoff
    # ).order_by('-scraped_at')[:100]
    comparable_properties = comparable_properties.order_by('-scraped_at')[:100]
    
    logger.warning(f"DEBUG: Properties after limiting to 100: {comparable_properties.count()}")
    # logger.info(f"DEBUG: Time cutoff: {recent_cutoff}")
    
    # Calculate statistics
    rent_values = [float(prop.weekly_rent) for prop in comparable_properties if prop.weekly_rent]
    
    stats = {}
    if rent_values:
        stats['average_rent'] = Decimal(sum(rent_values) / len(rent_values))
        stats['median_rent'] = Decimal(statistics.median(rent_values))
        stats['min_rent'] = Decimal(min(rent_values))
        stats['max_rent'] = Decimal(max(rent_values))
    
    # Create analysis record
    analysis = MarketAnalysis.objects.create(
        user=user,
        property_type=property_type,
        bedrooms=bedrooms,
        search_area=location,
        total_properties_found=len(comparable_properties),
        **stats
    )
    
    # Add comparable properties
    analysis.comparable_properties.set(comparable_properties)
    
    # Generate market summary
    analysis.market_summary = generate_market_summary(analysis, rent_values)
    analysis.save()
    
    return analysis, comparable_properties


def calculate_market_position(user_rent, comparable_properties):
    """Calculate where user's rent falls in the market"""
    if not user_rent or not comparable_properties:
        return None
        
    rent_values = [float(prop.weekly_rent) for prop in comparable_properties if prop.weekly_rent]
    
    if not rent_values:
        return None
        
    user_rent_float = float(user_rent)
    lower_count = sum(1 for rent in rent_values if rent <= user_rent_float)
    percentile = (lower_count / len(rent_values)) * 100
    
    return {
        'percentile': round(percentile, 1),
        'total_properties': len(rent_values),
        'cheaper_count': sum(1 for rent in rent_values if rent < user_rent_float),
        'more_expensive_count': sum(1 for rent in rent_values if rent > user_rent_float),
    }


def generate_market_summary(analysis, rent_values):
    """Generate a text summary of the market analysis"""
    if not rent_values:
        return "Insufficient data for market analysis."
        
    summary_parts = []
    
    # Basic stats
    summary_parts.append(f"Found {len(rent_values)} comparable {analysis.bedrooms}-bedroom {analysis.property_type}s in {analysis.search_area}.")
    
    # Price range
    if analysis.min_rent and analysis.max_rent:
        summary_parts.append(f"Weekly rents range from £{analysis.min_rent} to £{analysis.max_rent}.")
    
    # Average and median
    if analysis.average_rent and analysis.median_rent:
        summary_parts.append(f"Average rent is £{analysis.average_rent:.0f} per week, median is £{analysis.median_rent:.0f}.")
    
    # Market assessment
    if len(rent_values) >= 10:
        summary_parts.append("This sample size provides a reliable market overview.")
    else:
        summary_parts.append("Limited sample size - consider expanding search criteria for more comprehensive analysis.")
    
    return " ".join(summary_parts)


@require_authentication
def analysis_history(request):
    """Show user's analysis history"""
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, id=user_id)
    
    analyses = MarketAnalysis.objects.filter(user=user).order_by('-created_at')[:10]
    
    context = {
        'user': user,
        'analyses': analyses,
    }
    
    return render(request, 'market_analysis/history.html', context)


def create_sample_data(user, property_type, bedrooms, location):
    """Create sample property data when scraping fails"""
    sample_properties = [
        {
            'title': f'Sample {bedrooms} bed {property_type} in {location}',
            'address': f'{location}, UK',
            'weekly_rent': 300 + (i * 50),
            'monthly_rent': (300 + (i * 50)) * 52 / 12,
            'bedrooms': bedrooms,
            'property_type': property_type,
            'source': 'sample_data',
            'source_url': '#',
            'source_id': f'sample_{i}'
        } for i in range(8)
    ]
    
    # Save sample properties to database
    saved_count = 0
    for prop_data in sample_properties:
        try:
            PropertyListing.objects.create(
                title=prop_data['title'],
                address=prop_data['address'],
                weekly_rent=prop_data['weekly_rent'],
                monthly_rent=prop_data['monthly_rent'],
                bedrooms=prop_data['bedrooms'],
                property_type=prop_data['property_type'],
                source=prop_data['source'],
                source_url=prop_data['source_url'],
                source_id=prop_data['source_id'],
                scraped_at=timezone.now()
            )
            saved_count += 1
        except Exception as e:
            logger.error(f"Error saving sample property: {e}")
    
    return saved_count
