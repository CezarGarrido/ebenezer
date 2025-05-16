from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models import Q

TAX_REGIME = [
    ('LR', 'Lucro Real'),
    ('LP', 'Lucro Presumido'),
    ('SN', 'Simples Nacional'),
    ('SE', 'Simples Nacional, excesso sublimite de receita bruta')
]

ADDRESS_TYPE = [
    ('UNI', 'Único'),
    ('RES', 'Residencial'),
    ('COM', 'Comercial'),
    ('COB', 'Cobrança'),
    ('ENT', 'Entrega'),
    ('OUT', 'Outro'),
]

STATE_UF = [
    ('AC', 'AC'), ('AL', 'AL'), ('AP', 'AP'), ('AM', 'AM'), ('BA', 'BA'), ('CE', 'CE'),
    ('DF', 'DF'), ('ES', 'ES'), ('EX', 'EX'), ('GO', 'GO'), ('MA', 'MA'), ('MT', 'MT'),
    ('MS', 'MS'), ('MG', 'MG'), ('PA', 'PA'), ('PB', 'PB'), ('PR', 'PR'), ('PE', 'PE'),
    ('PI', 'PI'), ('RJ', 'RJ'), ('RN', 'RN'), ('RS', 'RS'), ('RO', 'RO'), ('RR', 'RR'),
    ('SC', 'SC'), ('SP', 'SP'), ('SE', 'SE'), ('TO', 'TO'),
]

class Person(models.Model):
    PERSON_TYPE_CHOICES = (
        ('F', 'Pessoa Física'),
        ('J', 'Pessoa Jurídica'),
    )

    person_type = models.CharField("Tipo", max_length=1, choices=PERSON_TYPE_CHOICES)
    name = models.CharField("Nome", max_length=255)
    created_by = models.ForeignKey(User, verbose_name="Criado por", on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", auto_now=True)

    class Meta:
        verbose_name = "Pessoa"
        verbose_name_plural = "Pessoas"

    def __str__(self):
        return self.name

class Individual(models.Model):
    person = models.OneToOneField(Person, verbose_name="Pessoa", on_delete=models.CASCADE, related_name='individual')
    cpf = models.CharField("CPF", max_length=32, null=True, blank=True)
    rg = models.CharField("RG", max_length=32, null=True, blank=True)
    birth_date = models.DateField("Data de nascimento", null=True, blank=True)
    
    def __str__(self):
        return f"{self.cpf}"
    
class LegalEntity(models.Model):
    person = models.OneToOneField(Person, verbose_name="Pessoa", on_delete=models.CASCADE, primary_key=True, related_name='legalentity')
    cnpj = models.CharField("CNPJ", max_length=32, null=True, blank=True)
    trade_name = models.CharField("Nome fantasia", max_length=255, null=True, blank=True)
    state_registration = models.CharField("Inscrição estadual", max_length=32, null=True, blank=True)
    responsible = models.CharField("Responsável", max_length=32, null=True, blank=True)
    tax_regime = models.CharField("Regime tributário", max_length=2, null=True, blank=True, choices=TAX_REGIME)
    suframa = models.CharField("SUFRAMA", max_length=16, null=True, blank=True)

    def __str__(self):
        return f"{self.cnpj}, {self.trade_name}"
    
class Address(models.Model):
    person = models.ForeignKey(Person, verbose_name="Pessoa", related_name="addresses", on_delete=models.CASCADE)
    address_type = models.CharField("Tipo de endereço", max_length=3, null=True, blank=True, choices=ADDRESS_TYPE)
    street = models.CharField("Logradouro", max_length=255, null=True, blank=True)
    number = models.CharField("Número", max_length=16, null=True, blank=True)
    neighborhood = models.CharField("Bairro", max_length=64, null=True, blank=True)
    complement = models.CharField("Complemento", max_length=64, null=True, blank=True)
    country = models.CharField("País", max_length=32, null=True, blank=True, default='Brasil')
    city = models.CharField("Cidade", max_length=64, null=True, blank=True)
    postal_code = models.CharField("CEP", max_length=16, null=True, blank=True)
    state = models.CharField("Estado (UF)", max_length=3, null=True, blank=True, choices=STATE_UF)
    is_primary = models.BooleanField("Endereço principal?", default=False)

    def __str__(self):
        return f"{self.street}, {self.number or 's/n'} - {self.city}/{self.state}"
    
class Email(models.Model):
    person = models.ForeignKey(Person, verbose_name="Pessoa", on_delete=models.CASCADE, related_name='emails')
    email = models.CharField("E-mail", max_length=255)
    is_primary = models.BooleanField("E-mail principal?", default=False)

    def __str__(self):
        return self.email

class Phone(models.Model):
    PHONE_TYPE_CHOICES = (
        ('M', 'Celular'),
        ('F', 'Fixo'),
        ('C', 'Comercial'),
    )

    person = models.ForeignKey(Person, verbose_name="Pessoa", on_delete=models.CASCADE, related_name='phones')
    phone = models.CharField("Telefone", max_length=20)
    type = models.CharField("Tipo", max_length=1, choices=PHONE_TYPE_CHOICES)
    is_primary = models.BooleanField("Telefone principal?", default=False)

    def __str__(self):
        return self.phone
