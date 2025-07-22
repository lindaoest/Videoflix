from rest_framework import serializers
from videoflix_app.models import Video

# Serializer for the Video model
class VideoSerializer(serializers.ModelSerializer):
    # Return the category as a string (using __str__ method of the related model)
    category = serializers.StringRelatedField()

    class Meta:
        model = Video
        # Fields to be included in the serialized output
        fields = ['id', 'title', 'video_file', 'category', 'created_at', 'description', 'thumbnail_url']