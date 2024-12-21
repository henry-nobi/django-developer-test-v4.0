from rest_framework import serializers

class UpdateUserDTO(serializers.Serializer):
    email = serializers.EmailField(required=False)
    display_name = serializers.CharField(max_length=255, required=False)
    avatar = serializers.CharField(required=False, allow_null=True)
    default_language = serializers.CharField(required=False, default='en')
    is_active = serializers.BooleanField(required=False)
    
    def validate(self, data):
        if not data:
            raise serializers.ValidationError("At least one field must be provided for update")
        return data
