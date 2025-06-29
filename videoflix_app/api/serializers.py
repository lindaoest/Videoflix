from rest_framework import serializers
from videoflix_app.models import Video

class VideoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Video
		fields = ['id', 'title', 'video_file', 'genre']