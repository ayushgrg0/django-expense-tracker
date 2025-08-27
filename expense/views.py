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


def expense_edit(request, expense_id):
    template_name = 'expense/add_expense.html'
    expense_details = Expense.objects.get(id=expense_id)

    if request.method == 'GET':
        form: ExpenseForm = ExpenseForm(instance=expense_details)
        context = {
            'form': form
            }
        return render(request, template_name, context)
    
    else :
        form = ExpenseForm(request.POST , instance = expense_details)
        form.save()
        messages.success(request, 'Expense updated successfully!')
        return redirect('home') 
