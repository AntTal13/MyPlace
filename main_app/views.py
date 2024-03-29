from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django import forms
from .forms import UpdateUserForm, MaintenanceRequestForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from main_app.forms import UserCreationForm
from .models import UserProfile, Apartment, MaintenanceRequest
from django.urls import reverse_lazy
from django.utils import timezone
import os
from django.db.models import F

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

@login_required
def profile(request, user_id):
    user = User.objects.get(id=user_id)
    userprofile = UserProfile.objects.get(user=user)
    if request.method == 'POST':
        form = MaintenanceRequestForm(request.POST)
        if form.is_valid():
            newrequest = form.save(commit=False)
            newrequest.user = UserProfile.objects.get(user=request.user)
            newrequest.created_at = timezone.now()
            newrequest.updated_at = timezone.now()
            newrequest.save()
            return redirect('maintenance_request_index')
    else:
        form = MaintenanceRequestForm()

    return render(request, 'profile/profile.html', { 'user': user, 'userprofile': userprofile, 'form': form })

@login_required
def maintenance_request_index(request):
    requests = MaintenanceRequest.objects.all().order_by('created_at')
    return render(request, 'maintenancerequest/maintenancerequest.html', { 'requests' : requests })

@login_required
def assign_apartment(request, **kwargs):
    if request.method == 'POST':
        apartment_id = request.POST.get('apartment')
        userprofile_id = kwargs['pk']
        apartment = Apartment.objects.get(id=apartment_id)
        userprofile = UserProfile.objects.get(id=userprofile_id)
        apartment.tenant = userprofile
        apartment.save()
    return redirect('Unassigned_Applicants')

@login_required
def apartment_list(request):
    apartments = Apartment.objects.all().prefetch_related('tenant').annotate(fl=F('floor'), num=F('number')).order_by('fl', 'num')
    return render(request, 'property_manager/apartment_list.html', {'apartments': apartments})

@login_required
def remove_tenant(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    if apartment.tenant:
        apartment.tenant = None
        apartment.save()
    return redirect('apartment_list')

class UserProfileUpdate(LoginRequiredMixin, UpdateView):
    model = UserProfile
    fields = ['number', 'emergency_contact', 'emergency_number']

class UserProfileCreate(LoginRequiredMixin, CreateView):
    model = UserProfile
    fields = ['number', 'emergency_contact', 'emergency_number']

    def form_valid(self, form):
         user = self.request.user
         form.instance.user = user
         return super(UserProfileCreate, self).form_valid(form)
         
class UpdateUserForm(LoginRequiredMixin, UpdateView):
    form_class = UpdateUserForm
    template_name = "user/user_update.html"

    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        User = form.save(commit=False)
        User.save()
        return redirect('profile', user_id = User.id)
    
class MaintenanceRequestDelete(LoginRequiredMixin, DeleteView):
    model = MaintenanceRequest
    success_url = "/maintenancerequests"

class MaintenanceRequestUpdate(LoginRequiredMixin, UpdateView):
    model = MaintenanceRequest
    fields = ['title', 'content']

class UnassignedApplicants(LoginRequiredMixin, ListView):
    model = UserProfile
    template_name = 'property_manager/unassigned_applicants.html'

    def get_queryset(self):
        queryset = UserProfile.objects.filter(apartment__isnull=True)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unassigned_apartments'] = Apartment.objects.filter(tenant=None)
        return context

    def post(self, request, *args, **kwargs):
        apartment_id = request.POST.get('apartment')
        userprofile_id = kwargs['pk']
        apartment = Apartment.objects.get(id=apartment_id)
        userprofile = UserProfile.objects.get(id=userprofile_id)
        apartment.tenant = userprofile
        apartment.save()
        return redirect('Unassigned_Applicants')

class TenantInfo(LoginRequiredMixin, ListView):
    model = UserProfile
    template_name = 'property_manager/tenant_info.html'
    context_object_name = 'tenants'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(apartment__isnull=False).annotate(fl=F('apartment__floor'), num=F('apartment__number')).order_by('fl', 'num')
        return UserProfile.objects.filter(apartment__isnull=False).order_by('user__last_name')