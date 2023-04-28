from django.db import models
from django.contrib.auth.models import User
# from phonenumbers import PhoneNumber

# PERMISSIONS = (
#     ('T', 'Tenant'),
#     ('M', 'Manager'),
#     ('A', 'Admin')
# )

# Create your models here.

class UserProfile(models.Model):
    number = models.CharField(max_length=12)
    emergency_contact = models.CharField(max_length=100)
    emergency_number = models.CharField(max_length=12)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    # user_type = PERMISSIONS[0][0]

class Apartment(models.Model):
    floor = models.CharField(max_length=2)
    number = models.IntegerField()
    tenant = models.OneToOneField(UserProfile, on_delete=models.SET_NULL, null=True, blank=True)
    num_rooms = [
    (1, 'One Bedroom'),
    (2, 'Two Bedroom'),
    (3, 'Three Bedroom')
    ]

