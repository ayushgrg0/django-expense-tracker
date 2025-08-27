from django.db.models import Sum
from expense.models import Expense
from .forms import ExpenseForm
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.

def expense_list(request):
    template_name = 'expense/home.html'
    expense_list = Expense.objects.all()

    total_budget = 20000  

    total_expenses = Expense.objects.aggregate(total=Sum('amount'))['total'] or 0
    
    remaining_budget = total_budget - total_expenses

    alert = None
    if remaining_budget <= 0:
        alert = f"⚠️ Your budget of ₹{total_budget} has been exhausted!"
    context = {
        'expense_list': expense_list,
        'total_budget': total_budget,
        'remaining_budget': remaining_budget,
        'alert': alert,
        'total_expenses': total_expenses,
        }
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

def expense_delete(request, expense_id):
    template_name = 'expense/delete.html'
    expense_details = Expense.objects.get(id=expense_id)

    if request.method == 'GET':
        context = {
            'expense': expense_details
            }
        return render(request, template_name, context)
    
    else:
        expense_details.delete()
        messages.success(request, 'Expense deleted successfully!')
        return redirect('home')
