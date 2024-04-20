from django.urls import path,include
from . import views

urlpatterns = [
    path('profile/<str:username>/', views.PassengerProfile.as_view(), name='passenger-profile'),
    # Add more URL patterns here if needed
]
