from functools import wraps
from django.utils.decorators import available_attrs
from codex.baseerror import *
from test_me_app.models import User_profile


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
        lambda u: u.is_authenticated and u.user_profile.status == User_profile.NORMAL
    )
    return actual_decorator(func, ValidateError, "Login required")


def player_required(func):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.user_profile.user_type == User_profile.PLAYER and
                  u.user_profile.status == User_profile.NORMAL
    )
    return actual_decorator(func, ValidateError, "Player required")


def organizer_required(func):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.user_profile.user_type == User_profile.ORGANIZER and
                  u.user_profile.status == User_profile.NORMAL
    )
    return actual_decorator(func, ValidateError, "Organizer required")


def admin_required(func):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.user_profile.user_type == User_profile.ADMINISTRATOR and
                  u.user_profile.status == User_profile.NORMAL
    )
    return actual_decorator(func, ValidateError, "Admin required")
