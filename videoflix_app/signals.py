from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from videoflix_app.models import Video
from videoflix_app.tasks import convert720p
import os
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
import os

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
	if created:
		convert720p(instance, instance.video_file.path)

@receiver(post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Video` object is deleted.
    """
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)

@receiver(post_save, sender=User)
def send_email_registration(sender, instance, created, **kwargs):
    token = default_token_generator.make_token(instance)
    uid = urlsafe_base64_encode(force_bytes(instance.pk))
    activation_path = reverse('activate', kwargs={'uidb64': uid, 'token': token})
    activation_link = f"http://localhost:8000/{activation_path}"
    confirmation_msg = render_to_string('templates/confirmation-registration-email.html', {'username': instance.username, 'activation_link': activation_link})

    if created:
        send_mail(
            "Confirm your email",
            confirmation_msg,
            os.environ.get("EMAIL_HOST_USER"),
            [instance.email],
            fail_silently=False,
        )