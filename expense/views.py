from django.shortcuts import render

# Create your views here.

def expense_list(request):
    template_name = 'expense/home.html'
    return render(request, template_name)