from django.urls import path
from .views import RegistrationView, CookieTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
	path('registration/', RegistrationView.as_view(), name='registration-list'),
	# path('login/', LoginView.as_view(), name='login-list'),
	path('login/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]