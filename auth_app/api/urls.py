from django.urls import path
from .views import RegistrationView, CookieTokenObtainPairView, RefreshTokenRefreshView, LogoutView, ActivateRegistration
from .views import csrf

urlpatterns = [
	path('register/', RegistrationView.as_view(), name='registration-list'),
	# path('login/', LoginView.as_view(), name='login-list'),
	path('login/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', RefreshTokenRefreshView.as_view(), name='token_refresh'),
    path('api/csrf/', csrf),
	path('logout/', LogoutView.as_view(), name='logout-list'),
	path('activate/<int:uidb64>/<int:token>/', ActivateRegistration.as_view(), name='activateRegistration-list'),

]