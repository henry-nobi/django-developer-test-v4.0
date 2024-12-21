from app.models.company import Company
from django.core.exceptions import ValidationError

class CompanyService:
    @staticmethod
    def create_company(name, description=None):
        company = Company.objects.create(
            name=name,
            description=description
        )
        return company

    @staticmethod
    def get_company(company_id):
        try:
            return Company.objects.get(pk=company_id)
        except Company.DoesNotExist:
            return None

    @staticmethod
    def update_company(company_id, **data):
        try:
            company = Company.objects.get(pk=company_id)
            for key, value in data.items():
                setattr(company, key, value)
            company.save()
            return company
        except Company.DoesNotExist:
            return None

    @staticmethod
    def delete_company(company_id):
        try:
            company = Company.objects.get(pk=company_id)
            company.delete()
            return True
        except Company.DoesNotExist:
            return False

    @staticmethod
    def list_companies(is_active=None):
        queryset = Company.objects.all()
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)
        return queryset 