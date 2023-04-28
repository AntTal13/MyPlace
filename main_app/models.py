from django.db import models
# from phonenumbers import PhoneNumber

# PERMISSIONS = (
#     ('T', 'Tenant'),
#     ('M', 'Manager'),
#     ('A', 'Admin')
# )

# Create your models here.

class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)
    number = models.CharField(max_length=12)
    emergency_contact = models.CharField(max_length=100)
    emergency_number = models.CharField(max_length=12)
    # user_type = PERMISSIONS[0][0]

class Apartment(models.Model):
    floor = models.CharField(max_length=2)
    number = models.IntegerField()
    tenant = models.OneToOneField(UserProfile, on_delete=models.SET_NULL, null=True)



