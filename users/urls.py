from django.urls import path

from .views import RegistrationAPIView, AuthorizationAPIView, ConfirmationAPIView

urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('login/', AuthorizationAPIView.as_view(), name='login'),
    path('confirm/', ConfirmationAPIView.as_view(), name='confirm'),
]