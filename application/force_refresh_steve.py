#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
django.setup()

from application.models import User
from market_analysis.models import MarketAnalysis

def force_refresh_steve_analysis():
    steve = User.objects.get(name__icontains='Steve')
    
    print('🗑️  Deleting all existing market analyses for Steve...')
    old_analyses = MarketAnalysis.objects.filter(user=steve)
    deleted_count = old_analyses.delete()[0]
    print(f'Deleted {deleted_count} old analyses')
    
    print('\n✅ Steve\'s market analysis cache cleared!')
    print('Next time he visits the rent review page, it will generate fresh analysis with correct pricing.')

if __name__ == '__main__':
    force_refresh_steve_analysis()