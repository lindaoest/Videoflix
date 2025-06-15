# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# import os

# @receiver(post_save, sender=MyModel)
# def video_post_save(sender, instance, created, **kwargs):
# 	print('Video wurde gespeichert')

# @receiver(post_delete, sender=Video)
# def auto_delete_file_on_delete(sender, instance, **kwargs):
#     """
#     Deletes file from filesystem
#     when corresponding `MediaFile` object is deleted.
#     """
#     if instance.video_file:
#         if os.path.isfile(instance.video_file.path):
#             os.remove(instance.video_file.path)
