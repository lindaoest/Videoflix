from django.db import models

class Genre(models.Model):
	name = models.CharField(max_length=566, blank=True, null=True)

	def __str__(self):
		return self.name

class Video(models.Model):
	title = models.CharField()
	created_at = models.DateTimeField(auto_now_add=True)
	video_file = models.FileField(upload_to='videos', blank=True, null=True)
	genre = models.ForeignKey(Genre, on_delete=models.CASCADE, null=True, blank=True)

	def __str__(self):
		return self.title
