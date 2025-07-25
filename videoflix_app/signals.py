from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from videoflix_app.models import Video
from videoflix_app.tasks import save_original_video
import os
import shutil
from django.conf import settings
import django_rq

# Signal for video after save
@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
	if created:
        # Create a queue
		queue = django_rq.get_queue('default', autocommit=True) # default heißt unser Queue in der stettings.py-Datei
		# Apply task save_original_video to queue
		queue.enqueue(save_original_video, instance.pk, instance.video_file.path)


# Signal for video after delete
@receiver(post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Video` object is deleted.
    """
    if instance.video_file:
        # Delete MP4 video
        video_path = os.path.join(settings.MEDIA_ROOT, 'videos', f"{instance.id}.mp4")
        if os.path.isfile(video_path):
            os.remove(video_path)

        # Delete thumbnail
        thumbnail_path = os.path.join(settings.MEDIA_ROOT, 'thumbnails', f"{instance.id}_thumb.jpg")
        if os.path.isfile(thumbnail_path):
            os.remove(thumbnail_path)

        # Delete HLS-files
        hls_dir = os.path.join(settings.MEDIA_ROOT, 'hls', str(instance.id))
        if os.path.isdir(hls_dir):
            shutil.rmtree(hls_dir)