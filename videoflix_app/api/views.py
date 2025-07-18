from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from videoflix_app.models import Video, Genre
from videoflix_app.api.serializers import VideoSerializer
from rest_framework import status
from django.http import Http404, FileResponse, HttpResponse
from django.conf import settings
import os
from rest_framework.permissions import AllowAny

# class MediaView(APIView):

#     def get(self, request, format=None):
#         categories = Genre.objects.all()

#         grouped_data = []

#         for category in categories:
#             videos = Video.objects.filter(category=category)
#             serialized_videos = VideoSerializer(videos, many=True, context={'request': request}).data

#             grouped_data.append({
#                 'category': category.name,
#                 'videos': serialized_videos
#             })

#         return Response(grouped_data, status=status.HTTP_200_OK)

class MediaView(APIView):

    def get(self, request, format=None):
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)

class HeroVideoView(APIView):

    def get(self, request, format=None):
        newest_video = Video.objects.order_by('-created_at')[0]
        serializer = VideoSerializer(newest_video, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)

class HlsPlaylistView(APIView):

    def get(self, request, movie_id, resolution):
        path = os.path.join(settings.MEDIA_ROOT, 'hls', str(movie_id), resolution, 'index.m3u8')
        if not os.path.exists(path):
            raise Http404("Playlist nicht gefunden")

        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        return HttpResponse(content, content_type='application/vnd.apple.mpegurl')

class HlsSegmentView(APIView):

    def get(self, request, movie_id, resolution, segment):
        if segment.startswith("index.m3u8/"):
            # Delete "index.m3u8/" from segment
            segment = segment[len("index.m3u8/"):]

        segment_path = os.path.join(settings.MEDIA_ROOT, 'hls', str(movie_id), resolution, 'segments', segment)

        if not os.path.exists(segment_path):
            raise Http404("Segmentfile not found")

        return FileResponse(open(segment_path, 'rb'), content_type='video/MP2T')

# class MediaView(generics.ListAPIView):
#     queryset = Video.objects.all()
#     serializer_class = VideoSerializer

#     def list(self, request):
#         # Note the use of `get_queryset()` instead of `self.queryset`
#         queryset = self.get_queryset()
#         serializer = VideoSerializer(queryset, many=True)
#         genres = Genre.objects.all()

#         data = serializer.data
#         test = []

#         for genre in genres:
#             test.append({
#                 "genre": genre,
#                 "videos": Video.objects.filter(genre=genre)
#             })


#         return Response(data)