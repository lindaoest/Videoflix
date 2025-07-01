from django.urls import path
from .views import RegistrationView, CookieTokenObtainPairView, RefreshTokenRefreshView, LogoutView
from .views import csrf

urlpatterns = [
	path('registration/', RegistrationView.as_view(), name='registration-list'),
	# path('login/', LoginView.as_view(), name='login-list'),
	path('login/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', RefreshTokenRefreshView.as_view(), name='token_refresh'),
    path('api/csrf/', csrf),
	path('logout/', LogoutView.as_view(), name='logout-list')

]