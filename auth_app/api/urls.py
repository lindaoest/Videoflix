from django.urls import path
from .views import RegistrationView, CookieTokenObtainPairView, RefreshTokenRefreshView
from .views import csrf

urlpatterns = [
	path('registration/', RegistrationView.as_view(), name='registration-list'),
	# path('login/', LoginView.as_view(), name='login-list'),
	path('login/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', RefreshTokenRefreshView.as_view(), name='token_refresh'),
    path('api/csrf/', csrf),

]