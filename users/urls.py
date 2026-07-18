from django.urls import path

from .views import RegistrationAPIView, AuthorizationAPIView, ConfirmationAPIView

urlpatterns = [
    path('registration/', RegistrationAPIView.as_view(), name='registration'),
    path('authorization/', AuthorizationAPIView.as_view(), name='authorization'),
    path('confirm/', ConfirmationAPIView.as_view(), name='confirm'),
]