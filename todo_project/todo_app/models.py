from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Todos(models.Model):           #representing table in the database that contains todo items
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        return {
            "id":self.id,
            "title":self.title,
            "description":self.description,
            "created_at":self.created_at,
            "updated_at":self.updated_at
        }


class MainUser(models.Model):        #representing table in the database that contains all users
    email       = models.EmailField(max_length=254, unique=True)
    username  = models.CharField(max_length=64)
    password    = models.CharField(max_length=254)
    user_type       = models.CharField(max_length=64, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
