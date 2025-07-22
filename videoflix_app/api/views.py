from rest_framework.views import APIView
from rest_framework.response import Response
from videoflix_app.models import Video
from videoflix_app.api.serializers import VideoSerializer
from rest_framework import status
from django.http import Http404, FileResponse, HttpResponse
from django.conf import settings
import os

# View to return a list of all available videos
class MediaView(APIView):

    def get(self, request, format=None):
        # Retrieve all video objects
        videos = Video.objects.all()
        # Serialize video data
        serializer = VideoSerializer(videos, many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)

# View to serve the HLS master playlist (.m3u8 file)
class HlsPlaylistView(APIView):

    def get(self, request, movie_id, resolution):
        # Build the path to the playlist file
        path = os.path.join(settings.MEDIA_ROOT, 'hls', str(movie_id), resolution, 'index.m3u8')

        # Raise 404 if playlist file does not exist
        if not os.path.exists(path):
            raise Http404("Playlist nicht gefunden")

        # Read and return playlist content
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        return HttpResponse(content, content_type='application/vnd.apple.mpegurl')

# View to serve video segments (.ts files) used in HLS streaming
class HlsSegmentView(APIView):

    def get(self, request, movie_id, resolution, segment):
        # Normalize segment name if it starts with "index.m3u8/"
        if segment.startswith("index.m3u8/"):
            # Delete "index.m3u8/" from segment
            segment = segment[len("index.m3u8/"):]

        # Build path to the segment file
        segment_path = os.path.join(settings.MEDIA_ROOT, 'hls', str(movie_id), resolution, 'segments', segment)

        # Raise 404 if segment file not found
        if not os.path.exists(segment_path):
            raise Http404("Segmentfile not found")

        # Return segment file as binary stream
        return FileResponse(open(segment_path, 'rb'), content_type='video/MP2T')