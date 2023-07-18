from rest_framework import serializers
from .models import Todos

class TodoSerializer(serializers.ModelSerializer):  #to serialize model data
    class Meta:
        model = Todos
        fields = '__all__'
