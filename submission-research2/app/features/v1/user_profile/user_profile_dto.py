from rest_framework import serializers

class UserProfileCreateDTO(serializers.Serializer):
    company_id = serializers.IntegerField()
    display_name = serializers.CharField(max_length=255)
    avatar = serializers.CharField(required=False, allow_null=True)
    default_language = serializers.CharField(max_length=10, required=False, default='en')
    is_primary = serializers.BooleanField(required=False, default=False)

class UserProfileUpdateDTO(serializers.Serializer):
    company_id = serializers.IntegerField(required=False)
    display_name = serializers.CharField(max_length=255, required=False)
    avatar = serializers.CharField(required=False, allow_null=True)
    default_language = serializers.CharField(max_length=10, required=False)
    is_primary = serializers.BooleanField(required=False)

    def validate(self, data):
        if not data:
            raise serializers.ValidationError("At least one field must be provided for update")
        return data

class UserProfileDTO(serializers.Serializer):
    id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    company_id = serializers.IntegerField()
    display_name = serializers.CharField()
    avatar = serializers.CharField(allow_null=True)
    default_language = serializers.CharField()
    is_primary = serializers.BooleanField()
    is_active = serializers.BooleanField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField() 