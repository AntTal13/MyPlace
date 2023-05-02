from .models import UserProfile, Apartment


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