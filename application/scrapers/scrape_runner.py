import os
import django
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from threading import Thread
import logging

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
django.setup()

from .property_spiders import RightmoveSpider, ZooplaSpider, BestAgentSpider

logger = logging.getLogger(__name__)


class PropertyScrapeRunner:
    """
    Manages running Scrapy spiders within Django
    """
    
    def __init__(self):
        self.process = None
        self.is_running = False
    
    def run_scraping(self, property_type='house', bedrooms=4, location='london', sources=['rightmove']):
        """
        Run property scraping for given criteria
        
        Args:
            property_type (str): Type of property (house, flat)
            bedrooms (int): Number of bedrooms
            location (str): Location to search
            sources (list): List of sources to scrape ['rightmove', 'zoopla']
        
        Returns:
            dict: Results summary
        """
        if self.is_running:
            return {'success': False, 'message': 'Scraping already in progress'}
        
        try:
            self.is_running = True
            
            # Configure Scrapy settings
            settings = {
                'LOG_LEVEL': 'INFO',
                'ROBOTSTXT_OBEY': True,
                'DOWNLOAD_DELAY': 2,
                'RANDOMIZE_DOWNLOAD_DELAY': 0.5,
                'CONCURRENT_REQUESTS': 1,
                'USER_AGENT': 'Bruce Property Analysis Bot (+https://meetbruce.ai)',
                'FEEDS': {
                    'scraped_properties.json': {
                        'format': 'json',
                        'overwrite': True
                    }
                }
            }
            
            # Create crawler process
            process = CrawlerProcess(settings)
            
            # Add spiders to crawl
            if 'rightmove' in sources:
                process.crawl(
                    RightmoveSpider,
                    property_type=property_type,
                    bedrooms=str(bedrooms),
                    location=location
                )
            
            if 'zoopla' in sources:
                process.crawl(
                    ZooplaSpider,
                    property_type=property_type,
                    bedrooms=str(bedrooms),
                    location=location
                )
            
            if 'bestagent' in sources:
                process.crawl(
                    BestAgentSpider,
                    property_type=property_type,
                    bedrooms=str(bedrooms),
                    location=location
                )
            
            # Start crawling
            logger.info(f"Starting scraping for {bedrooms}-bedroom {property_type}s in {location}")
            process.start()  # This blocks until finished
            
            self.is_running = False
            
            return {
                'success': True,
                'message': f'Scraping completed for {property_type}s in {location}',
                'scraped_count': self._count_scraped_properties()
            }
            
        except Exception as e:
            self.is_running = False
            logger.error(f"Scraping error: {e}")
            return {
                'success': False,
                'message': f'Scraping failed: {str(e)}'
            }
    
    def run_scraping_async(self, property_type='house', bedrooms=4, location='london', sources=['rightmove']):
        """
        Run scraping in background thread to avoid blocking Django
        """
        def run_in_thread():
            return self.run_scraping(property_type, bedrooms, location, sources)
        
        thread = Thread(target=run_in_thread)
        thread.daemon = True
        thread.start()
        
        return {
            'success': True,
            'message': 'Scraping started in background'
        }
    
    def _count_scraped_properties(self):
        """Count properties scraped in current session"""
        from market_analysis.models import PropertyListing
        from django.utils import timezone
        from datetime import timedelta
        
        # Count properties scraped in last 5 minutes
        recent_time = timezone.now() - timedelta(minutes=5)
        return PropertyListing.objects.filter(
            scraped_at__gte=recent_time
        ).count()
    
    def get_scraping_status(self):
        """Get current scraping status"""
        return {
            'is_running': self.is_running,
            'total_properties': self._get_total_properties(),
            'recent_properties': self._count_scraped_properties()
        }
    
    def _get_total_properties(self):
        """Get total number of properties in database"""
        from market_analysis.models import PropertyListing
        return PropertyListing.objects.count()


# Global scraper runner instance
scraper_runner = PropertyScrapeRunner()


def run_market_analysis_scraping(user, property_type, bedrooms, location):
    """
    Function to be called from market analysis views
    
    Args:
        user: Django User instance
        property_type (str): Property type
        bedrooms (int): Number of bedrooms  
        location (str): Location to search
    
    Returns:
        int: Number of properties scraped
    """
    try:
        result = scraper_runner.run_scraping_async(
            property_type=property_type.lower(),
            bedrooms=bedrooms,
            location=location.lower(),
            sources=['rightmove']  # Start with just Rightmove
        )
        
        if result['success']:
            logger.info(f"Started scraping for user {user.name}: {property_type} in {location}")
            return result.get('scraped_count', 0)
        else:
            logger.error(f"Scraping failed: {result['message']}")
            return 0
            
    except Exception as e:
        logger.error(f"Error running scraping: {e}")
        return 0


def test_scraping():
    """Test function to run scraping manually"""
    runner = PropertyScrapeRunner()
    result = runner.run_scraping(
        property_type='house',
        bedrooms=4,
        location='london',
        sources=['rightmove']
    )
    print(f"Scraping result: {result}")
    return result