from django.db import models
from django.contrib.auth.models import User
from core.models.company import Company
from core.models.donor import Donor

PAYMENT_METHOD_CHOICES = [
    ('cash', 'Dinheiro'),
    ('pix', 'Pix'),
    ('transfer', 'Transferência Bancária'),
    ('boleto', 'Boleto'),
    ('credit_card', 'Cartão de Crédito'),
    ('debit_card', 'Cartão de Débito'),
    ('other', 'Outro'),
]

class Donation(models.Model):
    owner = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='donations')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Criado por")

    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, verbose_name="Doador")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor (R$)")
    expected_at = models.DateTimeField(null=True, blank=True, verbose_name="Data") #  Data de expectativa de recebimento
    method = models.CharField(max_length=20,null=True, blank=True, choices=PAYMENT_METHOD_CHOICES, verbose_name="Método")

    paid = models.BooleanField(default=False, verbose_name="Foi Pago?")
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name="Data de pagamento") #Data em que foi pago
    notes = models.TextField(max_length=255, null=True, blank=True, verbose_name="Observação")
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name="Atualizado em")
    deleted_at = models.DateTimeField(null=True, blank=True, editable=False)  # Soft delete
    
    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(amount__gt=0), name='check_amount_positive')
        ]
        
        verbose_name = "Doação"
        verbose_name_plural = "Doações"
        permissions = [
            ("can_update_paid", "Can update paid field"),
        ]
    def __str__(self):
        return f"Doação #{self.id}"
