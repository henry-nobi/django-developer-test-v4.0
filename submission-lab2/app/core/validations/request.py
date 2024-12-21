from rest_framework import serializers

def validate_request_body(serializer_class, data):
    serializer = serializer_class(data=data)
    if not serializer.is_valid():
        raise serializers.ValidationError(serializer.errors)
    return serializer.validated_data