from django.db import models

# Create your models here.
class Video(models.Model):
	title = models.CharField()
	created_at = models.DateTimeField(auto_now_add=True)
	video_file = models.FileField(upload_to='videos', blank=True, null=True)

	def __str__(self):
		return self.title
