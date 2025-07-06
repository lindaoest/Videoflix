from django.db import models

class Genre(models.Model):
	name = models.CharField(max_length=566, blank=True, null=True)

	def __str__(self):
		return self.name

class Video(models.Model):
	title = models.CharField()
	created_at = models.DateTimeField(auto_now_add=True)
	video_file = models.FileField(upload_to='videos/', blank=True, null=True)
	category = models.ForeignKey(Genre, on_delete=models.CASCADE, null=True, blank=True)
	description = models.TextField(max_length=366, blank=True)
	thumbnail_url = models.FileField(upload_to='thumbnails/', blank=True, null=True)

	def __str__(self):
		return self.title