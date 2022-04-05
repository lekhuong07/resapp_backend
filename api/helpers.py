from functools import wraps
import re
from flask import abort, jsonify, request
from models.resume import Resume


def requires_json(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        body = request.json
        if body is None:
            abort(400, {'debug': 'Request body missing'})

        return func(*args, **body, **kwargs)

    return wrapper


def validate_types(expected):
    def _validate_types(func):
        @wraps(func)
        def wrapper(*args, **body):
            # Check each type and add to invalid if not correct
            invalid = {}
            for key, v in expected.items():
                if not key in body or not isinstance(body[key], v):
                    invalid[key] = v

            # if there's any invalid fields, respond with an error
            if len(invalid) > 0:
                debug = ''
                for key, v in invalid.items():
                    debug += '\'{0}\' was expected to be a {1}, '.format(key, v.__name__)
                abort(400, {'debug': debug})

            return func(*args, **body)

        return wrapper

    return _validate_types
