from django.urls import path
from .views import csrf, RegistrationView, CookieTokenObtainPairView, RefreshTokenRefreshView, LogoutView, ActivateRegistration, ResetPasswordView, ConfirmPasswordView

urlpatterns = [
	path('register/', RegistrationView.as_view(), name='registration-list'),
	path('login/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', RefreshTokenRefreshView.as_view(), name='token_refresh'),
    path('api/csrf/', csrf),
	path('logout/', LogoutView.as_view(), name='logout-list'),
	path('activate/<uidb64>/<token>/', ActivateRegistration.as_view(), name='activateRegistration-list'),
	path('password_reset/', ResetPasswordView.as_view(), name='password-reset-list'),
	path('password_confirm/<uidb64>/<token>/', ConfirmPasswordView.as_view(), name='password-confirm-list'),

]