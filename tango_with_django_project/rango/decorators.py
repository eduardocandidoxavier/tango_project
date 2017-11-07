from rango.models import UserProfile
from django.contrib import messages
from django.shortcuts import redirect


def user_email_confirmed(user):
    if UserProfile.objects.filter(user=user).count() < 1:
        return False
    user_profile = UserProfile.objects.filter(user=user)[0]
    return user_profile.confirmed


def user_email_confirmed2(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if UserProfile.objects.filter(user=user).count() < 1:
            messages.error(request, 'User not found!')
            return redirect('index')
        user_profile = UserProfile.objects.filter(user=user)[0]
        if user_profile.confirmed:
            return function(request, *args, **kwargs)
        else:
            messages.error(request, 'You have to confirm your account!')
            return redirect('index')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
