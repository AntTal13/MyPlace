from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from main_app.forms import UserCreationForm
from .models import UserProfile, Apartment

# Create your views here.
def home(request):
    return render(request, 'home.html')

def units_avail(request):
    units = Apartment.objects.filter(tenant__isnull=True)
    return render(request, 'units.html', { 'units':units })

def amenities(request):
    return render(request, 'amenities.html')

def apply(request):
    return render(request, 'apply.html')

def about(request):
    return render(request, 'about.html')

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('home')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)