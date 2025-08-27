from django.urls import path
from .views import expense_list, expense_add

urlpatterns = [
    path('', expense_list, name='home'),
    path('add/', expense_add, name='add_expense'),

]