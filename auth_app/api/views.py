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
				'token': 'token',
				'user': {
					'id': user.pk,
					'email': user.email
				}
			}, status=status.HTTP_201_CREATED)

		# Return validation errors if input is invalid
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CookieTokenObtainPairView(TokenObtainPairView):
	serializer_class = LoginSerializer

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)

		if serializer.is_valid():

			access = serializer.validated_data['access']
			refresh = serializer.validated_data['refresh']

			response = Response({
				'detail': 'Login successful',
				'user': {
					'id': serializer.validated_data['pk'],
					'username': serializer.validated_data['username']
				}
			}, status=status.HTTP_200_OK)

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

			# response.data = {
			# 	"detail": "Login successful",
			# 	"user": {
			# 		"id": serializer.validated_data["pk"],
			# 		"username": serializer.validated_data["username"]
			# 	}
			# }

			# response.status_code = status.HTTP_200_OK

			return response

		# Return validation errors if input is invalid
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RefreshTokenRefreshView(TokenRefreshView):

	def post(self, request, *args, **kwargs):
		refresh_token = request.COOKIES.get('refresh_token')

		if refresh_token is None:
			return Response({
				'detail': 'Refresh Token not found'
			}, status=status.HTTP_400_BAD_REQUEST)

		serializer = self.get_serializer(data={'refresh': refresh_token})

		try:
			serializer.is_valid(raise_exception=True)
		except:
			return Response({
				'detail': 'Refresh Token invalid'
	 		}, status=status.HTTP_401_UNAUTHORIZED)

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

class LogoutView(APIView):

	def post(self, request, *args, **kwargs):
		refresh_token = request.COOKIES.get('refresh_token')

		if refresh_token is not None:
			response = Response({
				'detail': 'Log-Out successfully! All Tokens will be deleted. Refresh token is now invalid.'
			}, status=status.HTTP_200_OK)

			response.delete_cookie('access_token')
			response.delete_cookie('refresh_token')

			return response

		return Response({
			'detail': 'Refresh Token not found'
		}, status=status.HTTP_400_BAD_REQUEST)


class ActivateRegistration(APIView):
	def get(self, request, uidb64, token):

		try:
			uid = urlsafe_base64_decode(uidb64).decode()
			user = User.objects.get(pk=uid)
		except (User.DoesNotExist, ValueError, TypeError):
			return Response({'message': 'Invalid link'}, status=status.HTTP_400_BAD_REQUEST)

		if default_token_generator.check_token(user, token):
			user.is_active = True
			user.save()
			return Response({'message': 'Account successfully activated.'}, status=status.HTTP_200_OK)
		else:
			return Response({'message': 'Token invalid or expired.'}, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        user = User.objects.get(email=email)

        if user is not None:
            resetPassword.send(sender=None, instance=user, created=True)

            return Response({
                'detail': 'An email has been sent to reset your password.'
            }, status=status.HTTP_200_OK)

class ConfirmPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError):
            return Response({'message': 'Invalid link'}, status=status.HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user, token):
            serializer = ConfirmPasswordSerializer(data=request.data, context={'user': user})

            # Check if input data is valid
            if serializer.is_valid():

                return Response({
                    'detail': 'Your Password has been successfully reset.'
                }, status=status.HTTP_200_OK)

            # Return validation errors if input is invalid
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Token invalid or expired.'}, status=status.HTTP_400_BAD_REQUEST)

@ensure_csrf_cookie
def csrf(request):
    return JsonResponse({'detail': 'CSRF cookie set'})