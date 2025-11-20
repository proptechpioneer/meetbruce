import scrapy
import re
import os
import django
from urllib.parse import urljoin, urlparse
from decimal import Decimal
from datetime import datetime

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
django.setup()

from market_analysis.models import PropertyListing


class RightmoveSpider(scrapy.Spider):
    name = 'rightmove'
    allowed_domains = ['rightmove.co.uk']
    
    # Respectful scraping settings
    custom_settings = {
        'DOWNLOAD_DELAY': 2,  # 2 second delay between requests
        'RANDOMIZE_DOWNLOAD_DELAY': 0.5,  # Randomize delay (0.5 to 1.5 * DOWNLOAD_DELAY)
        'CONCURRENT_REQUESTS': 1,  # Only 1 concurrent request
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'ROBOTSTXT_OBEY': True,  # Respect robots.txt
        'USER_AGENT': 'Bruce Property Analysis Bot (+https://meetbruce.ai)',
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 1,
        'AUTOTHROTTLE_MAX_DELAY': 5,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 1.0,
    }
    
    def __init__(self, property_type='house', bedrooms='4', location='london', *args, **kwargs):
        super(RightmoveSpider, self).__init__(*args, **kwargs)
        self.property_type = property_type
        self.bedrooms = bedrooms
        self.location = location
        self.scraped_count = 0
    
    def start_requests(self):
        """Generate initial search URLs for Rightmove"""
        # Rightmove search URL format
        base_url = "https://www.rightmove.co.uk/property-to-rent/find.html"
        
        # Build search parameters
        params = {
            'searchType': 'RENT',
            'locationIdentifier': f'REGION^{self.location}',
            'insId': '1',
            'radius': '3.0',
            'minPrice': '',
            'maxPrice': '',
            'minBedrooms': self.bedrooms,
            'maxBedrooms': self.bedrooms,
            'displayPropertyType': self.property_type,
            'maxDaysSinceAdded': '30',  # Only recent listings
            'sortByPriceDescending': 'false',
            'primaryDisplayPropertyType': self.property_type,
            'secondaryDisplayPropertyType': '',
            'oldDisplayPropertyType': '',
            'oldPrimaryDisplayPropertyType': '',
            'newHome': '',
            'auction': 'false'
        }
        
        # Convert params to query string
        query_string = '&'.join([f'{k}={v}' for k, v in params.items() if v])
        search_url = f"{base_url}?{query_string}"
        
        yield scrapy.Request(
            url=search_url,
            callback=self.parse_search_results,
            meta={'search_params': params}
        )
    
    def parse_search_results(self, response):
        """Parse the search results page and extract property links"""
        # Extract property cards
        property_links = response.css('.propertyCard-link::attr(href)').getall()
        
        # Follow each property link
        for link in property_links[:20]:  # Limit to first 20 properties
            if link:
                full_url = urljoin(response.url, link)
                yield scrapy.Request(
                    url=full_url,
                    callback=self.parse_property,
                    meta=response.meta
                )
        
        # Follow pagination (optional - be careful not to scrape too much)
        next_page = response.css('.pagination-direction--next::attr(href)').get()
        if next_page and self.scraped_count < 50:  # Limit total properties
            yield scrapy.Request(
                url=urljoin(response.url, next_page),
                callback=self.parse_search_results,
                meta=response.meta
            )
    
    def parse_property(self, response):
        """Parse individual property page"""
        try:
            # Extract property details
            title = response.css('h1._2uQQ3SV0eMHL1P6t5ZDo2q::text').get()
            if not title:
                title = response.css('h1[data-testid="property-title"]::text').get()
            
            address = response.css('h2._1uI3IvdF5sIuBtRIGPd_FX::text').get()
            if not address:
                address = response.css('[data-testid="address-label"]::text').get()
            
            # Extract rent price
            price_text = response.css('._1gfnqJ3Vtd1z40MlC0MzXu span::text').get()
            if not price_text:
                price_text = response.css('[data-testid="rent-display"]::text').get()
            
            # Parse price
            weekly_rent = self.parse_rent(price_text)
            
            # Extract bedrooms from title or specific element
            bedrooms = self.extract_bedrooms(title, response)
            
            # Extract additional details
            description = ' '.join(response.css('[data-testid="property-description"] p::text').getall())
            
            # Create property data
            property_data = {
                'title': title or 'Property Title Not Found',
                'address': address or 'Address Not Found',
                'weekly_rent': weekly_rent,
                'monthly_rent': weekly_rent * 52 / 12 if weekly_rent else 0,
                'bedrooms': bedrooms or int(self.bedrooms),
                'property_type': self.property_type,
                'description': description[:500],  # Limit description length
                'source': 'property_portal_a',
                'source_url': response.url,
                'source_id': f'portal_a_{self.extract_property_id(response.url)}',
                'scraped_at': datetime.now()
            }
            
            # Save to database
            self.save_property(property_data)
            self.scraped_count += 1
            
            yield property_data
            
        except Exception as e:
            self.logger.error(f"Error parsing property {response.url}: {e}")
    
    def parse_rent(self, price_text):
        """Parse rent price from text"""
        if not price_text:
            return None
        
        # Remove currency symbols and extract numbers
        price_text = price_text.replace('£', '').replace(',', '').strip()
        
        # Look for weekly/monthly indicators
        if 'pw' in price_text.lower() or 'week' in price_text.lower():
            # Weekly rent
            match = re.search(r'(\d+(?:\.\d{2})?)', price_text)
            if match:
                return Decimal(match.group(1))
        elif 'pcm' in price_text.lower() or 'month' in price_text.lower():
            # Monthly rent - convert to weekly
            match = re.search(r'(\d+(?:\.\d{2})?)', price_text)
            if match:
                monthly_rent = Decimal(match.group(1))
                return monthly_rent * 12 / 52  # Convert to weekly
        else:
            # Try to extract any number
            match = re.search(r'(\d+(?:\.\d{2})?)', price_text)
            if match:
                return Decimal(match.group(1))
        
        return None
    
    def extract_bedrooms(self, title, response):
        """Extract number of bedrooms"""
        if title:
            # Look for patterns like "4 bed", "4 bedroom", etc.
            match = re.search(r'(\d+)\s*(?:bed|bedroom)', title.lower())
            if match:
                return int(match.group(1))
        
        # Try to find it in specific elements
        bedroom_element = response.css('[data-testid="beds-label"]::text').get()
        if bedroom_element:
            match = re.search(r'(\d+)', bedroom_element)
            if match:
                return int(match.group(1))
        
        return None
    
    def extract_property_id(self, url):
        """Extract property ID from URL"""
        match = re.search(r'/property-(\d+)/', url)
        if match:
            return f"rightmove_{match.group(1)}"
        return f"rightmove_{hash(url)}"
    
    def save_property(self, property_data):
        """Save property to Django database"""
        try:
            # Check if property already exists
            existing = PropertyListing.objects.filter(
                source_id=property_data['source_id']
            ).first()
            
            if existing:
                # Update existing property
                for key, value in property_data.items():
                    setattr(existing, key, value)
                existing.save()
                self.logger.info(f"Updated property: {property_data['title']}")
            else:
                # Create new property
                PropertyListing.objects.create(
                    **property_data,
                    is_active=True,
                    is_duplicate=False
                )
                self.logger.info(f"Created property: {property_data['title']}")
                
        except Exception as e:
            self.logger.error(f"Error saving property: {e}")


class ZooplaSpider(scrapy.Spider):
    name = 'zoopla'
    allowed_domains = ['zoopla.co.uk']
    
    # Similar settings to Rightmove
    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'RANDOMIZE_DOWNLOAD_DELAY': 0.5,
        'CONCURRENT_REQUESTS': 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'ROBOTSTXT_OBEY': True,
        'USER_AGENT': 'Bruce Property Analysis Bot (+https://meetbruce.ai)',
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 1,
        'AUTOTHROTTLE_MAX_DELAY': 5,
    }
    
    def __init__(self, property_type='house', bedrooms='4', location='london', *args, **kwargs):
        super(ZooplaSpider, self).__init__(*args, **kwargs)
        self.property_type = property_type
        self.bedrooms = bedrooms
        self.location = location
        self.scraped_count = 0
    
    def start_requests(self):
        """Generate initial search URLs for Zoopla"""
        # Zoopla search URL format
        search_url = f"https://www.zoopla.co.uk/to-rent/{self.location}/{self.bedrooms}-bedrooms/{self.property_type}s/"
        
        yield scrapy.Request(
            url=search_url,
            callback=self.parse_search_results
        )
    
    def parse_search_results(self, response):
        """Parse Zoopla search results - implement similar to Rightmove"""
        # This is a placeholder - would need to be implemented based on Zoopla's structure
        self.logger.info("Zoopla scraping not yet implemented")
        return []
    
    def parse_property(self, response):
        """Parse individual Zoopla property page"""
        pass


class BestAgentSpider(scrapy.Spider):
    """Spider for scraping BestAgent property listings"""
    name = 'bestagent'
    allowed_domains = ['bestagent.property']
    
    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'ROBOTSTXT_OBEY': True,
    }
    
    def __init__(self, property_type='flat', bedrooms='2', location='london', *args, **kwargs):
        super(BestAgentSpider, self).__init__(*args, **kwargs)
        self.property_type = property_type
        self.bedrooms = bedrooms
        self.location = location
        self.scraped_count = 0
        
        # Setup Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
        django.setup()
    
    def start_requests(self):
        """Generate initial requests for BestAgent property search"""
        # BestAgent search URL structure (example - would need to be verified)
        search_params = {
            'property_type': self.property_type,
            'bedrooms': self.bedrooms,
            'location': self.location
        }
        
        search_url = f"https://bestagent.property/search?property_type={self.property_type}&bedrooms={self.bedrooms}&location={self.location}"
        
        yield scrapy.Request(
            url=search_url,
            callback=self.parse_search_results,
            headers={
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-GB,en;q=0.5',
            }
        )
    
    def parse_search_results(self, response):
        """Parse BestAgent search results"""
        # Note: This would need to be implemented based on BestAgent's actual HTML structure
        # For now, we'll create a placeholder that logs the attempt
        
        self.logger.info(f"Attempting to parse BestAgent search results from {response.url}")
        
        # Placeholder selectors - would need to be updated based on actual site structure
        property_links = response.css('.property-card a::attr(href)').getall()
        
        if not property_links:
            # Try alternative selectors
            property_links = response.css('[data-testid="property-link"]::attr(href)').getall()
        
        # Follow property links
        for link in property_links[:15]:  # Limit scraping
            if link:
                full_url = urljoin(response.url, link)
                yield scrapy.Request(
                    url=full_url,
                    callback=self.parse_property,
                    meta={'property_url': full_url}
                )
        
        self.logger.info(f"Found {len(property_links)} property links on BestAgent")
    
    def parse_property(self, response):
        """Parse individual BestAgent property page"""
        try:
            # These selectors would need to be updated based on BestAgent's actual HTML
            title = response.css('h1.property-title::text').get()
            if not title:
                title = response.css('h1::text').get()
            
            address = response.css('.property-address::text').get()
            price_text = response.css('.property-price::text').get()
            bedrooms_text = response.css('.property-bedrooms::text').get()
            description = response.css('.property-description::text').getall()
            
            # Extract and process the data
            weekly_rent = self.extract_weekly_rent(price_text)
            bedrooms = self.extract_bedrooms(bedrooms_text, title)
            
            if weekly_rent and weekly_rent > 0:
                property_data = {
                    'title': title or 'BestAgent Property',
                    'address': address or 'London',
                    'weekly_rent': weekly_rent,
                    'monthly_rent': weekly_rent * 52 / 12,
                    'bedrooms': bedrooms or int(self.bedrooms),
                    'property_type': self.property_type,
                    'description': ' '.join(description[:3]) if description else '',
                    'source': 'premium_listings',  # Anonymous source
                    'source_url': response.url,
                    'source_id': f'bestagent_{self.extract_property_id(response.url)}',
                    'scraped_at': datetime.now()
                }
                
                # Save to database
                self.save_property(property_data)
                self.scraped_count += 1
                
                self.logger.info(f"Scraped BestAgent property: {title} - £{weekly_rent}/week")
        
        except Exception as e:
            self.logger.error(f"Error parsing BestAgent property {response.url}: {e}")
    
    def extract_weekly_rent(self, price_text):
        """Extract weekly rent from price text"""
        if not price_text:
            return None
            
        # Remove currency symbols and spaces
        price_clean = re.sub(r'[£,\s]', '', price_text)
        
        # Look for weekly rent patterns
        weekly_match = re.search(r'(\d+).*?(?:week|pw)', price_text.lower())
        if weekly_match:
            return int(weekly_match.group(1))
        
        # Look for monthly rent and convert
        monthly_match = re.search(r'(\d+).*?(?:month|pcm|pm)', price_text.lower())
        if monthly_match:
            monthly_rent = int(monthly_match.group(1))
            return int(monthly_rent * 12 / 52)  # Convert to weekly
        
        return None
    
    def extract_bedrooms(self, bedrooms_text, title):
        """Extract number of bedrooms"""
        if bedrooms_text:
            bedroom_match = re.search(r'(\d+)', bedrooms_text)
            if bedroom_match:
                return int(bedroom_match.group(1))
        
        # Fallback to title
        if title:
            bedroom_match = re.search(r'(\d+)\s*bed', title.lower())
            if bedroom_match:
                return int(bedroom_match.group(1))
        
        return None
    
    def extract_property_id(self, url):
        """Extract property ID from URL"""
        # Extract the last number from the URL
        matches = re.findall(r'\d+', url)
        if matches:
            return matches[-1]
        return str(hash(url))[:8]
    
    def save_property(self, property_data):
        """Save property to Django database"""
        try:
            from market_analysis.models import PropertyListing
            from django.utils import timezone
            
            # Check if property already exists
            existing = PropertyListing.objects.filter(
                source_id=property_data['source_id']
            ).first()
            
            if not existing:
                PropertyListing.objects.create(
                    title=property_data['title'],
                    address=property_data['address'],
                    weekly_rent=property_data['weekly_rent'],
                    monthly_rent=property_data['monthly_rent'],
                    bedrooms=property_data['bedrooms'],
                    property_type=property_data['property_type'],
                    description=property_data['description'],
                    source=property_data['source'],
                    source_url=property_data['source_url'],
                    source_id=property_data['source_id'],
                    scraped_at=timezone.now(),
                    is_active=True,
                    is_duplicate=False
                )
                self.logger.info(f"Saved BestAgent property: {property_data['title']}")
            else:
                self.logger.debug(f"Property already exists: {property_data['source_id']}")
                
        except Exception as e:
            self.logger.error(f"Error saving BestAgent property: {e}")