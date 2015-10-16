from mathtutor.models import Constants
from django.shortcuts import redirect
c = Constants()

def check_category_access(view_func):
    def _wrapped_view_func(request, category, *args, **kwargs):
        if c.check_access(request.user.student.group, request.user.student.district, category):
            return view_func(request, category, *args, **kwargs)
        else:
            return redirect("/accounts/grid/")
    return _wrapped_view_func
