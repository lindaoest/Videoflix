from django.db.models.signals import post_save
from django.dispatch import receiver
import os
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
import os
from auth_app.api.views import resetPassword
from django.core.mail import EmailMultiAlternatives

@receiver(post_save, sender=User)
def send_email_registration(sender, instance, created, **kwargs):
    token = default_token_generator.make_token(instance)
    uid = urlsafe_base64_encode(force_bytes(instance.pk))
    activation_path = reverse('activateRegistration-list', kwargs={'uidb64': uid, 'token': token})
    activation_link = f"http://localhost:8000/{activation_path}"
    confirmation_msg = render_to_string('confirmation-registration-email.html', {'username': instance.username, 'activation_link': activation_link})

    if created:
        send_mail(
            "Confirm your email",
            confirmation_msg,
            os.environ.get("EMAIL_HOST_USER"),
            [instance.email],
            fail_silently=False,
        )

@receiver(resetPassword)
def send_email_reset_password(sender, instance, created, **kwargs):
    # user = kwargs.get('user')
    token = default_token_generator.make_token(instance)
    uid = urlsafe_base64_encode(force_bytes(instance.pk))
    activation_path = reverse('password-confirm-list', kwargs={'uidb64': uid, 'token': token})
    activation_link = f"http://localhost:4200/confirm-password/{uid}/{token}"
    confirmation_msg_text = render_to_string('password_confirm-email.txt', {'activation_link': activation_link})
    confirmation_msg_html = render_to_string('password_confirm-email.html', {'activation_link': activation_link})

    if created:
        msg = EmailMultiAlternatives(
            "Reset your password",
            confirmation_msg_text,
            os.environ.get("EMAIL_HOST_USER"),
            [instance.email],
        )

        msg.attach_alternative(confirmation_msg_html, "text/html")
        msg.send()