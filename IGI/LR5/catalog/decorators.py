from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def my_view(request):
    return render(request, 'error/403.html', status=403)

def superuser_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        try:
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            else:
                return render(request, 'error/403.html', status=403)
        except AttributeError: 
            return render(request, 'error/403.html', status=403)
    return _wrapped_view

def staff_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        try:
            if request.user.is_staff:
                return view_func(request, *args, **kwargs)
            else:
                return render(request, 'error/403.html', status=403)
        except AttributeError: 
            return render(request, 'error/403.html', status=403)
    return _wrapped_view

def customer_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        try:
            if request.user.is_customer:
                return view_func(request, *args, **kwargs)
            else:
                return render(request, 'error/403.html', status=403)
        except AttributeError: 
            return render(request, 'error/403.html', status=403)
    return _wrapped_view
