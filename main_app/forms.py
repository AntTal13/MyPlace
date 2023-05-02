from django import forms
from .models import UserProfile, Apartment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import MaintenanceRequest
from django.utils import timezone


class UserCreationForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('first_name','last_name', 'username', 'email', 'password1' ,'password2')

# class UpdateUserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = '__all__'

class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True,)

    class Meta:
        model = User
        fields = ['username', 'email']

class MaintenanceRequestForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = ['title', 'apartment', 'content']

    def save(self, request, commit=True):
        instance = super().save(commit=False)
        instance.user = UserProfile.objects.get(user=request.user)
        instance.created_at = timezone.now()
        instance.updated_at = timezone.now()
        if commit:
            instance.save()
        return instance
