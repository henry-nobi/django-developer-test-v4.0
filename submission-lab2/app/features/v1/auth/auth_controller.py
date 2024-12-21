import json
from django.utils.translation import gettext as _
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.features.v1.auth.auth_dto import (
    LoginDTO,
    RegisterDTO,
    ResetPasswordRequestDTO,
    ResetPasswordConfirmDTO,
)
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from app.models.company import Company
from rest_framework.permissions import AllowAny
from app.core.formats.response import ApiResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from app.core.validations.request import validate_request_body
import logging
from django.middleware.csrf import get_token
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login as auth_login

logger = logging.getLogger(__name__)
@swagger_auto_schema(method='post', request_body=LoginDTO)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def login(request):
    data = json.loads(request.body)
    validated_data = validate_request_body(LoginDTO, data)
    
    user = AuthService.login_user(
        request, 
        validated_data['email'], 
        validated_data['password']
    )
    
    if user:
        # Generate token
        token = AuthService.create_auth_token(user)
        
        # Create session
        auth_login(request, user)

        # Get primary profile language
        default_language = 'en'
        primary_profile = user.profiles.filter(is_primary=True).first()
        if primary_profile:
            default_language = primary_profile.default_language
        
        # Create response
        return ApiResponse.success(
            data={
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'token': token,
                    'default_language': default_language
                }
            },
            message=_("Login successful"),
            status_code=status.HTTP_200_OK
        )
        
    return ApiResponse.error(
        message=_("Invalid credentials"),
        status_code=status.HTTP_401_UNAUTHORIZED
    )

@swagger_auto_schema(method='post', request_body=RegisterDTO)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def register(request):
    data = json.loads(request.body)
    validated_data = validate_request_body(RegisterDTO, data)
    
    # Get company if company_id is provided
    company_id = validated_data.get('company_id')
    company = None
    if company_id:
        try:
            company = Company.objects.get(pk=company_id)
        except Company.DoesNotExist:
            return ApiResponse.error(
                message=_("Company not found"),
                status_code=status.HTTP_404_NOT_FOUND
            )

    # Create user with profile
    user = UserService.create_user(
        email=validated_data['email'],
        password=validated_data['password'],
        company=company,
        display_name=validated_data['display_name'],
        avatar=validated_data.get('avatar'),
        default_language=validated_data.get('default_language', 'en'),
        is_primary=validated_data.get('is_primary', True),
        is_active=validated_data.get('is_active', True)
    )
    
    response_data = {
        'user_id': user.id,
    }
    
    if user.active_profile:
        response_data['profile'] = {
            'id': user.active_profile.id,
            'display_name': user.active_profile.display_name,
            'company_id': user.active_profile.company.id
        }
        
    return ApiResponse.success(
        data=response_data,
        message=_("Registration successful"),
        status_code=status.HTTP_201_CREATED
    )

@swagger_auto_schema(method='post', request_body=ResetPasswordRequestDTO)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def reset_password_request(request):
    data = json.loads(request.body)
    validated_data = validate_request_body(ResetPasswordRequestDTO, data)
    
    # Use UserService to check if user exists before sending email
    user = UserService.get_user_by_email(validated_data['email'])
    if not user:
        return ApiResponse.error(
            message=_("User not found"),
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    if AuthService.reset_password(validated_data['email']):
        return ApiResponse.success(
            message=_("Password reset email sent"),
            status_code=status.HTTP_200_OK
        )
    return ApiResponse.error(
        message=_("Failed to send password reset email"),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )

@swagger_auto_schema(method='post', request_body=ResetPasswordConfirmDTO)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def reset_password_confirm(request):
    data = json.loads(request.body)
    validated_data = validate_request_body(ResetPasswordConfirmDTO, data)
    
    if AuthService.confirm_reset_password(
        validated_data['uid'],
        validated_data['token'],
        validated_data['new_password']
    ):
        return ApiResponse.success(
            message=_("Password reset successful"),
            status_code=status.HTTP_200_OK
        )
    return ApiResponse.error(
        message=_("Invalid reset link"),
        status_code=status.HTTP_400_BAD_REQUEST
    )

@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    try:
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return ApiResponse.error(
                message=_("Refresh token not found"),
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken(refresh_token)
        tokens = {
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }

        response = ApiResponse.success(
            message=_("Token refreshed successfully"),
            status_code=status.HTTP_200_OK
        )
        
        # Set new tokens in cookies
        AuthService.set_jwt_cookies(response, tokens)
        
        return response
    except Exception as e:
        return ApiResponse.error(
            message=_("Invalid refresh token"),
            status_code=status.HTTP_401_UNAUTHORIZED
        )

@swagger_auto_schema(method='post')
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    Logout endpoint that:
    1. Invalidates the user's auth token
    2. Logs them out of their session
    """
    if AuthService.logout_user(request):
        return ApiResponse.success(
            message=_("Logged out successfully"),
            status_code=status.HTTP_200_OK
        )
    
    return ApiResponse.error(
        message=_("Error during logout"),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )