from django.urls import path
from . import views

app_name = 'market_analysis'

urlpatterns = [
    path('', views.market_analysis_view, name='analysis'),
    path('start/', views.start_market_analysis, name='start_analysis'),
    path('history/', views.analysis_history, name='history'),
]