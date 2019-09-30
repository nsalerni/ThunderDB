import requests
import traceback
from thunderdb.exceptions.errors import ServiceError


def is_valid_response_code(code):
    """True if the response code is valid and is not a Server Error
    """
    return 200 <= code < 500


def _issue_request(func, url, *args, **kwargs):
    """Issue an HTTP request 
    
    This function will issue an HTTP POST or GET request and handle 
    any exceptions that are thrown in the process
    """
    response = None
    last_raised_exception = None
    last_raised_exception_tb = None

    try:
        response = func(url, *args, **kwargs)
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as ex:
        last_raised_exception = ex
        last_raised_exception_tb = traceback.format_exc()

    if response is not None and is_valid_response_code(response.status_code):
        return response

    if response is not None:
        raise ServiceError("Request Failed",
                           url=url,
                           response=response.text,
                           status_code=response.status_code)
    else:
        raise ServiceError("Request failed",
                           url=url,
                           exception=str(last_raised_exception),
                           traceback=last_raised_exception_tb)


def post(url, *args, **kwargs):
    """Issue an HTTP POST request to the specified URL"""
    return _issue_request(requests.post, url, *args, **kwargs)


def get(url, *args, **kwargs):
    """Issue an HTTP GET request to the specified URL
    """
    return _issue_request(requests.get, url, *args, **kwargs)
