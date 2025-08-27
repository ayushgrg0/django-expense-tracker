from django.db import models

# Create your models here.

CATEGORY_CHOICES = [
    ('Food', 'Food'),
    ('Transport', 'Transport'),
    ('Health', 'Health'),
    ('Other', 'Other'),
]

class Expense(models.Model):
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.amount}"