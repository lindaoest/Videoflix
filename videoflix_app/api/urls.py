from django.urls import path
from .views import MediaView, HeroVideoView

urlpatterns = [
	path('videos/', MediaView.as_view(), name='videos-list'),
	path('video/', HeroVideoView.as_view(), name='video-list')
]