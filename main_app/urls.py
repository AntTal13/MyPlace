from django.contrib import admin
from django.urls import path, include
from . import views
	
urlpatterns = [
    path('', views.home, name='home'),
    path('units/', views.units, name='units'),
    path('amenities/', views.amenities, name='amenities'),
    path('apply/', views.apply, name='apply'),
    path('about/', views.about, name='about'),
    path('accounts/signup/', views.signup, name='signup'),
]
