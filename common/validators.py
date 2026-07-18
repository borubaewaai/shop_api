from datetime import date

from rest_framework import serializers


def validate_user_age(request):

    token_payload = request.auth

    birthdate_str = None
    if token_payload:
        birthdate_str = token_payload.get('birthdate')

    if not birthdate_str or birthdate_str == 'None':
        raise serializers.ValidationError(
            'Укажите дату рождения, чтобы создать продукт.'
        )

    birthdate = date.fromisoformat(birthdate_str)
    today = date.today()
    age = today.year - birthdate.year - (
        (today.month, today.day) < (birthdate.month, birthdate.day)
    )

    if age < 18:
        raise serializers.ValidationError(
            'Вам должно быть 18 лет, чтобы создать продукт.'
        )