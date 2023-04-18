from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import exception_handler
from .response_template import get_response_template


def c_exception_handler(exec, context):
    handlers = {
        # 'ValidationError': _handle_generic_error,
        'ValidationError': _handle_validation_error,
        'Http404': _handle_not_found_error,
        'NotFound': _handle_not_found_error,
        'NotAuthenticated': _handle_authentication_error,
        'InvalidToken': _handle_invalid_token_error,
        'PermissionDenied': _handle_permission_denied_error,
        'DoesNotExist': _handle_doesnot_exist_error,
    }
    response = exception_handler(exec, context)
    exec_class = exec.__class__.__name__
    if exec_class in handlers:
        return handlers[exec_class](exec, context, response)
    return response


def _handle_validation_error(exec, context, response):
    response_template = get_response_template()
    response_template['success'] = False
    exception_message = ""
    try:
        if hasattr(exec, 'message'):
            if type(exec.message).__class__.__name__ == "list":
                exception_message = exec.message[0]
            else:
                exception_message = exec.message
        elif hasattr(exec,'detail'):
            if type(exec.detail).__class__.__name__ == "list":
                exception_message = exec.detail[0].title()
            elif hasattr(exec.detail, 'items'):
                for key, value in exec.detail.items():
                    exception_message = f'{key} : {value[0]}'
            else:
                exception_message = exec.detail
        else:
            exception_message = str(exec)
    except ValueError as value_error:
        exception_message = str(exec)
    except Exception as e:
        exception_message = "Bad Request"
    response_template['message'] = exception_message
    response = JsonResponse(data=response_template, )
    response.status_code = status.HTTP_400_BAD_REQUEST
    return response

    
def _handle_doesnot_exist_error(exec, context, response):
    response_template = get_response_template()
    response_template['success'] = False
    response_template['message'] = str(exec)
    response = JsonResponse(data=response_template)
    return response


def _handle_permission_denied_error(exec, context, response):
    response_template = get_response_template()
    response_template['success'] = False
    response_template['message'] = exec.detail
    response.data = response_template
    return response


def _handle_not_found_error(exec, context, response):
    response_template = get_response_template()
    response_template['success'] = False
    response_template['message'] = str(exec)
    response.data = response_template
    return response


def _handle_invalid_token_error(exec, context, response):
    response_template = get_response_template()
    response_template['success'] = False
    response_template['message'] = exec.detail.get('detail')
    response.data = response_template
    return response


def _handle_authentication_error(exec, context, response):
    response_template = get_response_template()
    response_template['success'] = False
    response_template['message'] = "you are not authenticated, please login to proced"
    response.data = response_template
    return response


def _handle_generic_error(exec, context, response):
    response_template = get_response_template()
    response_template['success'] = False
    if isinstance(response.data, list):
        response_template['message'] = str(response.data[0])
    elif isinstance(response.data, dict):
        key = next(iter(response.data))
        if key == 'non_field_errors':
            if isinstance(response.data[key], list):
                response_template['message'] = str(response.data[key][0])
            else:
                response_template['message'] = str(response.data[key])
        else:
            error_message = str(response.data[key][0])
            if 'This' in error_message:
                error_message = error_message.replace('This', key)
            response_template['message'] = error_message.replace('_', ' ')
    response.data = response_template
    response.data = response_template
    return response


def error_404_handler(request, exception, *args, **kwargs):
    response_template = get_response_template()
    response_template['success'] = False
    response_template['message'] = "The end point not found."
    response = JsonResponse(data=response_template)
    response.status_code = status.HTTP_404_NOT_FOUND
    return response


def error_500_handler(request):
    response_template = get_response_template()
    response_template['success'] = False
    response_template['message'] = "Something bad had happened we are looking to debug it."
    response = JsonResponse(data=response_template)
    response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return response