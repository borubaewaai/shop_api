import random
import string

from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.generics import CreateAPIView
from drf_yasg.utils import swagger_auto_schema

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