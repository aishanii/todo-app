from .models import Todos
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .response import *
from .utils import validate_email_password
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from .models import MainUser
from django.http import QueryDict
from .constants import *


class Ping(View):                      #to check if the server is working properly
    def get(self, request):
        return send_200({'message':'Hello, I am fine.'})


class RegisterUser(View):              #model to register new users by taking their username, email and pwd
    def _init_(self):
        self.response = {}
    
    def make_user(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = MainUser(
                email=email,
                username=username,
            )
            if password:
                user.set_password(password)
            user.save()
        except Exception as e:          #to make sure same user is not registered twice
            self.response = {'error':'User already exists',
                                'tech_error':str(e)}
            raise e
            
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email and password:
            try:
                self.make_user(request)
            except Exception as e:
                return send_400(self.response)
            return send_200({'message':'User created successfully'})
            
        else:
            return send_400({'error': MISSING_PARAMS})
        
    
@csrf_exempt
def login(request):
    if request.method == 'POST':
        from .utils import generate_access_token
        try:
            username = request.POST['email']
            password = request.POST['password']
            
            if not validate_email_password(username, password): #validate user credentials
                return send_401({'error':'Invalid Credentials'})
        
            token = generate_access_token(username)
            if isinstance(token, bytes):
                token = str(token, 'utf-8')
            return send_200({'token':token}) #the backend returns a temporary access token
            
        except Exception as e:
            return send_400({'error':str(e)})
        

class TodoView(View):      #to handle retrieval, creation, updation and deletion of todo objects
    def __init__(self):
        self.response = {}

    def get(self, request):  #retrieving all to-do items in the database
        user = request.user
    
        todos = Todos.objects.all()
        todo_list = []
        for todo in todos:
            todo_list.append(todo.to_dict())
        return send_200({"res_str":"success",
                        "data":todo_list})
    
    def create_obj(self, data):
        title = data.get("title")
        description= data.get("description")
        
        obj = Todos(title=title, description = description)
       
        obj.save()
        
        return obj.to_dict()
 
    
    def post(self, request):          #to specify a POST request
        user = request.user
        try:
            created_obj = self.create_obj(request.POST)
            self.response["res_data"] = created_obj
        except Exception as e:
            self.response["res_str"] = DEFAULT_FAILURE_MESSAGE
            self.response["tech_err"] = str(e)
            return send_400(self.response)

        return send_200(self.response)
         

    def delete(self, request):         #to specify a DELETE request
        user = request.user
    
        id = QueryDict(request.body).get("id")
        if id:
            try:
                obj = Todos.objects.get(pk=int(id))
                obj.delete()
            except Exception as e:
                return send_400({"res_str":DEFAULT_FAILURE_MESSAGE, 
                                "tech_err":str(e)})
            return send_200({"res_str":"Todo Deleted Successfully"})
        else:
            return send_400({"res_str":"Please Pass the Todo Id"})
    

    def update_type(self, data):       #function for updating to-do items
        todoid = (data.get("id"))
        print(todoid)

        if todoid:
            obj = Todos.objects.get(pk=int(todoid))
        else:
            raise Exception("Please Pass the Todo Id")
        obj.title = data.get("title")
        obj.description = data.get("description")

        
        obj.save()
        return obj.to_dict()
        

    def put(self, request):            #to specify a PUT request
        user =  request.user
        data = QueryDict(request.body)
        try:
            updated_type = self.update_type(data)
            self.response["res_data"] = updated_type
        except Exception as e:
            self.response["res_str"] = DEFAULT_FAILURE_MESSAGE
            self.response["tech_err"] = str(e)
            return send_400(self.response)
        return send_200(self.response)


