from django.conf import settings
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from core.models.base import Person
from core.models.company import Company

class Employee(Person):
    """Funcionário vinculado a uma empresa"""
    owner = models.ForeignKey(
        "Company",
        verbose_name="Empresa",
        on_delete=models.CASCADE,
        related_name="employees"
    )
    date_of_birth = models.DateField("Data de nascimento", null=True, blank=True)
    hire_date = models.DateField("Data de admissão", null=True, blank=True)
    termination_date = models.DateField("Data de desligamento", null=True, blank=True)
    ctps = models.CharField("CTPS (Carteira de Trabalho)", max_length=100, null=True, blank=True)
    position = models.CharField("Cargo", max_length=100, null=True, blank=True)
    department = models.CharField("Departamento", max_length=100, null=True, blank=True)
    salary = models.DecimalField("Salário", max_digits=15, decimal_places=2, null=True, blank=True)    

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"

class EmployeeUser(models.Model):
    employee = models.ForeignKey(
        "Employee",
        verbose_name="Funcionário",
        on_delete=models.CASCADE,
        related_name='users'
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name="Usuário",
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Funcionário Vinculado"
        verbose_name_plural = "Funcionários Vinculados"

    def __str__(self):
        return f"{self.user} → {self.employee}"
