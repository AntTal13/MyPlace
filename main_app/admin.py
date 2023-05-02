from django.contrib import admin
from .models import UserProfile, Apartment, MaintenanceRequest

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Apartment)
admin.site.register(MaintenanceRequest)