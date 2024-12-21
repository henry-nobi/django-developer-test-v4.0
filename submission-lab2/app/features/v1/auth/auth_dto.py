from rest_framework import serializers

class LoginDTO(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6)

class RegisterDTO(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6)
    company_id = serializers.IntegerField(required=False)
    display_name = serializers.CharField(max_length=255)
    avatar = serializers.CharField(required=False, allow_null=True)
    default_language = serializers.CharField(required=False, default='en')
    is_primary = serializers.BooleanField(required=False, default=True)
    is_active = serializers.BooleanField(required=False, default=True)

class ResetPasswordRequestDTO(serializers.Serializer):
    email = serializers.EmailField()

class ResetPasswordConfirmDTO(serializers.Serializer):
    uid = serializers.CharField(max_length=255)
    token = serializers.CharField(max_length=255)
    new_password = serializers.CharField(min_length=6)
