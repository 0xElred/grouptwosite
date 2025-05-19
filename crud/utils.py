from django.shortcuts import redirect
from functools import wraps

def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # List of URLs that don't require login
        public_urls = ['/login', '/createaccount']
        
        # Check if the current path is public
        if request.path in public_urls:
            return view_func(request, *args, **kwargs)
            
        # For all other URLs, check if user is logged in
        if 'user_id' not in request.session:
            return redirect(f'/login?next={request.path}')
            
        return view_func(request, *args, **kwargs)
    return wrapper
