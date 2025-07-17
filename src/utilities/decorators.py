from functools import wraps



def require_role(*allowed_roles):
    def decorator(func):
        @wraps(func)  # keeps the original function name and docstring
        def wrapper(self, *args, **kwargs):
            if not hasattr(self, "user_role"):
                raise AttributeError("Class must have 'user_role' attribute")

            if self.user_role not in allowed_roles:
                raise PermissionError(
                    f"Role '{self.user_role}' not allowed to perform '{func.__name__}'"
                )
            return func(self, *args, **kwargs)
        return wrapper
    return decorator