from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from main_app.forms import UserCreationForm
from .models import UserProfile, Apartment

# Create your views here.
def home(request):
    return render(request, 'home.html')

def units_avail(request):
    units = Apartment.objects.filter(tenant__isnull=True)
    i=0
    j=0
    k=0
    for unit in units: 
        if unit.num_rooms == 1: 
            i+=1
        if unit.num_rooms == 2: 
            j+=1
        if unit.num_rooms == 3: 
            k+=1
    
    return render(request, 'units.html', { 'units':units, 'i':i,'j':j, 'k':k })

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

def profile(request, user_id):
    user = User.objects.get(id=user_id)
    userprofile = UserProfile.objects.get(user=user)
    return render(request, 'profile/profile.html', { 'user': user, 'userprofile': userprofile })



class UserProfileUpdate(UpdateView):
    model = UserProfile
    fields = ['number', 'emergency_contact', 'emergency_number']