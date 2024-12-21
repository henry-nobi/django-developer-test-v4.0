from rest_framework.response import Response
from rest_framework import status

class ApiResponse:
    @staticmethod
    def success(data=None, message=None, status_code=status.HTTP_200_OK):
        response_data = {
            'status': 'success',
            'message': message,
            'data': data
        }
        # Remove None values
        response_data = {k: v for k, v in response_data.items() if v is not None}
        return Response(response_data, status=status_code)

    @staticmethod
    def error(message, errors=None, status_code=status.HTTP_400_BAD_REQUEST):
        response_data = {
            'status': 'error',
            'message': message,
            'errors': errors
        }
        # Remove None values
        response_data = {k: v for k, v in response_data.items() if v is not None}
        return Response(response_data, status=status_code) 