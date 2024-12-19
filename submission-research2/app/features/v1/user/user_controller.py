import json
from app.services.user_service import UserService
from app.features.v1.user.user_dto import UpdateUserDTO
from rest_framework.decorators import api_view
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from app.core.formats.response import ApiResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from app.core.validations.request import validate_request_body
from django.utils.translation import gettext as _

@swagger_auto_schema(method='get', manual_parameters=[
    openapi.Parameter('user_id', openapi.IN_PATH, description="ID of the user", type=openapi.TYPE_INTEGER)
])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request, user_id):
    user = UserService.get_user(user_id)
    if user:
        user_data = {
            'id': user.id,
            'email': user.email,
            'profile': {
                'display_name': user.profile.display_name,
                'avatar': user.profile.avatar,
                'default_language': user.profile.default_language,
                'is_primary': user.profile.is_primary,
                'is_active': user.profile.is_active,
            }
        }
        return ApiResponse.success(
            data=user_data,
            message=_("User retrieved successfully")
        )
    return ApiResponse.error(
        message=_("User not found"),
        status_code=status.HTTP_404_NOT_FOUND
    )

@swagger_auto_schema(method='get')
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    """
    Get current user profile based on JWT token
    """
    user = request.user
    if not user.is_authenticated:
        return ApiResponse.error(
            message=_("Not authenticated"),
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
    # Get active profile
    active_profile = user.profiles.filter(is_primary=True).first()
    
    user_data = {
        'id': user.id,
        'email': user.email,
        'profile': None
    }
    
    if active_profile:
        user_data['profile'] = {
            'id': active_profile.id,
            'display_name': active_profile.display_name,
            'avatar': active_profile.avatar,
            'default_language': active_profile.default_language,
            'company_id': active_profile.company_id if active_profile.company else None
        }
    
    return ApiResponse.success(
        data=user_data,
        message=_("User profile retrieved successfully")
    )

@swagger_auto_schema(method='put', request_body=UpdateUserDTO)
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_user(request, user_id):
    data = json.loads(request.body)
    validated_data = validate_request_body(UpdateUserDTO, data)
    
    user = UserService.update_user(user_id, **validated_data)
    if user:
        return ApiResponse.success(
            data={'user_id': user.id},
            message=_("User updated successfully")
        )
    return ApiResponse.error(
        message=_("User not found"),
        status_code=status.HTTP_404_NOT_FOUND
    )

@swagger_auto_schema(method='delete', manual_parameters=[
    openapi.Parameter('user_id', openapi.IN_PATH, description="ID of the user", type=openapi.TYPE_INTEGER)
])
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_user(request, user_id):
    if UserService.delete_user(user_id):
        return ApiResponse.success(
            message=_("User deleted successfully"),
            status_code=status.HTTP_204_NO_CONTENT
        )
    return ApiResponse.error(
        message=_("User not found"),
        status_code=status.HTTP_404_NOT_FOUND
    )

@swagger_auto_schema(
    method='post',
    responses={
        200: openapi.Response('Successful logout'),
        401: openapi.Response('Unauthorized - Invalid or expired token')
    }
)
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    Logout the current user and invalidate their token
    """
    try:
        # Delete the user's token to logout
        request.user.auth_token.delete()
        return ApiResponse.success(
            message=_("Successfully logged out"),
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        return ApiResponse.error(
            message=_("An error occurred during logout"),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['current_password', 'new_password'],
        properties={
            'current_password': openapi.Schema(type=openapi.TYPE_STRING),
            'new_password': openapi.Schema(type=openapi.TYPE_STRING),
        }
    )
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """
    Change the password for the current user
    """
    current_password = request.data.get('current_password')
    new_password = request.data.get('new_password')
    
    if not current_password or not new_password:
        return ApiResponse.error(
            message=_("Both current and new password are required"),
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    if len(new_password) < 6:
        return ApiResponse.error(
            message=_("New password must be at least 6 characters long"),
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    success = UserService.change_password(request.user, current_password, new_password)
    
    if success:
        return ApiResponse.success(
            message=_("Password changed successfully"),
            status_code=status.HTTP_200_OK
        )
    else:
        return ApiResponse.error(
            message=_("Current password is incorrect"),
            status_code=status.HTTP_400_BAD_REQUEST
        )

@swagger_auto_schema(
    method='get',
    responses={
        200: openapi.Response(
            description="List of user profiles",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_STRING),
                    'message': openapi.Schema(type=openapi.TYPE_STRING),
                    'data': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'profiles': openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                        'display_name': openapi.Schema(type=openapi.TYPE_STRING),
                                        'avatar': openapi.Schema(type=openapi.TYPE_STRING),
                                        'email': openapi.Schema(type=openapi.TYPE_STRING),
                                        'is_primary': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                    }
                                )
                            )
                        }
                    )
                }
            )
        )
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profiles(request):
    """
    Get all profiles for the current user
    """
    try:
        profiles = UserService.get_user_profiles(request.user.id)
        
        profiles_data = [{
            'id': profile.id,
            'display_name': profile.display_name,
            'avatar': profile.avatar,
            'email': request.user.email,
            'is_primary': profile.is_primary,
            'company_id': profile.company_id if profile.company else None,
            'default_language': profile.default_language
        } for profile in profiles]
        
        return ApiResponse.success(
            data={'profiles': profiles_data},
            message=_("User profiles retrieved successfully"),
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        return ApiResponse.error(
            message=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )