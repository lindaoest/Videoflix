from django.urls import path
from .views import MediaView

urlpatterns = [
	path('videos/', MediaView.as_view(), name='videos-list')
]