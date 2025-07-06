from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User
from auth_app.api.serializers import RegistrationSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode

""" View for user registration - anyone can access """
class RegistrationView(APIView):
	permission_classes = [AllowAny]

	def post(self, request, *args, **kwargs):
		serializer = RegistrationSerializer(data=request.data)

		# Check if input data is valid
		if serializer.is_valid():
			# Save user and create a token
			user = serializer.save()
			user.is_active = False
			user.save()
			# token, created = Token.objects.get_or_create(user=user)

			# Return token and user info in response
			return Response({
				# 'token': token.key,
				'user_id': user.pk,
				'email': user.email,
				'username': user.username
			}, status=status.HTTP_201_CREATED)

		# Return validation errors if input is invalid
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

""" View for user login - inherits default ObtainAuthToken behavior """
# class LoginView(ObtainAuthToken):
# 	permission_classes = [AllowAny]
# 	serializer_class = LoginSerializer
# 	# renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

# 	def post(self, request, *args, **kwargs):
# 		serializer = self.serializer_class(data=request.data, context={'request': request})

# 		# Validate credentials
# 		if serializer.is_valid():
# 			print('test', serializer.validated_data)
# 			user = serializer.validated_data['user']
# 			# Get or create authentication token for user
# 			token, created = Token.objects.get_or_create(user=user)

# 			# Return token and user info
# 			return Response({
# 				'token': token.key,
# 				'user_id': user.pk,
# 				'email': user.email,
# 			}, status=status.HTTP_201_CREATED)

# 		# Return errors if authentication fails
# 		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CookieTokenObtainPairView(TokenObtainPairView):
	serializer_class = CustomTokenObtainPairSerializer

	def post(self, request, *args, **kwargs):
		# response =  super().post(request, *args, **kwargs)
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		access = serializer.validated_data['access']
		refresh = serializer.validated_data['refresh']

		# access = response.data.get('access')
		# refresh = response.data.get('refresh')

		response = Response({'message': 'success'})

		response.set_cookie(
			key='access_token',
			value=str(access),
			httponly=True,
			secure=True,
			samesite='Lax'
		)

		response.set_cookie(
			key='refresh_token',
			value=str(refresh),
			httponly=True,
			secure=True,
			samesite='Lax'
		)

		response.data = {
			"detail": "Login successful",
			"user": {
				"id": serializer.validated_data["pk"],
				"username": serializer.validated_data["username"]
			}
		}
		return response

class RefreshTokenRefreshView(TokenRefreshView):

	def post(self, request, *args, **kwargs):
		refresh_token = request.COOKIES.get('refresh_token')

		if refresh_token is None:
			return Response({'detail': 'Refresh Token not found'}, status=status.HTTP_400_BAD_REQUEST)

		serializer = self.get_serializer(data={'refresh': refresh_token})

		try:
			serializer.is_valid(raise_exception=True)
		except:
			return Response({'detail': 'Refresh Token invalid'}, status=status.HTTP_400_BAD_REQUEST)

		access_token = serializer.validated_data.get('access')

		response = Response({
			'detail': 'Token refreshed',
			'access': access_token
		})
		response.set_cookie(
			key='access_token',
			value=access_token,
			httponly=True,
			secure=True,
			samesite='Lax'
		)

		return response

class LogoutView(APIView):
	def post(self, request, *args, **kwargs):
		response = Response({"detail": "Log-Out successfully! All Tokens will be deleted. Refresh token is now invalid."})
		response.delete_cookie("access_token")
		response.delete_cookie("refresh_token")
		return response

class ActivateRegistration(APIView):
	def get(self, request, uidb64, token):

		try:
			uid = urlsafe_base64_decode(uidb64).decode()
			user = User.objects.get(pk=uid)
		except (User.DoesNotExist, ValueError, TypeError):
			return Response({"message": "Invalid link"})

		if default_token_generator.check_token(user, token):
			user.is_active = True
			user.save()
			return Response({"message": "Account successfully activated."})
		else:
			return Response({"message": "Token invalid or expired."})


@ensure_csrf_cookie
def csrf(request):
    return JsonResponse({'detail': 'CSRF cookie set'})