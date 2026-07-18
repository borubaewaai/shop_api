from rest_framework import serializers

from .models import CustomUser, ConfirmationCode


class RegisterValidateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, label='Повтор пароля')

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'password2', 'first_name', 'last_name', 'phone_number')
        extra_kwargs = {'phone_number': {'required': False}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Пароли не совпадают'})
        return attrs


class AuthValidateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class ConfirmationSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        try:
            confirmation = ConfirmationCode.objects.get(user_id=attrs['user_id'])
        except ConfirmationCode.DoesNotExist:
            raise serializers.ValidationError('Код подтверждения не найден')

        if confirmation.code != attrs['code']:
            raise serializers.ValidationError('Неверный код подтверждения')

        attrs['confirmation'] = confirmation
        return attrs