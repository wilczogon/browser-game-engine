from flask import jsonify
from functools import wraps
import logging


logger = logging.getLogger(__name__)


def error_handling(func):
    @wraps(func)
    def call(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ApiError as e:
            logger.error(e, exc_info=True)
            return jsonify({'error_message': str(e)}), e.status_code
        except Exception as e:
            logger.fatal('Unexpected error occured.', exc_info=True)
            return jsonify({'error_message': 'Unexpected error occured.'}), 500
    return call


class ApiError(Exception):
    def __init__(self, status_code, msg):
        Exception.__init__(self, msg)
        self.status_code = status_code


class Unauthorized(ApiError):
    def __init__(self, msg='Authorization failed. Make sure token/username/password are correct.'):
        ApiError.__init__(self, 401, msg)


class BadRequest(ApiError):
    def __init__(self, msg='Invalid request.'):
        ApiError.__init__(self, 400, msg)


class InternalServerError(ApiError):
    def __init__(self, msg='Internal server error.'):
        ApiError.__init__(self, 500, msg)
