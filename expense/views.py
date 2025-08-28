from expense.models import Expense
from .forms import ExpenseForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum
from datetime import date



# Create your views here.


def expense_list(request):
    template_name = "expense/home.html"
    today = date.today()
    current_month = today.month
    current_year = today.year

    # Get all expenses for current month
    monthly_expenses = Expense.objects.filter(
        date__year=current_year,
        date__month=current_month
    )

    # Sum of one-time expenses
    total_expenses = monthly_expenses.filter(is_recurring=False).aggregate(total=Sum("amount"))["total"] or 0

    # Add recurring expenses for this month
    recurring_expenses = Expense.objects.filter(is_recurring=True)
    for expense in recurring_expenses:
        if expense.recurrence == "Daily":
            total_expenses += expense.amount * today.day  # number of days passed
        elif expense.recurrence == "Weekly":
            total_expenses += expense.amount * (today.day // 7 + 1)  # approximate weeks
        elif expense.recurrence == "Monthly":
            total_expenses += expense.amount
        elif expense.recurrence == "Yearly":
            total_expenses += expense.amount / 12  # spread yearly amount monthly

    total_budget = 20000
    remaining_budget = total_budget - total_expenses
    alert = None
    if remaining_budget <= 0:
        alert = f"⚠️ Your budget of ₹{total_budget} has been exhausted!"

    # Monthly summary grouped by category
    category_summary = monthly_expenses.values("category").annotate(total=Sum("amount")).order_by("-total")

    chart_labels = [item["category"] for item in category_summary]
    chart_data = [float(item["total"]) for item in category_summary]

    context = {
        "expense_list": monthly_expenses,
        "total_budget": total_budget,
        "remaining_budget": remaining_budget,
        "alert": alert,
        "total_expenses": total_expenses,
        "chart_labels": chart_labels,
        "chart_data": chart_data,
    }
    return render(request, template_name, context)


def expense_add(request):
    template_name = "expense/add_expense.html"

    if request.method == "GET":
        form = ExpenseForm()
        context = {"form": form}
        return render(request, template_name, context)
    else:
        form = ExpenseForm(request.POST)
        form.save()
        messages.success(request, "Expense added successfully!")
        return redirect("home")


def expense_edit(request, expense_id):
    template_name = "expense/add_expense.html"
    expense_details = Expense.objects.get(id=expense_id)

    if request.method == "GET":
        form: ExpenseForm = ExpenseForm(instance=expense_details)
        context = {"form": form}
        return render(request, template_name, context)

    else:
        form = ExpenseForm(request.POST, instance=expense_details)
        form.save()
        messages.success(request, "Expense updated successfully!")
        return redirect("home")


def expense_delete(request, expense_id):
    template_name = "expense/delete.html"
    expense_details = Expense.objects.get(id=expense_id)

    if request.method == "GET":
        context = {"expense": expense_details}
        return render(request, template_name, context)

    else:
        expense_details.delete()
        messages.success(request, "Expense deleted successfully!")
        return redirect("home")
