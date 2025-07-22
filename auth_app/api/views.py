from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from auth_app.api.serializers import RegistrationSerializer, LoginSerializer, ConfirmPasswordSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.dispatch import Signal
from django.contrib.auth.models import User

# Set signal
resetPassword = Signal()

# View for user registration - anyone can access
class RegistrationView(APIView):
	permission_classes = [AllowAny]

	def post(self, request, *args, **kwargs):
		# Validate input data with serializer
		serializer = RegistrationSerializer(data=request.data)

		# Check if input data is valid
		if serializer.is_valid():
			# Save user but deactivate until email confirmation
			user = serializer.save()
			user.is_active = False
			user.save()

			# Return token placeholder and user info
			return Response({
				'token': 'token',
				'user': {
					'id': user.pk,
					'email': user.email
				}
			}, status=status.HTTP_201_CREATED)

		# Return validation errors
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View for user login using JWT and cookies
class CookieTokenObtainPairView(TokenObtainPairView):
	serializer_class = LoginSerializer

	def post(self, request, *args, **kwargs):
		# Validate login data
		serializer = self.get_serializer(data=request.data)

		if serializer.is_valid():

			# Get access and refresh tokens
			access = serializer.validated_data['access']
			refresh = serializer.validated_data['refresh']

			# Prepare login success response
			response = Response({
				'detail': 'Login successful',
				'user': {
					'id': serializer.validated_data['pk'],
					'username': serializer.validated_data['username']
				}
			}, status=status.HTTP_200_OK)

			# Set JWT tokens in HttpOnly cookies
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

			# Return validation errors
			return response

		# Return validation errors if input is invalid
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View to refresh access token using refresh token from cookies
class RefreshTokenRefreshView(TokenRefreshView):

	def post(self, request, *args, **kwargs):
		# Get refresh token from cookies
		refresh_token = request.COOKIES.get('refresh_token')

		if refresh_token is None:
			return Response({
				'detail': 'Refresh Token not found'
			}, status=status.HTTP_400_BAD_REQUEST)

		# Validate refresh token
		serializer = self.get_serializer(data={'refresh': refresh_token})
		try:
			serializer.is_valid(raise_exception=True)
		except:
			return Response({
				'detail': 'Refresh Token invalid'
	 		}, status=status.HTTP_401_UNAUTHORIZED)

		# Return new access token and set cookie
		access_token = serializer.validated_data.get('access')
		response = Response({
			'detail': 'Token refreshed',
			'access': access_token
		}, status=status.HTTP_200_OK)

		response.set_cookie(
			key='access_token',
			value=access_token,
			httponly=True,
			secure=True,
			samesite='Lax'
		)

		return response

# View to log out user by deleting JWT cookies
class LogoutView(APIView):

	def post(self, request, *args, **kwargs):
		# Get refresh token from cookies
		refresh_token = request.COOKIES.get('refresh_token')

		if refresh_token is not None:
			# Delete both access and refresh tokens
			response = Response({
				'detail': 'Log-Out successfully! All Tokens will be deleted. Refresh token is now invalid.'
			}, status=status.HTTP_200_OK)

			response.delete_cookie('access_token')
			response.delete_cookie('refresh_token')

			return response

		# Refresh token not found
		return Response({'detail': 'Refresh Token not found'}, status=status.HTTP_400_BAD_REQUEST)

# View to activate user account via email link
class ActivateRegistration(APIView):
	permission_classes = [AllowAny]

	def get(self, request, uidb64, token):

		# Decode user ID and validate token
		try:
			uid = urlsafe_base64_decode(uidb64).decode()
			user = User.objects.get(pk=uid)
		except (User.DoesNotExist, ValueError, TypeError):
			return Response({'message': 'Invalid link'}, status=status.HTTP_400_BAD_REQUEST)

		if default_token_generator.check_token(user, token):
			# Activate user account
			user.is_active = True
			user.save()
			return Response({'message': 'Account successfully activated.'}, status=status.HTTP_200_OK)

		# Token is invalid or expired
		return Response({'message': 'Token invalid or expired.'}, status=status.HTTP_400_BAD_REQUEST)

# View to trigger password reset email via signal
class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
		# Get user by email
        email = request.data.get('email')
        user = User.objects.get(email=email)

        if user is not None:
			# Send password reset signal
            resetPassword.send(sender=None, instance=user, created=True)

            return Response({
                'detail': 'An email has been sent to reset your password.'
            }, status=status.HTTP_200_OK)

# View to confirm password reset with token
class ConfirmPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
		# Decode user ID and validate token
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError):
            return Response({'message': 'Invalid link'}, status=status.HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user, token):
			# Validate new password input
            serializer = ConfirmPasswordSerializer(data=request.data, context={'user': user})

            # Check if input data is valid
            if serializer.is_valid():
				# Save new password
                serializer.save()

                return Response({
                    'detail': 'Your Password has been successfully reset.'
                }, status=status.HTTP_200_OK)

            # Return validation errors if input is invalid
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Token invalid or expired.'}, status=status.HTTP_400_BAD_REQUEST)

# View to ensure CSRF cookie is set
@ensure_csrf_cookie
def csrf(request):
    return JsonResponse({'detail': 'CSRF cookie set'})