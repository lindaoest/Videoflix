from rest_framework import serializers
from videoflix_app.models import Video

class VideoSerializer(serializers.ModelSerializer):
	category = serializers.StringRelatedField()

	class Meta:
		model = Video
		fields = ['id', 'title', 'video_file', 'category', 'created_at', 'description', 'thumbnail_url']