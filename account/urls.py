"""
URL configuration for nepaMove project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),
    path("register/",views.RegistrationView.as_view(),name="register"),
    path('login/',views.CustomLoginView.as_view(),name='login'),
    path('logout/',views.CustomLogoutView.as_view(),name='logout'),
    path('get-csrf-token/',views.get_csrf_token,name="csrf_token"),
    path('driver/',include('Driver.urls'))
    # path('user/',views.UserView.as_view(),name="user"),
]
