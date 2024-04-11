
from django.urls import path
from . import views

# app_name ='Driver'
urlpatterns = [
    path("<str:username>/",views.DriverProfile.as_view(),name="profile"),
    path("",views.VehicleView.as_view(),name="vehicle"),
    path("vehicle/<str:licence_plate_number>/",views.VehicleDetailView.as_view(),name="licence-plate-number"),
    path("trip/tripview/",views.TripView.as_view(),name="trip"),
    path("trip/tripview/<str:tripid>/",views.TripDetail.as_view(), name="trip-detail"),
    path("trip/trip-price/",views.TripPriceView.as_view(), name="trip-price"),
    path("trip/trip-price/<str:trip_price_id>/",views.TripPriceDetailView.as_view(), name="trip-price-detail"),
    path("trip/booking/",views.BookingView.as_view(), name="trip-booking"),
    path("trip/booking/<str:booking_id>/",views.BookingDetail.as_view(), name="trip-booking-detail"),
    
    
    # path("vechile/test/",views.Test.as_view(),name="test"),
    # path('user/',views.UserView.as_view(),name="user"),
]
