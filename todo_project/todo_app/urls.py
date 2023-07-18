from django.urls import path
from .views import login, RegisterUser, TodoView, Ping
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('login/', login),
    path('register/', csrf_exempt(RegisterUser.as_view()), name='register'),
    path('todo/', csrf_exempt(TodoView.as_view())),
    path('ping/', csrf_exempt(Ping.as_view()), name='ping'),
]
