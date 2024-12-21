from rest_framework.decorators import api_view
from rest_framework import status
from app.services.company_service import CompanyService
from drf_yasg.utils import swagger_auto_schema
from .company_dto import CompanyDTO, CompanyCreateDTO, CompanyUpdateDTO
from app.core.formats.response import ApiResponse
from app.core.validations.request import validate_request_body
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import gettext as _
import json

@swagger_auto_schema(method='post', request_body=CompanyCreateDTO)
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_company(request):
    data = json.loads(request.body)
    validated_data = validate_request_body(CompanyCreateDTO, data)
    
    company = CompanyService.create_company(
        name=validated_data['name'],
        description=validated_data.get('description')
    )
    return ApiResponse.success(
        data={'id': company.id},
        message=_("Company created successfully"),
        status_code=status.HTTP_201_CREATED
    )

@api_view(['GET'])
def get_company(request, company_id):
    company = CompanyService.get_company(company_id)
    if not company:
        return ApiResponse.error(
            message=_("Company not found"),
            status_code=status.HTTP_404_NOT_FOUND
        )
    return ApiResponse.success(
        data=CompanyDTO(company).data,
        message=_("Company retrieved successfully")
    )

@swagger_auto_schema(method='put', request_body=CompanyUpdateDTO)
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_company(request, company_id):
    data = json.loads(request.body)
    validated_data = validate_request_body(CompanyUpdateDTO, data)
    
    company = CompanyService.update_company(company_id, **validated_data)
    if not company:
        return ApiResponse.error(
            message=_("Company not found"),
            status_code=status.HTTP_404_NOT_FOUND
        )
    return ApiResponse.success(
        data=CompanyDTO(company).data,
        message=_("Company updated successfully")
    )

@api_view(['DELETE'])
def delete_company(request, company_id):
    if CompanyService.delete_company(company_id):
        return ApiResponse.success(
            message=_("Company deleted successfully"),
            status_code=status.HTTP_204_NO_CONTENT
        )
    return ApiResponse.error(
        message=_("Company not found"),
        status_code=status.HTTP_404_NOT_FOUND
    )

@api_view(['GET'])
def list_companies(request):
    is_active = request.query_params.get('is_active')
    if is_active is not None:
        is_active = is_active.lower() == 'true'
    companies = CompanyService.list_companies(is_active=is_active)
    return ApiResponse.success(
        data=[CompanyDTO(company).data for company in companies],
        message=_("Companies retrieved successfully")
    )