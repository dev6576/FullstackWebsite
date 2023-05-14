from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import UserPreference
from .models import Source, UserIncome


# Create your views here.


# def search_incomes(request):
#     if request.method=='POST':
#         search_str=json.loads(request.body).get('searchText')
        
#         incomes=income.objects.filter(amount__istartswith=search_str,owner=request.user) | income.objects.filter(
#             date__istartswith=search_str,owner=request.user) |income.objects.filter(
#             description__icontains=search_str,owner=request.user) | income.objects.filter(
#             category__icontains=search_str,owner=request.user)
        
#         data=incomes.values()
#         return JsonResponse(list(data),safe=False)

@login_required(login_url='/authentication/login')
def index(request):
    income=UserIncome.objects.filter(owner=request.user)
    paginator=Paginator(income,5)
    page_number=request.GET.get('page')
    page_obj=Paginator.get_page(paginator,page_number)
    currency=UserPreference.objects.get(user=request.user).currency
    categories=Source.objects.all()
    context={'income':income,'page_obj':page_obj,'currency':currency}
    return render(request,'income\index.html',context)

def add_income(request):
    sources=Source.objects.all()
    context={'sources':sources,'value':request.POST}
    if request.method=="GET":
        return render(request,r'income\add_income.html',context)

    if request.method=="POST":
        amount=request.POST['amount']

        if not amount:
            messages.error(request,'Amount required')
            return render(request,r'income\add_income.html',context)
        description=request.POST['description']

        if not description:
            messages.error(request,'Description required')
            return render(request,r'income\add_income.html',context)
        date=request.POST['income_date']

        if not date:
            messages.error(request,'Date required')
            return render(request,r'income\add_income.html',context)
        source=request.POST['source']

        if not source:
            messages.error(request,'Date required')
            return render(request,r'income\add_income.html',context)
        
        UserIncome.objects.create(amount=amount,date=date,source=source,description=description, owner=request.user)

        messages.success(request,'Income Added')

        return redirect('income')
    

def income_edit(request,id):
    income=UserIncome.objects.get(pk=id)
    sources=Source.objects.all()
    context={'income':income,'value':income,'sources':sources}
    if request.method=='GET':
        return render(request,'income/edit_income.html',context)
    if request.method=="POST":
        amount=request.POST['amount']

        if not amount:
            messages.error(request,'Amount required')
            return render(request,r'income\edit_income.html',context)
        description=request.POST['description']

        if not description:
            messages.error(request,'Description required')
            return render(request,r'income\edit_income.html',context)
        date=request.POST['income_date']

        if not date:
            messages.error(request,'Date required')
            return render(request,r'income\edit_income.html',context)
        category=request.POST['category']

        if not category:
            messages.error(request,'Date required')
            return render(request,r'income\edit_income.html',context)
        
        income.owner=request.user
        income.amount=amount
        income.date=date
        income.source=sources
        income.description=description
        income.save()
        messages.success(request,'Income Updated')

        return redirect('income')
    


    