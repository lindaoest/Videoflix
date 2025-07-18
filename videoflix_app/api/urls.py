from django.urls import path
from .views import MediaView, HlsSegmentView, HlsPlaylistView

urlpatterns = [
	# path('videos/', MediaView.as_view(), name='videos-list'),
	path('video/', MediaView.as_view(), name='video-list'),
	path('video/<int:movie_id>/<str:resolution>/index.m3u8/', HlsPlaylistView.as_view(), name='hls_playlist'),
	path('video/<int:movie_id>/<str:resolution>/<path:segment>/', HlsSegmentView.as_view(), name='hls_segment'),
]