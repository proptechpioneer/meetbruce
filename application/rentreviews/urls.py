from django.urls import path
from . import views

app_name = 'rentreviews'

urlpatterns = [
    path('', views.review_list, name='review_list'),
    path('review/<int:review_id>/', views.review_detail, name='review_detail'),
    path('create/', views.create_review, name='create_review'),
    path('create/submit/', views.create_review_submit, name='create_review_submit'),
    path('my-reviews/', views.my_reviews, name='my_reviews'),
    path('review-my-rent/', views.review_my_rent, name='review_my_rent'),
]