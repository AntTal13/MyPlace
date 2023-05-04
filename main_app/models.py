from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

ROOMS = (
    (1, 'One Bedroom'),
    (2, 'Two Bedroom'),
    (3, 'Three Bedroom')
    )

# Create your models here.

class UserProfile(models.Model):
    number = models.CharField(max_length=12)
    emergency_contact = models.CharField(max_length=100)
    emergency_number = models.CharField(max_length=12)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    is_property_manager = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def get_absolute_url(self):
        return reverse('profile', kwargs={'user_id': self.user.id})

class Apartment(models.Model):
    floor = models.CharField(max_length=2)
    number = models.IntegerField()
    tenant = models.OneToOneField(UserProfile, on_delete=models.SET_NULL, null=True, blank=True)
    num_rooms = models.IntegerField(
        choices=ROOMS,
        default=ROOMS[0][0]
    )

    def __str__(self):
        return f"{self.floor}-{self.number}"

class MaintenanceRequest(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE, null=True)
    apartment = models.ForeignKey('Apartment', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('maintenance_request_index')
