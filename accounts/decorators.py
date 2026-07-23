from django.core.exceptions import PermissionDenied

def role_required(allowed_roles):
    def decorator(view_func):
        def wrap(request, *args, **kwargs):
            # الأدمن يقدر يدخل أي حتة، أو لو دورك مسموح ليه هتدخل
            if request.user.role == 'Admin' or request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                # لو دورك مش مسموح، هيطردك بره
                raise PermissionDenied 
        return wrap
    return decorator