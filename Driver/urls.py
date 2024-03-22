
from django.urls import path
from . import views

urlpatterns = [
    path("<str:username>/",views.DriverProfile.as_view(),name="profile")
    # path('user/',views.UserView.as_view(),name="user"),
]
