from django.core.management.base import BaseCommand
from django.utils import timezone
from scrapers.scrape_runner import test_scraping
from market_analysis.models import PropertyListing


class Command(BaseCommand):
    help = 'Scrape property data using Scrapy'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--property-type',
            type=str,
            default='house',
            help='Property type to search for (house, flat)'
        )
        parser.add_argument(
            '--bedrooms',
            type=int,
            default=4,
            help='Number of bedrooms'
        )
        parser.add_argument(
            '--location',
            type=str,
            default='london',
            help='Location to search'
        )
        parser.add_argument(
            '--test',
            action='store_true',
            help='Run in test mode with limited scraping'
        )
    
    def handle(self, *args, **options):
        property_type = options['property_type']
        bedrooms = options['bedrooms']
        location = options['location']
        test_mode = options['test']
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Starting property scraping for {bedrooms}-bedroom {property_type}s in {location}'
            )
        )
        
        # Count existing properties
        initial_count = PropertyListing.objects.count()
        self.stdout.write(f'Properties in database before scraping: {initial_count}')
        
        try:
            if test_mode:
                self.stdout.write('Running in test mode...')
                # Run a limited test scraping
                result = test_scraping()
            else:
                # Import here to avoid circular imports
                from scrapers.scrape_runner import PropertyScrapeRunner
                
                runner = PropertyScrapeRunner()
                result = runner.run_scraping(
                    property_type=property_type,
                    bedrooms=bedrooms,
                    location=location,
                    sources=['rightmove']
                )
            
            if result['success']:
                final_count = PropertyListing.objects.count()
                new_properties = final_count - initial_count
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✅ Scraping completed successfully!'
                    )
                )
                self.stdout.write(f'Properties in database after scraping: {final_count}')
                self.stdout.write(f'New properties added: {new_properties}')
                self.stdout.write(f'Message: {result["message"]}')
            else:
                self.stdout.write(
                    self.style.ERROR(f'❌ Scraping failed: {result["message"]}')
                )
        
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error during scraping: {str(e)}')
            )
            # Show recent properties as fallback
            recent_properties = PropertyListing.objects.filter(
                scraped_at__gte=timezone.now() - timezone.timedelta(hours=24)
            ).count()
            self.stdout.write(f'Properties scraped in last 24 hours: {recent_properties}')
    
    def show_recent_properties(self):
        """Show recently scraped properties"""
        recent_properties = PropertyListing.objects.filter(
            scraped_at__gte=timezone.now() - timezone.timedelta(hours=1)
        ).order_by('-scraped_at')[:5]
        
        if recent_properties.exists():
            self.stdout.write('\nRecent properties:')
            for prop in recent_properties:
                self.stdout.write(f'- {prop.title[:50]}... | £{prop.weekly_rent}/week | {prop.address}')