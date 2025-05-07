from encodings.punycode import T
import locale
from django.db import models
from django.contrib.auth.models import User
from core.escbuilder.escprinter import ESCPrinter
from core.models.company import Company
from core.models.donor import Donor
from django.core.exceptions import ObjectDoesNotExist
from core.escbuilder.escbuilder import ESCBuilder
from num2words import num2words
from core.models.employee import Employee
        # Enviar para impressora
import platform, tempfile, os

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

class DonationSettings(models.Model):
    thank_you_message = models.ForeignKey(
        ThankYouMessage,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Mensagem de Agradecimento"
    )
    
    default_printer = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Impressora Padrão",
        help_text="Nome da impressora padrão para imprimir recibos."
    )
    owner = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='donation_settings')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Criado por")

    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name="Atualizado em")
    deleted_at = models.DateTimeField(null=True, blank=True, editable=False)  # Soft delete

    class Meta:
        verbose_name = "Configuração de Doações"
        verbose_name_plural = "Configurações de Doações"

    def __str__(self):
        return "Configurações do Sistema de Doações"

    @classmethod
    def get_solo(cls):
        """Garantir que sempre tenha apenas um registro"""
        return cls.objects.first()

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

    def print_receipt(self, settings):
        content_bytes = self.get_receipt(settings)

        if platform.system() == "Windows":
            import win32print

        with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
            tmpfile.write(content_bytes)
            tmpfile_path = tmpfile.name

        try:
            if platform.system() == "Windows":
                hprinter = win32print.OpenPrinter(settings.default_printer)
                try:
                    job = win32print.StartDocPrinter(hprinter, 1, ("Recibo de Doação", None, "RAW"))
                    win32print.StartPagePrinter(hprinter)
                    with open(tmpfile_path, "rb") as f:
                        win32print.WritePrinter(hprinter, f.read())
                    win32print.EndPagePrinter(hprinter)
                    win32print.EndDocPrinter(hprinter)
                finally:
                    win32print.ClosePrinter(hprinter)
            else:
                import subprocess
                subprocess.run(["lp", "-d", settings.default_printer, tmpfile_path])
        finally:
            os.remove(tmpfile_path)
            
    def get_receipt(self, settings):
        CHARS_PER_LINE = 80  # Adjusted for typical condensed font on receipt printers
        CHARS_PER_LINE_CONDENSED = 136  # Adjusted for typical condensed font on receipt printers

        LEFT_MARGIN = 5  # Minimum left margin in characters
        RIGHT_MARGIN = 1  # Minimum right margin in characters
        RIGHT_MARGIN_CONDENSED  = 5  # Minimum right margin in characters
        MAX_LINE_WIDTH = CHARS_PER_LINE - LEFT_MARGIN - RIGHT_MARGIN
        MAX_LINE_WIDTH_CONDENSED = CHARS_PER_LINE_CONDENSED - LEFT_MARGIN - RIGHT_MARGIN_CONDENSED

        def print_centered(printer, text):
            """Print text centered within the paper width"""
            printer.print(text.center(MAX_LINE_WIDTH))
            printer.lineFeed()

        def print_centered_condensed(printer, text):
            """Print text centered within the paper width"""
            printer.print(text.center(MAX_LINE_WIDTH_CONDENSED))
            printer.lineFeed()


        def print_line_side_by_side(printer, left, right):
            """Print two pieces of text side by side with proper spacing"""
            min_margin = 2  # minimum spaces between sides
            total_len = len(left) + len(right) + min_margin
            
            if total_len >= MAX_LINE_WIDTH:
                result = left + ' ' * min_margin + right
            else:
                space_between = MAX_LINE_WIDTH - len(left) - len(right)
                result = left + (' ' * space_between) + right
            
            printer.print(result)
            printer.lineFeed()

        def print_line_side_by_side_condensed(printer, left, right):
            """Print two pieces of text side by side with proper spacing"""
            min_margin = 2  # minimum spaces between sides
            total_len = len(left) + len(right) + min_margin
            
            if total_len >= MAX_LINE_WIDTH_CONDENSED:
                result = left + ' ' * min_margin + right
            else:
                space_between = MAX_LINE_WIDTH_CONDENSED - len(left) - len(right)
                result = left + (' ' * space_between) + right
            
            printer.print(result)
            printer.lineFeed()


        def format_currency_extenso(value):
            """Format currency in Portuguese words"""
            return num2words(value, lang='pt_BR', to='currency').upper()

        def format_currency_value(value):
            """Format currency value with proper decimal places"""
            return locale.currency(value, grouping=True)

        def print_donor_address(printer, donor):
            """Print donor address information"""
            if not hasattr(donor, 'addresses'):
                return

            address = donor.addresses.first()
            if not address:
                return

            # Street and number
            address_parts = []
            if address.street:
                address_parts.append(address.street)
            if address.number:
                address_parts.append(address.number)
            address_str = " ".join(address_parts) if address_parts else "-"
            printer.print(f"Endereço....: {address_str.upper()}")
            printer.lineFeed()
            
            # Neighborhood
            neighborhood = address.neighborhood if address.neighborhood else "-"
            printer.print(f"Bairro......: {neighborhood.upper()}")
            printer.lineFeed()
            
            # City and state
            city_state = []
            if address.city:
                city_state.append(address.city)
            if address.state:
                city_state.append(address.state)
            city_state_str = " - ".join(city_state) if city_state else "-"
            printer.print(f"Cidade......: {city_state_str.upper()}")
            printer.lineFeed()

        def print_company_info(printer, company):
            """Print all company information"""
            # Print company name
            printer.bold(True)
            print_centered(printer, company.name.upper())
            printer.bold(False)

            # Print legal information
            printer.condensed(True)
            print_line_side_by_side_condensed(
                printer,
                "Utilidade Pública Municipal Lei Nº 1527 de 09/11/88",
                "Utilidade Pública Estadual Lei Nº 1493 de 13/05/94"
            )
            print_line_side_by_side_condensed(
                printer,
                "Utilidade Pública Federal Portaria Nº 735 de 13/08/01 DOU 14/08/01",
                "CEBAS: CEBAS 0030 Resolução Nº 05 de 12/04/2021"
            )
            print_centered_condensed(printer, "Atest. de Reg. no Cons. Nac. de Assist. Soc. R n.º 0018 Res n.º 05 de 02/02/04 DOU 05/02/04")
            printer.lineFeed()

            # Print address
            address = company.addresses.filter(address_type='UNI').first() or company.addresses.first()
            if address:
                address_line = f"{address.street}, {address.number}, {address.neighborhood}"
                print_centered_condensed(printer, address_line.upper())
                city_state = f"{address.city} - {address.state}"
                print_centered_condensed(printer, city_state.upper())

            printer.condensed(False)
            printer.lineFeed()

            # Print contacts
            try:
                legal = company.legalentity
                cnpj = legal.cnpj or "-"
                printer.print(f"CNPJ: {cnpj}")
                printer.lineFeed()
            except ObjectDoesNotExist:
                pass
            
            phones = company.phones.all()
            if phones.exists():
                phone_str = ', '.join([p.phone for p in phones])
                printer.print(f"Telefones: {phone_str}")
                printer.lineFeed()

            emails = company.emails.all()
            if emails.exists():
                email_str = ', '.join([e.email for e in emails])
                printer.print(f"E-mails: {email_str}")
                printer.lineFeed()

        def print_receipt_header(printer):
            """Print receipt header section"""
            printer.lineFeed()
            printer.print("-" * MAX_LINE_WIDTH)
            printer.lineFeed()
            printer.bold(True)
            print_centered(printer, "RECIBO DE DOAÇÃO")
            printer.bold(False)
            printer.print("-" * MAX_LINE_WIDTH)
            printer.lineFeed()
            printer.lineFeed()

        def print_donation_details(printer, receipt):
            """Print donation details section"""
            # Receipt number and issue date
            receipt_num = f"Recibo Nº...: {receipt.id}"
            issue_date = f"Emitido em: {receipt.expected_at.strftime('%d/%m/%Y')}"
            print_line_side_by_side(printer, receipt_num, issue_date)
            
            # Donor information
            printer.print(f"Recebemos de: {receipt.donor.name}")
            printer.lineFeed()
            
            print_donor_address(printer, receipt.donor)

            # Donor contact
            if hasattr(receipt.donor, 'phones') and receipt.donor.phones.exists():
                phone = receipt.donor.phones.first().phone
                printer.print(f"Contato.....: {phone.upper()}")
                printer.lineFeed()
            
            # Donation value
            formatted_value = format_currency_value(receipt.amount)
            printer.print(f"Valor.......: {formatted_value}")
            printer.lineFeed()
            printer.print(f"Por Extenso.: {format_currency_extenso(float(receipt.amount))}")
            printer.lineFeed()
            
            # Payment method
            if receipt.method and receipt.paid:
                method = dict(PAYMENT_METHOD_CHOICES).get(receipt.method, 'Outro').upper()
                printer.print(f"Pago em.....: {method}")
                printer.lineFeed()

        def print_footer(printer, settings):
            """Print receipt footer section"""
            printer.lineFeed()
            
            if settings.thank_you_message:
                for line in settings.thank_you_message.lines.all():
                    print_centered(printer, line.text.upper())
                printer.lineFeed()
                printer.lineFeed()
            else:
                print_centered(printer, "Agradecemos sua doação.".upper())
                printer.lineFeed()
                printer.lineFeed()
                
            signature_line = "-" * (MAX_LINE_WIDTH // 2)
            printer.print(signature_line.center(MAX_LINE_WIDTH))
            print_centered(printer, "Assinatura")


        # Main execution
        company = self.owner

        # Initialize printer
        escp = ESCPrinter(escp24pin=False)
        if not escp.initialize():
            raise Exception("Failed to initialize printer")
        escp.setMargins(5, 80)
        print_company_info(escp, company)
        print_receipt_header(escp)
        print_donation_details(escp, self)
        print_footer(escp, settings)

        escp.formFeed()
        return escp.build()


