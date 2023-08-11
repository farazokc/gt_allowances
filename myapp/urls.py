"""
URL configuration for allowances project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, re_path
from myapp import views

urlpatterns = [
    path("", views.index, name="Index"),
    path("Login/", views.Login, name="Login"),
    path('Home/', views.Home, name = 'Home'),
    path('Transport/', views.Trans_req, name = 'Transport_Request'),
    # path('Transport/request/', views.plan_trip, name = 'plan_trip'),
    path('Payment/', views.payment, name = 'Payment'),
    path('test/', views.Home, name = 'Test'),
    path('add_location/', views.Add_Locations, name = 'locations'),
    path('add_location/Location_request/', views.location_save, name = 'add_loc'),
    re_path(r'^Logout/$', views.Logout, name = 'Logout'),
    path('add_price/', views.add_petrol_price, name = 'pprice'),
    path('history/', views.history, name = 'history'),
]

