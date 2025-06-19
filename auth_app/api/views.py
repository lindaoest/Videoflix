from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User
from auth_app.api.serializers import RegistrationSerializer

""" View for user registration - anyone can access """
class RegistrationView(APIView):
	permission_classes = [AllowAny]

	def post(self, request, *args, **kwargs):
		serializer = RegistrationSerializer(data=request.data)

		# Check if input data is valid
		if serializer.is_valid():
			# Save user and create a token
			user = serializer.save()
			token, created = Token.objects.get_or_create(user=user)

			# Return token and user info in response
			return Response({
				'token': token.key,
				'user_id': user.pk,
				'email': user.email,
			}, status=status.HTTP_201_CREATED)

		# Return validation errors if input is invalid
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

""" View for user login - inherits default ObtainAuthToken behavior """
class LoginView(ObtainAuthToken):
	permission_classes = [AllowAny]

	def post(self, request, *args, **kwargs):
		serializer = self.serializer_class(data=request.data)

		# Validate credentials
		if serializer.is_valid():
			user = serializer.validated_data['user']
			# Get or create authentication token for user
			token, created = Token.objects.get_or_create(user=user)

			# Return token and user info
			return Response({
				'token': token.key,
				'user_id': user.pk,
				'email': user.email,
			}, status=status.HTTP_201_CREATED)

		# Return errors if authentication fails
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)