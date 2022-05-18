from django.core.exceptions import PermissionDenied


def user_is_admin(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_admin:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
