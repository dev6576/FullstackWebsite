from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns=[
    path('',views.index,name='income'),
    path('add_income',views.add_income,name='add_income'),
    path('income-edit/<int:id>',views.income_edit,name='income-edit'),
    #  path('search-incomes',csrf_exempt(views.search_incomes),name='search-incomes'),
]