import os
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from core.models.base import Person
from core.models.company import Company

class Donor(Person):
    """Doador vinculado a uma empresa"""
    owner = models.ForeignKey("Company", on_delete=models.CASCADE, related_name="donors")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Doador"
        verbose_name_plural = "Doadores"
        ordering = ['id','name']
        