from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('property/', views.property_details, name='property_details'),
    path('insights/', views.rental_insights, name='rental_insights'),
    path('chat/', views.chat_with_bruce, name='chat_with_bruce'),
]