from django.core.mail import EmailMessage
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from rango.models import UserProfile

def send_confirmation_email(request, user):
    current_site = get_current_site(request)
    tk = PasswordResetTokenGenerator()
    message = render_to_string('auth/confirm_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': tk.make_token(user),
    })
    mail_subject = 'Activate your Rango account.'
    to_email = user.email
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()


def verify_confirmation_token(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    tk = PasswordResetTokenGenerator()
    if user is not None and tk.check_token(user, token):
        user_profile = UserProfile.objects.filter(user=user)[0]
        user_profile.confirmed = True
        user.save()
        user_profile.save()
        return user
    else:
        return None