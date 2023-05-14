from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns=[
    path('',views.index,name='expenses'),
    path('add_expense',views.add_expense,name='add_expenses'),
    path('expense-edit/<int:id>',views.expense_edit,name='expense-edit'),
    path('search-expenses',csrf_exempt(views.search_expenses),name='search-expenses'),

]