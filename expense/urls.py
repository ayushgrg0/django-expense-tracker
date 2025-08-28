from django.urls import path
from .views import expense_list, expense_add, expense_edit, expense_delete, export_expenses_csv

urlpatterns = [
    path('add/', expense_add, name='add_expense'),
    path('edit/<int:expense_id>/', expense_edit, name='edit_expense'),
    path('delete/<int:expense_id>/', expense_delete, name='delete_expense'),  # Placeholder for delete view
    path('export/csv/', export_expenses_csv, name='export_expenses_csv'),
    path('', expense_list, name='home'),
]