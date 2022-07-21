import json, re, bcrypt, jwt

from django.http import JsonResponse
from django.views import View
from django.conf import settings

from users.models import User

class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            email	 = data['email']
            password	 = data['password']
            first_name	 = data['first_name']
            last_name	 = data['last_name']
            phone_number = data['phone_number']
            birthdate	 = data['birthdate']
            
            REGEX_EMAIL	  	 = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            REGEX_PASSWORD	 = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'
            REGEX_PHONE_NUMBER	 = '^01([0|1|6|7|8|9])-?([0-9]{3,4})-?([0-9]{4})$'
            REGEX_BIRTHDATE	 = '^(19[0-9][0-9]|20\d{2})-(0[0-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$'
            
            if not re.match(REGEX_EMAIL, email):
                return JsonResponse({'message':'INVALID_EMAIL'}, status=400)
            
            if not re.match(REGEX_PASSWORD, password):
                return JsonResponse({'message':'INVALID_PASSWORD'}, status=400)
            
            if not re.match(REGEX_PHONE_NUMBER, phone_number):
                return JsonResponse({'message':'INVALID_PHONE_NUMBER'}, status=400)
            
            if not re.match(REGEX_BIRTHDATE, birthdate):
                return JsonResponse({'message':'INVALID_BIRTHDATE'}, status=400)
            
            if User.objects.filter(email=email).exists():
                return JsonResponse({'message':'INVALID_EMAIL'}, status=400)
            
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            user = User(
                email        = email,
                password     = hashed_password,
                first_name   = first_name,
                last_name    = last_name,
                phone_number = phone_number,
                birthdate    = birthdate
            )
            
            user.save()
            
            return JsonResponse({'message':'SIGNUP_SUCCESS'}, status=201)
        
        except KeyError:
            return JsonResponse({'message':'KeyError'}, status=400)
        
class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            email    = data['email']
            password = data['password']
            
            user = User.objects.get(email=email)

            if not User.objects.filter(email=email).exists():
                return JsonResponse({"message" : "INVALID_USER"}, status=401)
            
            if not bcrypt.checkpw(password.encode('utf-8'), User.objects.get(email=email).password.encode("utf-8")):
                return JsonResponse({"message" : "INVALID_USER"}, status=401)
            
            access_token = jwt.encode({'id':user.id}, settings.SECRET_KEY, settings.ALGORITHM)
            
            return JsonResponse({'message':'LOGIN_SUCCESS', 'USER_NAME':user.first_name, 'TOKEN':access_token}, status=200)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
