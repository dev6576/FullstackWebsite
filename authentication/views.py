from django.shortcuts import render,redirect
from django.views import View
import json
import django
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes, DjangoUnicodeDecodeError
from django.utils.encoding import force_str
django.utils.encoding.force_text = force_str

from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator
from django.contrib import auth


# Create your views here.
class UsernameRegistrationView(View):
    def post(self,request):
        data=json.loads(request.body)
        username=data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error':'username should contain only alphanumeric characters'},status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'username taken'},status=409)
        return JsonResponse({'username_valid':True})
    
class EmailRegistrationView(View):
    def post(self,request):
        data=json.loads(request.body)
        email=data['email']

        if not validate_email(email):
            return JsonResponse({'email_error':'invalid email'},status=400)
        if User.objects.filter(username=email).exists():
            return JsonResponse({'email_error':'email taken'},status=409)
        return JsonResponse({'email_valid':True})
    

class RegistrationView(View):
    def get(self,request):
        return render(request,'authentication/register.html')
    

    def post(self,request):
        #GET user data
        #validate
        #create a user account
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']

        context={
            'fieldValue':request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password)<6:
                    messages.error(request,'Password too short')
                    return render(request,'authentication/register.html',context)
                user=User.objects.create_user(username=username,email=email)
                user.set_password(password)
                user.is_active=False
                user.save()
                domain=get_current_site(request).domain
                uidb64=(urlsafe_base64_encode(force_bytes(user.pk)))


                link=reverse('activate',kwargs={'uidb64':uidb64,'token':token_generator.make_token(user)})
                email_subject='Activate your account'
                activate_url='http://'+domain+link
                email_body='Use the below link to verify your account \n'+activate_url
                send_mail(
                    email_subject,
                    email_body,
                    'noreply@example.com',
                    [email],
                )

                messages.success(request,'User Created')
                return render(request,'authentication/register.html')

        return render(request,'authentication/register.html')
    

class VerificationView(View):
    def get(self,request,uidb64,token):
        try:
            id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=id)

            if not token_generator(user,token):
                return redirect('login'+'?message='+'User already activated')
            if user.is_active:
                return redirect('login')
            user.is_active=True
            user.save()

            messages.success(request,'Account activated successfully')
            return redirect('login')
        except Exception as ex:
            pass
        return redirect('login')


class LoginView(View):
    def get(self,request):
        return render(request,'authentication/login.html')

    def post(self,request):
        username=request.POST['username']
        password=request.POST['password']

        if username and password:
            user=auth.authenticate(username=username,password=password)
            if user:
                if user.is_active:
                    auth.login(request,user)
                    messages.success(request,'Welcome ' +user.username)
                    return redirect('expenses')
            

                messages.error(request,'Account not active')
                return render(request,'authentication/login.html')
            messages.error(request,'Invalid Credentials')
            return render(request,'authentication/login.html')
        messages.error(request,'Please fill all fields  ')
        return render(request,'authentication/login.html')
    
class LogoutView(View):
    def post(self,request):
        auth.logout(request)
        messages.success(request,'You have been logged out')
        return redirect('login')