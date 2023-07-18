import jwt
from django.conf import settings
from django.http import JsonResponse
from .models import MainUser
from .constants import PATH_TO_SKIP_MIDDLEWARE
from datetime import datetime

class JWTMiddleware():


    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path in PATH_TO_SKIP_MIDDLEWARE:
            request.user = None
            return self.get_response(request)
        if 'HTTP_AUTHORIZATION' in request.META:
            auth_header = request.META['HTTP_AUTHORIZATION']
            token = auth_header.split(' ')[1]
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                exp = datetime.fromtimestamp(payload['exp'])
                if exp < datetime.utcnow():
                    return JsonResponse({"error":"Token expired"}, status=401)
                request.user = MainUser.objects.get(email=payload['username'])
            except jwt.ExpiredSignatureError:
                return JsonResponse({"error":"Token expired"}, status=401)
            except:
                return JsonResponse({'error':'Invalid Token'}, status=400)
        else:
            request.user = None
            return JsonResponse({'error':'Token not found'}, status=400)
            
        return self.get_response(request)