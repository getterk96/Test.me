from functools import wraps
from django.utils.decorators import available_attrs
from codex.baseerror import *


def user_passes_test(test_func, error=ValidateError, msg="Can not pass user test"):

    def decorator(view_func, error, msg):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(view, *args, **kwargs):
            if test_func(view.request.user):
                return view_func(view, *args, **kwargs)
            raise error(msg)
        return _wrapped_view
    return decorator


def login_required(func):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated
    )
    return actual_decorator(func, ValidateError, "Login required")
