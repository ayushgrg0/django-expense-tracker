from expense.models import Expense
from .forms import ExpenseForm
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.

def expense_list(request):
    template_name = 'expense/home.html'
    expense_list = Expense.objects.all()
    context = {'expense_list': expense_list}
    return render(request, template_name, context)

def expense_add(request):
    template_name = 'expense/add_expense.html'

    if request.method == 'GET':
        form = ExpenseForm()
        context = {
            'form': form
            }
        return render(request, template_name, context)
    else:
        form = ExpenseForm(request.POST)
        form.save()
        messages.success(request, 'Expense added successfully!')
        return redirect('home')