from .models import UserProfile, Apartment, MaintenanceRequest


def user_profile(request):
    user_profile = None
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            pass
    return {'user_profile': user_profile}

def has_apartment(request):
    apartment = None
    if request.user.is_authenticated:
        user_profile = getattr(request.user, 'userprofile', None)
        if user_profile:
            apartment = Apartment.objects.filter(tenant=user_profile).first()
    return {'has_apartment': bool(apartment), 'apartment': apartment}

def has_maintenance_requests(request):
    maintenance_requests = []
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            maintenance_requests = MaintenanceRequest.objects.filter(user=user_profile)
        except UserProfile.DoesNotExist:
            pass

    context = {'maintenance_requests': maintenance_requests}

    return context

def is_property_manager(request):
    is_property_manager = False
    user_profile = None
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            is_property_manager = user_profile.is_property_manager
        except UserProfile.DoesNotExist:
            pass
    context = {'is_property_manager': is_property_manager}

    return context