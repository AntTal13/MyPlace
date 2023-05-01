from django.contrib import admin
from django.urls import path, include
from . import views
	
urlpatterns = [
    path('', views.home, name='home'),
    path('units/', views.units_avail, name='units'),
    path('amenities/', views.amenities, name='amenities'),
    path('apply/', views.apply, name='apply'),
    path('about/', views.about, name='about'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/<int:user_id>/', views.profile, name='profile'),
    path('profiles/<int:pk>/update/', views.UserProfileUpdate.as_view(), name='userprofile_update'),
    path('profiles/create/', views.UserProfileCreate.as_view(), name='UserProfileCreate'),
    path('user/<int:pk>/update/', views.UpdateUserForm.as_view(), name='UpdateUserForm'),
]
