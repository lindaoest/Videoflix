from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from videoflix_app.models import Video, Genre
from videoflix_app.api.serializers import VideoSerializer
from rest_framework import status

class MediaView(APIView):

    def get(self, request, format=None):
        categories = Genre.objects.all()

        grouped_data = []

        for category in categories:
            videos = Video.objects.filter(category=category)
            serialized_videos = VideoSerializer(videos, many=True, context={'request': request}).data

            grouped_data.append({
                'category': category.name,
                'videos': serialized_videos
            })

        return Response(grouped_data, status=status.HTTP_200_OK)

class HeroVideoView(APIView):

    def get(self, request, format=None):
        newest_video = Video.objects.order_by('-created_at')[0]
        serializer = VideoSerializer(newest_video, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)


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