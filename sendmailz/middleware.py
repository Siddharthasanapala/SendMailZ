from django.shortcuts import redirect
from django.urls import resolve, Resolver404

class AuthRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # List of URL names that don't require authentication
        allowed_paths = ['welcome', 'signin', 'signup' , 'forgot_password' , 'verify_otp']

        # Check if the user is authenticated
        if not request.user.is_authenticated:
            # Try to resolve the current path
            try:
                resolved = resolve(request.path_info)
                current_path = resolved.url_name
                if current_path not in allowed_paths:
                    return redirect('signin')
            except Resolver404:
                # If the path can't be resolved, redirect to signin
                return redirect('signin')

        response = self.get_response(request)
        return response