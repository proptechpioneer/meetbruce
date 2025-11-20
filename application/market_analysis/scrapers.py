import requests
from bs4 import BeautifulSoup
import time
import random
from urllib.parse import urljoin, urlparse, parse_qs
import re
from decimal import Decimal
from datetime import datetime
from .models import PropertyListing, ScrapingJob
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

# Try to import Scrapy runner, fallback to basic scraping if not available
try:
    from scrapers.scrape_runner import scraper_runner
    SCRAPY_AVAILABLE = True
except ImportError:
    SCRAPY_AVAILABLE = False
    logger.warning("Scrapy not available, using basic scraping")


def run_market_analysis_scraping(user, property_type='house', bedrooms=4, location='london'):
    """
    Run comprehensive market analysis scraping
    Uses the new simple scraper that works reliably
    """
    
    # Create scraping job
    job = ScrapingJob.objects.create(
        user=user,
        property_type=property_type,
        bedrooms=bedrooms,
        location=location,
        status='running',
        started_at=timezone.now()
    )
    
    try:
        # Import the working simple scraper
        from simple_scraper import run_property_scraping
        
        logger.info(f"Running property scraping for {property_type}s in {location}")
        
        # Run the scraping
        saved_count = run_property_scraping(
            property_type=property_type.lower(),
            bedrooms=bedrooms,
            location=location.lower()
        )
        
        # Update job status
        job.status = 'completed'
        job.properties_scraped = saved_count
        job.completed_at = timezone.now()
        job.save()
        
        logger.info(f"Scraping completed: {saved_count} properties saved")
        return saved_count
        
    except Exception as e:
        job.status = 'failed'
        job.error_message = str(e)
        job.completed_at = timezone.now()
        job.save()
        
        logger.error(f"Scraping failed: {e}")
        return 0


def run_basic_scraping(user, property_type='house', bedrooms=4, location='london'):
    """
    Basic fallback scraping implementation
    """
    logger.info("Running basic scraping fallback")
    
    # Create some sample data if scraping fails
    sample_properties = [
        {
            'title': f'{bedrooms} Bedroom {property_type.title()} - {location.title()} Central',
            'address': f'{location.title()}, UK',
            'weekly_rent': Decimal('1800'),
            'monthly_rent': Decimal('1800') * 52 / 12,
            'bedrooms': bedrooms,
            'property_type': property_type.lower(),
            'source': 'sample_data',
            'source_url': '#',
            'source_id': f'sample_{int(time.time())}_1',
            'scraped_at': timezone.now(),
            'is_active': True,
            'is_duplicate': False
        },
        {
            'title': f'{bedrooms} Bed {property_type.title()} - Modern & Spacious',
            'address': f'{location.title()}, UK', 
            'weekly_rent': Decimal('2100'),
            'monthly_rent': Decimal('2100') * 52 / 12,
            'bedrooms': bedrooms,
            'property_type': property_type.lower(),
            'source': 'sample_data',
            'source_url': '#',
            'source_id': f'sample_{int(time.time())}_2',
            'scraped_at': timezone.now(),
            'is_active': True,
            'is_duplicate': False
        }
    ]
    
    saved_count = 0
    for prop_data in sample_properties:
        try:
            listing, created = PropertyListing.objects.get_or_create(
                source_id=prop_data['source_id'],
                defaults=prop_data
            )
            if created:
                saved_count += 1
                logger.info(f"Created sample property: {prop_data['title']}")
        except Exception as e:
            logger.error(f"Error creating sample property: {e}")
    
    return saved_count


# Keep the existing scraper classes for backward compatibility
class PropertyScraper:
    """Base class for property website scrapers"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def random_delay(self, min_seconds=1, max_seconds=3):
        """Add random delay between requests to be respectful"""
        time.sleep(random.uniform(min_seconds, max_seconds))
        
    def extract_price(self, price_text):
        """Extract price from various formats"""
        if not price_text:
            return None
            
        # Remove currency symbols and common text
        price_text = re.sub(r'[£$€,]', '', price_text)
        price_text = re.sub(r'per week|pw|pcm|per month', '', price_text, flags=re.IGNORECASE)
        
        # Extract numbers
        price_match = re.search(r'(\d+(?:\.\d{2})?)', price_text)
        if price_match:
            return Decimal(price_match.group(1))
        return None


class RightmoveScraper(PropertyScraper):
    """Scraper for Rightmove property listings"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.rightmove.co.uk"
        
    def build_search_url(self, location, property_type='', min_bedrooms=1, max_bedrooms=None, radius=2):
        """Build Rightmove search URL"""
        # This is a simplified URL structure - would need location ID mapping
        search_url = f"{self.base_url}/property-to-rent/find.html"
        params = {
            'searchType': 'RENT',
            'locationIdentifier': location,  # Would need to convert location to Rightmove ID
            'minBedrooms': min_bedrooms,
            'radius': radius,
        }
        
        if max_bedrooms:
            params['maxBedrooms'] = max_bedrooms
            
        return search_url
        
    def scrape_listings(self, location, property_type='flat', bedrooms=2, max_results=50):
        """Scrape property listings from Rightmove"""
        listings = []
        
        try:
            # Build search URL
            search_url = self.build_search_url(location, property_type, bedrooms, bedrooms + 1)
            
            logger.info(f"Scraping Rightmove: {search_url}")
            response = self.session.get(search_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find property listings (this selector would need to be updated based on current Rightmove structure)
            property_cards = soup.find_all('div', class_='l-searchResult')[:max_results]
            
            for card in property_cards:
                try:
                    listing_data = self.extract_listing_data(card, property_type)
                    if listing_data:
                        listings.append(listing_data)
                        
                    self.random_delay(0.5, 1.5)
                    
                except Exception as e:
                    logger.error(f"Error extracting listing data: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error scraping Rightmove: {e}")
            
        return listings
        
    def extract_listing_data(self, card, property_type='flat'):
        """Extract data from a single property card"""
        try:
            # Extract title
            title_elem = card.find('h2', class_='propertyCard-title')
            title = title_elem.get_text(strip=True) if title_elem else ''
            
            # Extract address
            address_elem = card.find('address', class_='propertyCard-address')
            address = address_elem.get_text(strip=True) if address_elem else ''
            
            # Extract price
            price_elem = card.find('span', class_='propertyCard-priceValue')
            price_text = price_elem.get_text(strip=True) if price_elem else ''
            weekly_rent = self.extract_price(price_text)
            
            # Extract bedrooms
            bedrooms_elem = card.find('span', class_='propertyCard-bedrooms')
            bedrooms_text = bedrooms_elem.get_text(strip=True) if bedrooms_elem else '0'
            bedrooms = int(re.search(r'(\d+)', bedrooms_text).group(1)) if re.search(r'(\d+)', bedrooms_text) else 0
            
            # Extract property link
            link_elem = card.find('a', class_='propertyCard-link')
            property_url = urljoin(self.base_url, link_elem['href']) if link_elem else ''
            
            # Extract property ID from URL
            property_id = self.extract_property_id(property_url)
            
            return {
                'title': title,
                'address': address,
                'weekly_rent': weekly_rent,
                'monthly_rent': weekly_rent * 52 / 12 if weekly_rent else None,
                'bedrooms': bedrooms,
                'source_url': property_url,
                'source_id': property_id,
                'source': 'rightmove',
                'property_type': property_type,
            }
            
        except Exception as e:
            logger.error(f"Error extracting listing data: {e}")
            return None
            
    def extract_property_id(self, url):
        """Extract property ID from Rightmove URL"""
        match = re.search(r'/property-(\d+)', url)
        return match.group(1) if match else str(hash(url))


class OpenRentScraper(PropertyScraper):
    """Scraper for OpenRent property listings"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.openrent.co.uk"
        
    def scrape_listings(self, location, property_type='flat', bedrooms=2, max_results=50):
        """Scrape property listings from OpenRent"""
        listings = []
        
        try:
            # Build search URL for OpenRent
            search_url = f"{self.base_url}/properties-to-rent/{location.lower()}"
            params = {
                'term': location,
                'bedrooms': bedrooms,
                'prices_min': 0,
                'prices_max': 10000,
            }
            
            logger.info(f"Scraping OpenRent: {search_url}")
            response = self.session.get(search_url, params=params)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find property listings
            property_cards = soup.find_all('div', class_='pli')[:max_results]
            
            for card in property_cards:
                try:
                    listing_data = self.extract_listing_data(card, property_type)
                    if listing_data:
                        listings.append(listing_data)
                        
                    self.random_delay(0.5, 1.5)
                    
                except Exception as e:
                    logger.error(f"Error extracting OpenRent listing: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error scraping OpenRent: {e}")
            
        return listings
        
    def extract_listing_data(self, card, property_type='flat'):
        """Extract data from OpenRent property card"""
        try:
            # Extract title and address
            title_elem = card.find('h2')
            title = title_elem.get_text(strip=True) if title_elem else ''
            
            # Extract price
            price_elem = card.find('span', class_='price')
            price_text = price_elem.get_text(strip=True) if price_elem else ''
            weekly_rent = self.extract_price(price_text)
            
            # Extract bedrooms
            beds_elem = card.find('span', class_='beds')
            bedrooms = int(beds_elem.get_text(strip=True)) if beds_elem and beds_elem.get_text(strip=True).isdigit() else 1
            
            # Extract property link
            link_elem = card.find('a')
            property_url = urljoin(self.base_url, link_elem['href']) if link_elem else ''
            
            # Extract property ID
            property_id = property_url.split('/')[-1] if property_url else str(hash(title))
            
            return {
                'title': title,
                'address': title,  # OpenRent often includes address in title
                'weekly_rent': weekly_rent,
                'monthly_rent': weekly_rent * 52 / 12 if weekly_rent else None,
                'bedrooms': bedrooms,
                'source_url': property_url,
                'source_id': property_id,
                'source': 'openrent',
                'property_type': property_type,
            }
            
        except Exception as e:
            logger.error(f"Error extracting OpenRent listing: {e}")
            return None


def run_market_analysis_scraping(user, property_type='flat', bedrooms=2, location='london'):
    """Run comprehensive market analysis by scraping multiple sources"""
    
    # Create scraping job
    job = ScrapingJob.objects.create(
        user=user,
        property_type=property_type,
        bedrooms=bedrooms,
        location=location,
        status='running',
        started_at=timezone.now()
    )
    
    all_listings = []
    
    try:
        # Initialize scrapers
        rightmove_scraper = RightmoveScraper()
        openrent_scraper = OpenRentScraper()
        
        # Scrape Rightmove
        logger.info("Starting Rightmove scraping...")
        rightmove_listings = rightmove_scraper.scrape_listings(location, property_type, bedrooms)
        all_listings.extend(rightmove_listings)
        
        time.sleep(2)  # Delay between different sites
        
        # Scrape OpenRent
        logger.info("Starting OpenRent scraping...")
        openrent_listings = openrent_scraper.scrape_listings(location, property_type, bedrooms)
        all_listings.extend(openrent_listings)
        
        # Save listings to database
        saved_count = 0
        for listing_data in all_listings:
            try:
                if listing_data.get('weekly_rent') and listing_data.get('title'):
                    listing, created = PropertyListing.objects.get_or_create(
                        source=listing_data['source'],
                        source_id=listing_data['source_id'],
                        defaults=listing_data
                    )
                    if created:
                        saved_count += 1
            except Exception as e:
                logger.error(f"Error saving listing: {e}")
                
        # Update job status
        job.status = 'completed'
        job.completed_at = timezone.now()
        job.properties_scraped = saved_count
        job.save()
        
        logger.info(f"Scraping completed. {saved_count} new properties saved.")
        return saved_count
        
    except Exception as e:
        # Update job with error
        job.status = 'failed'
        job.error_message = str(e)
        job.completed_at = timezone.now()
        job.save()
        
        logger.error(f"Scraping failed: {e}")
        raise e