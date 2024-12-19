from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from drf_yasg.generators import OpenAPISchemaGenerator
from django.utils.translation import gettext_lazy as _
from rest_framework import permissions

class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = ["http", "https"]
        return schema

schema_view = get_schema_view(
    openapi.Info(
        title=_("Canada Lab2 API"),
        default_version='v1',
        description=_("API documentation for Canada Lab2\n\n"
                     "To authorize, use the login endpoint to get a token, then click the 'Authorize' "
                     "button and enter the token with the prefix 'Token ' (e.g., 'Token abc123')"),
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    generator_class=BothHttpAndHttpsSchemaGenerator,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[],
    patterns=None,
) 