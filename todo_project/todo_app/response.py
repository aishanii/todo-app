from django.http import JsonResponse
def send_200(data):
    return JsonResponse(data, status=200)

def send_400(data):
    return JsonResponse(data, status=400)

def send_401(data):
    return JsonResponse(data, status=401)

def send_403(data):
    return JsonResponse(data, status=403)