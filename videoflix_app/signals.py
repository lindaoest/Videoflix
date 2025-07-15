from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from videoflix_app.models import Video
from videoflix_app.tasks import convert720p, convert1080p, convert480p
import os

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
	if created:
		convert1080p(instance, instance.video_file.path)
		convert720p(instance, instance.video_file.path)
		convert480p(instance, instance.video_file.path)

@receiver(post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Video` object is deleted.
    """
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)