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
    path('maintenancerequests/', views.maintenance_request_index, name='maintenance_request_index'),
    path('maintenancerequests/<int:pk>/delete/', views.MaintenanceRequestDelete.as_view(), name='MaintenanceRequestDelete'),
    path('maintenancerequests/<int:pk>/update/', views.MaintenanceRequestUpdate.as_view(), name='MaintenanceRequestUpdate')
]
