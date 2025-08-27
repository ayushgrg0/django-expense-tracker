from django.urls import path
from .views import expense_list, expense_add, expense_edit, expense_delete

urlpatterns = [
    path('add/', expense_add, name='add_expense'),
    path('edit/<int:expense_id>/', expense_edit, name='edit_expense'),
    path('delete/<int:expense_id>/', expense_delete, name='delete_expense'),  # Placeholder for delete view
    path('', expense_list, name='home'),
]