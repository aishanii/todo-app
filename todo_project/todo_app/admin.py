from django.contrib import admin
from .models import *

#so that models show on the admin portal

admin.site.register(Todos)
admin.site.register(MainUser)
