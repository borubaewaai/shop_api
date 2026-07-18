import random
import string

from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.generics import CreateAPIView
from drf_yasg.utils import swagger_auto_schema
import requests as http_requests
from urllib.parse import urlencode
from django.conf import settings as django_settings
from django.utils import timezone
from django.shortcuts import redirect
from .serializers import (
    RegisterValidateSerializer,
    AuthValidateSerializer,
    ConfirmationSerializer,
    get_tokens_with_birthdate,
)
from .models import CustomUser, ConfirmationCode


class AuthorizationAPIView(APIView):
    @swagger_auto_schema(request_body=AuthValidateSerializer)
    def post(self, request):
        serializer = AuthValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)

        if not user:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
                data={'error': 'User credentials are wrong!'}
            )

        if not user.is_active:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
                data={'error': 'User account is not activated yet!'}
            )

        tokens = get_tokens_with_birthdate(user)
        return Response(data=tokens)


class RegistrationAPIView(CreateAPIView):
    serializer_class = RegisterValidateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        phone_number = serializer.validated_data.get('phone_number')
        first_name = serializer.validated_data.get('first_name', '')
        last_name = serializer.validated_data.get('last_name', '')

        with transaction.atomic():
            user = CustomUser.objects.create_user(
                email=email,
                password=password,
                phone_number=phone_number,
                first_name=first_name,
                last_name=last_name,
            )

            code = ''.join(random.choices(string.digits, k=6))
            ConfirmationCode.objects.create(user=user, code=code)

        return Response(
            data={
                'user_id': user.id,
                'email': user.email,
                'confirmation_code': code,
            },
            status=status.HTTP_201_CREATED
        )


class ConfirmationAPIView(APIView):
    @swagger_auto_schema(request_body=ConfirmationSerializer)
    def post(self, request):

        serializer = ConfirmationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        confirmation = serializer.validated_data['confirmation']
        user = confirmation.user
        user.is_active = True
        user.save()

        confirmation.delete()

        return Response(data={'message': 'Аккаунт успешно активирован'})

class GoogleLoginAPIView(APIView):
    """Редиректим пользователя на страницу согласия Google."""

    def get(self, request):
        params = {
            'client_id': django_settings.GOOGLE_OAUTH_CLIENT_ID,
            'redirect_uri': django_settings.GOOGLE_OAUTH_REDIRECT_URI,
            'response_type': 'code',
            'scope': 'openid email profile',
            'access_type': 'offline',
        }
        url = 'https://accounts.google.com/o/oauth2/v2/auth?' + urlencode(params)
        return redirect(url)


class GoogleCallbackAPIView(APIView):

    def get(self, request):
        code = request.GET.get('code')
        if not code:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'error': 'Не получен код авторизации от Google'}
            )

        token_response = http_requests.post(
            'https://oauth2.googleapis.com/token',
            data={
                'code': code,
                'client_id': django_settings.GOOGLE_OAUTH_CLIENT_ID,
                'client_secret': django_settings.GOOGLE_OAUTH_CLIENT_SECRET,
                'redirect_uri': django_settings.GOOGLE_OAUTH_REDIRECT_URI,
                'grant_type': 'authorization_code',
            }
        )
        token_data = token_response.json()
        access_token = token_data.get('access_token')

        if not access_token:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'error': 'Не удалось получить access_token', 'details': token_data}
            )

        userinfo_response = http_requests.get(
            'https://www.googleapis.com/oauth2/v2/userinfo',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        userinfo = userinfo_response.json()

        email = userinfo.get('email')
        if not email:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'error': 'Google не вернул email'}
            )

        user, created = CustomUser.objects.get_or_create(
            email=email,
            defaults={
                'first_name': userinfo.get('given_name', ''),
                'last_name': userinfo.get('family_name', ''),
                'registration_source': 'google',
                'is_active': True,
            }
        )

        user.is_active = True
        user.last_login = timezone.now()
        user.first_name = userinfo.get('given_name', user.first_name)
        user.last_name = userinfo.get('family_name', user.last_name)
        user.save()

        tokens = get_tokens_with_birthdate(user)
        return Response(data=tokens)