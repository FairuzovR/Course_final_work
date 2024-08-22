from django.http import JsonResponse
from rest_framework_simplejwt.tokens import AccessToken


def jwt_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        token = request.COOKIES.get('accessToken')
        if not token:
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        if not token:
            return JsonResponse(
                {'detail': 'Authentication credentials were not provided.'},
                status=401
            )
        try:
            AccessToken(token)
        except Exception:
            return JsonResponse({'detail': 'Invalid token.'}, status=401)
        return view_func(request, *args, **kwargs)

    return _wrapped_view
