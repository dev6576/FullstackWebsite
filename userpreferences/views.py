from django.shortcuts import render
import os
import json
from django.conf import settings
import pdb
from .models import UserPreference
from django.contrib import messages

# Create your views here.

def index(request):
    exists=UserPreference.objects.filter(user=request.user).exists()
    user_preference=None
    if exists:
        user_preference=UserPreference.objects.get(user=request.user)
    currencyData=[]
    file_path=os.path.join(settings.BASE_DIR,'currencies.json')
    with open(file_path,'r') as json_file:
        data=json.load(json_file)
        for k,v in data.items():
            currencyData.append({'name':k,'value':v})
    if request.method=="GET":
        return render(request,'preferences/index.html',{'currencies':currencyData,'user_preference':user_preference})
    else:
        currency=request.POST['currency']
        if exists:
            user_preference.currency=currency
            user_preference.save()
        else:
            UserPreference.objects.create(user=request.user,currency=currency)
        messages.success(request,'Changes Saved')
        return render(request,'preferences/index.html',{'currencies':currencyData,'user_preference':user_preference})