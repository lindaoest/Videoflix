from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
import os
from auth_app.api.views import resetPassword
from auth_app.tasks import send_email_registration_task, send_email_reset_password_task
import django_rq

# Signal for user registration
@receiver(post_save, sender=User)
def send_email_registration(sender, instance, created, **kwargs):
    # Create token
    token = default_token_generator.make_token(instance)
    # Encode user ID into base64
    uid = urlsafe_base64_encode(force_bytes(instance.pk))
    # Create activation link
    activation_path = reverse('activateRegistration-list', kwargs={'uidb64': uid, 'token': token})
    # activation_link = f"http://localhost:8000{activation_path}"
    activation_link = f"http://127.0.0.1:5500/pages/auth/activate.html?uid={uid}&token={token}"
    # Apply template
    confirmation_msg_text = render_to_string('confirmation-registration-email.txt', {'username': instance.username, 'activation_link': activation_link})
    confirmation_msg_html = render_to_string('confirmation-registration-email.html', {'username': instance.username, 'activation_link': activation_link})

    if created:
        # Create a queue
        queue = django_rq.get_queue('default', autocommit=True)
        # Apply task send_email_registration_task to queue
        queue.enqueue(send_email_registration_task, instance, confirmation_msg_text, confirmation_msg_html)

@receiver(resetPassword)
def send_email_reset_password(sender, instance, created, **kwargs):
    # Create token
    token = default_token_generator.make_token(instance)
    # Encode user ID into base64
    uid = urlsafe_base64_encode(force_bytes(instance.pk))
    # Create activation link
    activation_path = reverse('password-confirm-list', kwargs={'uidb64': uid, 'token': token})
    activation_link = f"http://127.0.0.1:5500/pages/auth/confirm_password.html?uid={uid}&token={token}"
    # Apply template
    confirmation_msg_text = render_to_string('password_confirm-email.txt', {'activation_link': activation_link})
    confirmation_msg_html = render_to_string('password_confirm-email.html', {'activation_link': activation_link})

    if created:
        # Create a queue
        queue = django_rq.get_queue('default', autocommit=True)
        # Apply task send_email_reset_password_task to queue
        queue.enqueue(send_email_reset_password_task, instance, confirmation_msg_text, confirmation_msg_html)