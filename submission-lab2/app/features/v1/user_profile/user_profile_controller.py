from rest_framework.decorators import api_view
from rest_framework import status
from app.services.user_profile_service import UserProfileService
from drf_yasg.utils import swagger_auto_schema
from .user_profile_dto import UserProfileDTO, UserProfileCreateDTO, UserProfileUpdateDTO
from app.core.formats.response import ApiResponse
from app.core.validations.request import validate_request_body
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import gettext as _
import json

@swagger_auto_schema(method='post', request_body=UserProfileCreateDTO)
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_profile(request):
    data = json.loads(request.body)
    validated_data = validate_request_body(UserProfileCreateDTO, data)
    
    profile = UserProfileService.create_profile(
        user_id=request.user.id,
        company_id=validated_data['company_id'],
        display_name=validated_data['display_name'],
        avatar=validated_data.get('avatar'),
        default_language=validated_data.get('default_language'),
        is_primary=validated_data.get('is_primary'),
    )
    return ApiResponse.success(
        data=UserProfileDTO(profile).data,
        message=_("Profile created successfully"),
        status_code=status.HTTP_201_CREATED
    )

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_profile(request, profile_id):
    profile = UserProfileService.get_profile(profile_id)
    if not profile:
        return ApiResponse.error(
            message=_("Profile not found"),
            status_code=status.HTTP_404_NOT_FOUND
        )
    return ApiResponse.success(
        data=UserProfileDTO(profile).data,
        message=_("Profile retrieved successfully")
    )

@swagger_auto_schema(method='put', request_body=UserProfileUpdateDTO)
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_profile(request, profile_id):
    data = json.loads(request.body)
    validated_data = validate_request_body(UserProfileUpdateDTO, data)
    
    profile = UserProfileService.update_profile(profile_id, **validated_data)
    if not profile:
        return ApiResponse.error(
            message=_("Profile not found"),
            status_code=status.HTTP_404_NOT_FOUND
        )
    return ApiResponse.success(
        data=UserProfileDTO(profile).data,
        message=_("Profile updated successfully")
    )

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_profile(request, profile_id):
    if UserProfileService.delete_profile(profile_id):
        return ApiResponse.success(
            message=_("Profile deleted successfully"),
            status_code=status.HTTP_204_NO_CONTENT
        )
    return ApiResponse.error(
        message=_("Profile not found"),
        status_code=status.HTTP_404_NOT_FOUND
    )

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_user_profiles(request, user_id):
    profiles = UserProfileService.list_user_profiles(user_id)
    return ApiResponse.success(
        data=[UserProfileDTO(profile).data for profile in profiles],
        message=_("Profiles retrieved successfully")
    )