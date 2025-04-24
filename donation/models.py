from django.db import models
from django.contrib.auth.models import User
from core.escbuilder.escprinter import ESCPrinter
from core.models.company import Company
from core.models.donor import Donor
from django.core.exceptions import ObjectDoesNotExist
from core.escbuilder.escbuilder import ESCBuilder
from num2words import num2words
from core.models.employee import Employee

PAYMENT_METHOD_CHOICES = [
    ('cash', 'Dinheiro'),
    ('pix', 'Pix'),
    ('transfer', 'Transferência Bancária'),
    ('boleto', 'Boleto'),
    ('credit_card', 'Cartão de Crédito'),
    ('debit_card', 'Cartão de Débito'),
    ('other', 'Outro'),
]

class ThankYouMessage(models.Model):
    owner = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='thank_you_messages')
    name = models.CharField(max_length=100, verbose_name="Título")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Criado por")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Agradecimento"
        verbose_name_plural = "Mensagem de Agradecimentos"

    def __str__(self):
        return f"{self.name} - {self.get_lines_text()}"
    
    def get_lines_text(self):
        text = ",".join(line.text for line in self.lines.all())
        return text if len(text) <= 25 else text[:25] + "..."
    
class ThankYouMessageLine(models.Model):
    message = models.ForeignKey(ThankYouMessage, on_delete=models.CASCADE, related_name='lines')
    text = models.TextField(max_length=255, verbose_name="Linha de texto")

    class Meta:
        verbose_name = "Linha da Mensagem"
        verbose_name_plural = "Linhas da Mensagem"

    def __str__(self):
        return self.text
    
class Donation(models.Model):
    owner = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='donations')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Criado por")

    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, verbose_name="Doador")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Esperado (R$)", )
    expected_at = models.DateField(null=False, blank=False, verbose_name="Data") #  Data de expectativa de recebimento
    method = models.CharField(max_length=20,null=True, blank=True, choices=PAYMENT_METHOD_CHOICES, verbose_name="Meio de Pagamento")

    paid = models.BooleanField(default=False, verbose_name="Foi Pago?")
    paid_amount = models.DecimalField(default=None, null=True, blank=True, max_digits=10, decimal_places=2, verbose_name="Valor Recebido (R$)")
    received_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Recebido por")

    paid_at = models.DateField(null=True, blank=True, verbose_name="Data de Pagamento") #Data em que foi pago
    notes = models.TextField(max_length=255, null=True, blank=True, verbose_name="Observação")
    
    thank_you_message = models.ForeignKey(
        ThankYouMessage,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Mensagem de Agradecimento"
    )

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
        return f"Doação {self.id}"
    
    def receipt(self):
        
        CENTER_WIDTH = 66
        PAGE_WIDTH = CENTER_WIDTH + 40
    
        company = self.owner


        def linha_lado_lado(esquerda, direita, largura=CENTER_WIDTH):
            return f"{esquerda}{' ' * (largura - len(esquerda) - len(direita))}{direita}"

        def valor_por_extenso(valor):
            return num2words(valor, lang='pt_BR', to='currency')

        b = ESCBuilder()
        b.set_charset().font(draft=True)

        # Cabeçalho
        b.bold(True)
        b.text(company.name.center(PAGE_WIDTH))
        b.bold(False).linefeed()
        
        b.condensed(True)
        a = "Utilidade Pública Municipal Lei Nº 1527 de 09/11/88"
        c = "Utilidade Pública Estadual Lei Nº 1493 de 13/05/94"
        b.text(linha_lado_lado(a, c, largura=PAGE_WIDTH)).linefeed()
        b.text("Utilidade Pública Federal Portaria Nº 735 de 13/08/01 DOU 14/08/01".center(PAGE_WIDTH)).linefeed()
        b.text("CEBAS: CEBAS 0030 Resolução Nº 05 de 12/04/2021".center(PAGE_WIDTH)).linefeed()
        b.linefeed()
        b.condensed(False)

        # Endereço
        endereco = company.addresses.filter(address_type='UNI').first() or company.addresses.first()
        if endereco:
            b.text(f"{endereco.street}, {endereco.number} - {endereco.neighborhood}".center(PAGE_WIDTH)).linefeed()
            b.text(f"{endereco.city} - {endereco.state} - CEP: {endereco.postal_code}".center(PAGE_WIDTH)).linefeed()

        # Contatos
        telefones = company.phones.all()
        emails = company.emails.all()
        try:
            legal = company.legalentity
            cnpj = legal.cnpj or "-"
            b.text(f"CNPJ: {cnpj}").linefeed()
        except ObjectDoesNotExist:
            pass
        
        if telefones.exists():
            tel_str = ', '.join([t.phone for t in telefones])
            b.text(f"Telefones: {tel_str}").linefeed()

        if emails.exists():
            email_str = ', '.join([e.email for e in emails])
            b.text(f"E-mails: {email_str}").linefeed()

        b.linefeed()
        b.text("-" * (PAGE_WIDTH)).linefeed()
        b.bold(True)
        b.text("RECIBO DE DOAÇÃO".center(PAGE_WIDTH)).linefeed()
        b.bold(False)

        b.text("-" * (PAGE_WIDTH)).linefeed()
        b.linefeed()
        
        # Número do recibo e data de emissão
        recibo_num = f"Recibo Nº...: {self.id}"
        data_emissao = f"Emitido em: {self.expected_at.strftime('%d/%m/%Y')}"
        b.text(linha_lado_lado(recibo_num, data_emissao, largura=PAGE_WIDTH)).linefeed()
        
        # Dados do doador
        b.text(f"Recebemos de: {self.donor.name}").linefeed()
        
        # Endereço do doador (usando os dados do modelo Donor)
        if hasattr(self.donor, 'addresses'):
            endereco_doador = self.donor.addresses.first()
            if endereco_doador:
                # Formata o endereço (rua e número)
                endereco_parts = []
                if endereco_doador.street:
                    endereco_parts.append(endereco_doador.street)
                if endereco_doador.number:
                    endereco_parts.append(endereco_doador.number)
                endereco_str = " ".join(endereco_parts) if endereco_parts else "-"
                b.text(f"Endereço....: {endereco_str}").linefeed()
                
                # Bairro
                bairro_str = endereco_doador.neighborhood if endereco_doador.neighborhood else "-"
                b.text(f"Bairro......: {bairro_str}").linefeed()
                
                # Cidade e estado
                cidade_estado_parts = []
                if endereco_doador.city:
                    cidade_estado_parts.append(endereco_doador.city)
                if endereco_doador.state:
                    cidade_estado_parts.append(endereco_doador.state)
                cidade_estado_str = " - ".join(cidade_estado_parts) if cidade_estado_parts else "-"
                b.text(f"Cidade......: {cidade_estado_str}").linefeed()
    
        # Contato do doador
        if hasattr(self.donor, 'phones') and self.donor.phones.exists():
            telefone = self.donor.phones.first().phone
            b.text(f"Contato.....: {telefone}").linefeed()
        
        # Valor da doação
        valor_formatado = f"{self.amount:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        b.text(f"Valor.......: R$ {valor_formatado}").linefeed()
        b.text(f"Por Extenso.: {valor_por_extenso(float(self.amount))}").linefeed()
        
        # Método de pagamento (se aplicável)
        if self.method and self.paid:
            b.text(f"Pago em.....: {dict(PAYMENT_METHOD_CHOICES).get(self.method, 'Outro')}").linefeed()
            if self.paid_at:
                b.text(f"Data Pagto..: {self.paid_at.strftime('%d/%m/%Y')}").linefeed()
            if self.received_by:
                b.text(f"Recebido por.: {self.received_by.name}").linefeed()

        # Mensagem final
        b.linefeed()
        
        if self.thank_you_message:
            for line in self.thank_you_message.lines.all():
                b.text(line.text.center(PAGE_WIDTH)).linefeed()
            b.linefeed(2)  # espaço extra após a mensagem
        else:
            b.text("Agradecemos sua doação.".center(PAGE_WIDTH)).linefeed(2)
            
        b.text("______________________________".center(PAGE_WIDTH)).linefeed()
        b.text("Assinatura do Responsável".center(PAGE_WIDTH)).linefeed()

        b.form_feed()

        return b.build()
    
    def receipt_html(self):
        b = ESCBuilder()
        return b.to_html(self.receipt())
    

    def test_receipt(self):
        printer = "LPT1"
        company = self.owner
        center = 66

        def linha_lado_lado(esquerda, direita, largura=center):
            return f"{esquerda}{' ' * (largura - len(esquerda) - len(direita))}{direita}"

        def valor_por_extenso(valor):
            return num2words(valor, lang='pt_BR', to='currency')

        # Initialize printer
        escp = ESCPrinter(printer, escp24pin=False)
        if not escp.initialize():
            raise Exception("Failed to initialize printer")

        # Header
        escp.bold(True)
        escp.print(company.name.center(center + 40))
        escp.lineFeed()
        escp.bold(False)

        a = "Utilidade Pública Municipal Lei Nº 1527 de 09/11/88"
        c = "Utilidade Pública Estadual Lei Nº 1493 de 13/05/94"
        escp.print(linha_lado_lado(a, c, largura=center + 40))
        escp.lineFeed()
        escp.print("Utilidade Pública Federal Portaria Nº 735 de 13/08/01 DOU 14/08/01".center(center + 40))
        escp.lineFeed()
        escp.print("CEBAS: CEBAS 0030 Resolução Nº 05 de 12/04/2021".center(center + 40))
        escp.lineFeed()
        escp.lineFeed()

        # Address
        endereco = company.addresses.filter(address_type='UNI').first() or company.addresses.first()
        if endereco:
            escp.print(f"{endereco.street}, {endereco.number} - {endereco.neighborhood}".center(center + 40))
            escp.lineFeed()
            escp.print(f"{endereco.city} - {endereco.state} - CEP: {endereco.postal_code}".center(center + 40))
            escp.lineFeed()

        # Contacts
        telefones = company.phones.all()
        emails = company.emails.all()
        try:
            legal = company.legalentity
            cnpj = legal.cnpj or "-"
            escp.print(f"CNPJ: {cnpj}")
            escp.lineFeed()
        except ObjectDoesNotExist:
            pass
        
        if telefones.exists():
            tel_str = ', '.join([t.phone for t in telefones])
            escp.print(f"Telefones: {tel_str}")
            escp.lineFeed()

        if emails.exists():
            email_str = ', '.join([e.email for e in emails])
            escp.print(f"E-mails: {email_str}")
            escp.lineFeed()

        escp.lineFeed()
        escp.print("-" * (center + 40))
        escp.lineFeed()
        escp.bold(True)
        escp.print("RECIBO DE DOAÇÃO".center(center + 40))
        escp.lineFeed()
        escp.bold(False)

        escp.print("-" * (center + 40))
        escp.lineFeed()
        escp.lineFeed()
        
        # Receipt number and issue date
        recibo_num = f"Recibo Nº...: {self.id}"
        data_emissao = f"Emitido em: {self.expected_at.strftime('%d/%m/%Y')}"
        escp.print(linha_lado_lado(recibo_num, data_emissao, largura=center+40))
        escp.lineFeed()
        
        # Donor data
        escp.print(f"Recebemos de: {self.donor.name}")
        escp.lineFeed()
        
        # Donor address
        if hasattr(self.donor, 'addresses'):
            endereco_doador = self.donor.addresses.first()
            if endereco_doador:
                endereco_parts = []
                if endereco_doador.street:
                    endereco_parts.append(endereco_doador.street)
                if endereco_doador.number:
                    endereco_parts.append(endereco_doador.number)
                endereco_str = " ".join(endereco_parts) if endereco_parts else "-"
                escp.print(f"Endereço....: {endereco_str}")
                escp.lineFeed()
                
                bairro_str = endereco_doador.neighborhood if endereco_doador.neighborhood else "-"
                escp.print(f"Bairro......: {bairro_str}")
                escp.lineFeed()
                
                cidade_estado_parts = []
                if endereco_doador.city:
                    cidade_estado_parts.append(endereco_doador.city)
                if endereco_doador.state:
                    cidade_estado_parts.append(endereco_doador.state)
                cidade_estado_str = " - ".join(cidade_estado_parts) if cidade_estado_parts else "-"
                escp.print(f"Cidade......: {cidade_estado_str}")
                escp.lineFeed()

        # Donor contact
        if hasattr(self.donor, 'phones') and self.donor.phones.exists():
            telefone = self.donor.phones.first().phone
            escp.print(f"Contato.....: {telefone}")
            escp.lineFeed()
        
        # Donation value
        valor_formatado = f"{self.amount:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        escp.print(f"Valor.......: R$ {valor_formatado}")
        escp.lineFeed()
        escp.print(f"Por Extenso.: {valor_por_extenso(float(self.amount))}")
        escp.lineFeed()
        
        # Payment method
        if self.method and self.paid:
            escp.print(f"Pago em.....: {dict(PAYMENT_METHOD_CHOICES).get(self.method, 'Outro')}")
            escp.lineFeed()
            if self.paid_at:
                escp.print(f"Data Pagto..: {self.paid_at.strftime('%d/%m/%Y')}")
                escp.lineFeed()
            if self.received_by:
                escp.print(f"Recebido por.: {self.received_by.name}")
                escp.lineFeed()

        # Final message
        escp.lineFeed()
        
        if self.thank_you_message:
            for line in self.thank_you_message.lines.all():
                escp.print(line.text.center(center + 40))
                escp.lineFeed()
            escp.lineFeed()
            escp.lineFeed()
        else:
            escp.print("Agradecemos sua doação.".center(center + 40))
            escp.lineFeed()
            escp.lineFeed()
            
        escp.print("______________________________".center(center + 40))
        escp.lineFeed()
        escp.print("Assinatura do Responsável".center(center + 40))
        escp.lineFeed()

        escp.formFeed()
        escp.close()