from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class MediaView(APIView):
	permission_classes = [IsAuthenticated]

	def get(self, request):
		return Response('Hello World')