from django.urls import path

from .views import (
    RegistrationAPIView, AuthorizationAPIView, ConfirmationAPIView,
    GoogleLoginAPIView, GoogleCallbackAPIView,
)
urlpatterns = [
    path('registration/', RegistrationAPIView.as_view(), name='registration'),
    path('authorization/', AuthorizationAPIView.as_view(), name='authorization'),
    path('confirm/', ConfirmationAPIView.as_view(), name='confirm'),
    path('google/login/', GoogleLoginAPIView.as_view(), name='google-login'),
    path('google/callback/', GoogleCallbackAPIView.as_view(), name='google-callback'),
]