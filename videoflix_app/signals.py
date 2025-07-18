from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from videoflix_app.models import Video
from videoflix_app.tasks import saveOriginalVideo, convert720p, convert1080p, convert480p
import os
import shutil
from django.conf import settings

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
	if created:
		saveOriginalVideo(instance, instance.video_file.path)
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