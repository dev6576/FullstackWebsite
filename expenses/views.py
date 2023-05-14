from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import UserPreference

# Create your views here.


def search_expenses(request):
    if request.method=='POST':
        search_str=json.loads(request.body).get('searchText')
        
        expenses=Expense.objects.filter(amount__istartswith=search_str,owner=request.user) | Expense.objects.filter(
            date__istartswith=search_str,owner=request.user) |Expense.objects.filter(
            description__icontains=search_str,owner=request.user) | Expense.objects.filter(
            category__icontains=search_str,owner=request.user)
        
        data=expenses.values()
        return JsonResponse(list(data),safe=False)

@login_required(login_url='/authentication/login')
def index(request):
    expenses=Expense.objects.filter(owner=request.user)
    paginator=Paginator(expenses,5)
    page_number=request.GET.get('page')
    page_obj=Paginator.get_page(paginator,page_number)
    currency=UserPreference.objects.get(user=request.user).currency
    categories=Category.objects.all()
    context={'expenses':expenses,'page_obj':page_obj,'currency':currency}
    return render(request,'expenses\index.html',context)

def add_expense(request):
    categories=Category.objects.all()
    context={'categories':categories,'value':request.POST}
    if request.method=="GET":
        return render(request,r'expenses\add_expense.html',context)

    if request.method=="POST":
        amount=request.POST['amount']

        if not amount:
            messages.error(request,'Amount required')
            return render(request,r'expenses\add_expense.html',context)
        description=request.POST['description']

        if not description:
            messages.error(request,'Description required')
            return render(request,r'expenses\add_expense.html',context)
        date=request.POST['expense_date']

        if not date:
            messages.error(request,'Date required')
            return render(request,r'expenses\add_expense.html',context)
        category=request.POST['category']

        if not category:
            messages.error(request,'Date required')
            return render(request,r'expenses\add_expense.html',context)
        
        Expense.objects.create(amount=amount,date=date,category=category,description=description, owner=request.user)

        messages.success(request,'Expenses Added')

        return redirect('expenses')
    

def expense_edit(request,id):
    expense=Expense.objects.get(pk=id)
    categories=Category.objects.all()
    context={'expense':expense,'value':expense,'categories':categories}
    if request.method=='GET':
        return render(request,'expenses/edit-expense.html',context)
    if request.method=="POST":
        amount=request.POST['amount']

        if not amount:
            messages.error(request,'Amount required')
            return render(request,r'expenses\edit-expense.html',context)
        description=request.POST['description']

        if not description:
            messages.error(request,'Description required')
            return render(request,r'expenses\edit-expense.html',context)
        date=request.POST['expense_date']

        if not date:
            messages.error(request,'Date required')
            return render(request,r'expenses\edit-expense.html',context)
        category=request.POST['category']

        if not category:
            messages.error(request,'Date required')
            return render(request,r'expenses\edit-expense.html',context)
        
        expense.owner=request.user
        expense.amount=amount
        expense.date=date
        expense.category=category
        expense.description=description
        expense.save()
        messages.success(request,'Expenses Updated')

        return redirect('expenses')
    