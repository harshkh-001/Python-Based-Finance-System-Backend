from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.conf import settings
from decimal import Decimal

class Transaction(models.Model):
    class Type(models.TextChoices):
        INCOME = 'income', 'Income'
        EXPENSE = 'expense', 'Expense'
        
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    
    transaction_type = models.CharField(max_length=10, choices=Type.choices)
    category = models.CharField(max_length=30)
    date = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"
    
