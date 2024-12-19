from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ValidationError as DjangoValidationError
from app.core.formats.response import ApiResponse
import json

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    # Handle JSON decode errors
    if isinstance(exc, json.JSONDecodeError):
        return ApiResponse.error(
            message="Invalid JSON format",
            status_code=status.HTTP_400_BAD_REQUEST,
            errors=str(exc)
        )

    # Handle DRF ValidationError
    if isinstance(exc, ValidationError):
        return ApiResponse.error(
            message=str(exc.detail),
            status_code=status.HTTP_400_BAD_REQUEST,
            errors=str(exc)
        )

    # Handle Django's ValidationError
    if isinstance(exc, DjangoValidationError):
        return ApiResponse.error(
            message=str(exc),
            status_code=status.HTTP_400_BAD_REQUEST,
            errors=str(exc)
        )

    # Handle any other exceptions
    if response is None:
        import pprint
        pprint.pprint(exc)
        return ApiResponse.error(
            message="Internal server error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            errors=str(exc)
        )

    return response 