
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('todo_app.urls'))   #users will have to navigate to localhost/api/todo/
]
