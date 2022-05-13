from rest_framework.response import Response
from rest_framework.exceptions import ValidationError


def api_exception_handler(except_msg, context):    
        if isinstance(except_msg, ValidationError):
            response = {
                'error': 'Validation errors'.upper(),
                'errors': except_msg.get_full_details(),
                'details': "Validation errors, check 'errors' tag for details",
            }
        else:
            response = {
                'error': str(except_msg),
            }
        return Response(response, status=400)
