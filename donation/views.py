from django.http import HttpResponse, JsonResponse
from django.urls import path
import locale
import logging
from datetime import datetime
import os
import platform
import subprocess
import tempfile
from django.contrib import admin
from django import forms
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.template.response import TemplateResponse
from django.utils.translation import gettext_lazy as _

from donation import report_pdf
from .models import Donation, DonationSettings
from core.models.donor import Donor
from core.models.employee import Employee, EmployeeUser
from core.escbuilder.escprinter import ESCPrinter
from django.db import models

logger = logging.getLogger(__name__)

class ReportBuilderMixin:
    """Mixin containing common report building functionality"""
    CHARS_PER_LINE = 80  # Adjusted for typical condensed font on receipt printers
    CHARS_PER_LINE_CONDENSED = 136  # Adjusted for typical condensed font on receipt printers
    
    LEFT_MARGIN = 2  # Minimum left margin in characters
    RIGHT_MARGIN = 1  # Minimum right margin in characters
    RIGHT_MARGIN_CONDENSED  = 2  # Minimum right margin in characters
    MAX_LINE_WIDTH = CHARS_PER_LINE - LEFT_MARGIN - RIGHT_MARGIN
    MAX_LINE_WIDTH_CONDENSED = CHARS_PER_LINE_CONDENSED - LEFT_MARGIN - RIGHT_MARGIN_CONDENSED


    def print_centered(self, printer, text):
        """Print text centered within the paper width"""
        printer.print(text.center(self.MAX_LINE_WIDTH))
        printer.lineFeed()

    def print_centered_condensed(self, printer, text):
        """Print text centered within the paper width"""
        printer.print(text.center(self.MAX_LINE_WIDTH_CONDENSED))
        printer.lineFeed()

    def print_line_side_by_side(self, printer, left, right):
        """Print two pieces of text side by side with proper spacing"""
        min_margin = 2  # minimum spaces between sides
        total_len = len(left) + len(right) + min_margin
        
        if total_len >= self.MAX_LINE_WIDTH:
            result = left + ' ' * min_margin + right
        else:
            space_between = self.MAX_LINE_WIDTH - len(left) - len(right)
            result = left + (' ' * space_between) + right
        
        printer.print(result)
        printer.lineFeed()

    def print_line_side_by_side_condensed(self, printer, left, right):
        """Print two pieces of text side by side with proper spacing"""
        min_margin = 2  # minimum spaces between sides
        total_len = len(left) + len(right) + min_margin
        
        if total_len >= self.MAX_LINE_WIDTH_CONDENSED:
            result = left + ' ' * min_margin + right
        else:
            space_between = self.MAX_LINE_WIDTH_CONDENSED - len(left) - len(right)
            result = left + (' ' * space_between) + right
        
        printer.print(result)
        printer.lineFeed()

    def _linha_pontilhada(self, esquerda, direita, largura=None):
        largura = largura or self.MAX_LINE_WIDTH
        return f"{esquerda}{'.' * (largura - len(esquerda) - len(direita))}{direita}"

    def _generate_report_header(self, printer, company, title):
        """Generate common report header"""
        self.print_line_side_by_side(
            printer,
            company.name,
            f"Emissão: {datetime.now().strftime('%d/%m/%Y')}"
        )

        try:
            cnpj = company.legalentity.cnpj or "-"
        except ObjectDoesNotExist:
            cnpj = "-"

        self.print_line_side_by_side(
            printer,
            "Inscrição Estadual Nº ISENTO",
            f"C.G.C Nº: {cnpj}"
        )
        printer.lineFeed(3)

        printer.bold(True)
        self.print_centered(printer, title)
        printer.bold(False)

        printer.lineFeed(3)

    def _generate_table_header(self, printer):
        """Generate common table header"""
        
        printer.condensed(True)
        self.print_centered_condensed(printer, "-" * self.MAX_LINE_WIDTH_CONDENSED)
        
        header_line = (
            "CÓDIGO".ljust(10) +
            "DATA".ljust(12) +
            "DOADOR".ljust(38) + 
            "VALOR PREVISTO".rjust(22) + 
            "VALOR RECEBIDO".rjust(25) + 
            "DIFERENÇA".rjust(20)
        )
        printer.print(header_line)
        printer.lineFeed()
        
        self.print_centered_condensed(printer, "-" * self.MAX_LINE_WIDTH_CONDENSED)
        printer.condensed(False)


    def _generate_donation_row(self, printer, donation):
        """Generate a single donation row"""
        row_line = (
            f"{donation.id}".ljust(10) +
            (donation.expected_at.strftime('%d/%m/%Y') if donation.expected_at else "-").ljust(12) +
            f"{donation.donor.id} - {donation.donor.name}".ljust(38) +
            locale.currency(donation.amount or 0, grouping=True).rjust(22) +
            locale.currency(donation.paid_amount or 0, grouping=True).rjust(25)
        )
        
        valor_previsto = donation.amount or 0
        valor_pago = donation.paid_amount or 0
        dif_percentual = ((valor_pago - valor_previsto) / valor_previsto * 100) if valor_previsto > 0 else 0.0
        
        row_line += f"{dif_percentual:.2f}%".rjust(20)
        printer.print(row_line)
        printer.lineFeed()

    def _generate_report_footer(self, printer, total_previsto, total_recebido, page=1):
        """Generate common report footer"""
        self.print_centered(printer, "-" * self.MAX_LINE_WIDTH)
        printer.lineFeed()
        
        printer.bold(True)
        diferenca_total = ((total_recebido - total_previsto) / total_previsto * 100) if total_previsto > 0 else 0.0
        
        printer.print(self._linha_pontilhada(
            "Total Previsto", 
            f":{locale.currency(total_previsto, grouping=True)}"
        ))
        printer.lineFeed()
        
        printer.print(self._linha_pontilhada(
            "Total Recebido", 
            f":{locale.currency(total_recebido, grouping=True)}"
        ))
        printer.lineFeed()
        
        printer.print(self._linha_pontilhada(
            "Diferença", 
            f":{diferenca_total:.2f}%"
        ))
        printer.bold(False)
        printer.lineFeed(2)
        
        self.print_centered(printer, f"--- Página {page} ---")
        
        printer.formFeed()
        printer.reset()

    def _generate_page_footer(self, printer, total_previsto, total_recebido, page):
        """Generate page footer with subtotals"""
        self.print_centered_condensed(printer, "-" * self.MAX_LINE_WIDTH_CONDENSED)
        printer.lineFeed()
        
        printer.print(self._linha_pontilhada(
            "Subtotal Previsto", 
            f":{locale.currency(total_previsto, grouping=True)}",
            self.MAX_LINE_WIDTH_CONDENSED
        ))
        printer.lineFeed()
        
        printer.print(self._linha_pontilhada(
            "Subtotal Recebido", 
            f":{locale.currency(total_recebido, grouping=True)}",
            self.MAX_LINE_WIDTH_CONDENSED
        ))
        printer.lineFeed()
        
        self.print_centered_condensed(printer, f"--- Página {page} ---")
        printer.lineFeed()
        
class BaseReportForm(forms.Form):
    """Base form for all report types with common date fields"""
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
    start_date = forms.DateField(
        label=_("Data inicial"), 
        required=True, 
        widget=forms.DateInput(attrs={'type': 'date', 'value': datetime.now().date(), 'class': 'form-control'})
    )
    end_date = forms.DateField(
        label=_("Data final"), 
        required=True, 
        widget=forms.DateInput(attrs={'type': 'date', 'value': datetime.now().date(), 'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date and end_date < start_date:
            self.add_error('end_date', _("A data final não pode ser anterior à data inicial."))


class GeneralReportForm(BaseReportForm):
    """Form for general reports (only date fields)"""
    pass


class EmployeeReportForm(BaseReportForm):
    """Form for employee-specific reports"""
    created_by = forms.ModelChoiceField(
        label=_("Funcionário"),
        required=True,
        queryset=Employee.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.request:
            user = self.request.user
            if user.is_superuser:
                self.fields['created_by'].queryset = Employee.objects.all()
            else:
                self.fields['created_by'].queryset = Employee.objects.filter(owner=user.profile.company)


class DonorReportForm(BaseReportForm):
    """Form for donor-specific reports"""
    donor = forms.ModelChoiceField(
        label=_("Doador"),
        required=True,
        queryset=Donor.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    autocomplete_fields = ['donor']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.request:
            user = self.request.user
            if user.is_superuser:
                self.fields['donor'].queryset = Donor.objects.all()
            else:
                self.fields['donor'].queryset = Donor.objects.filter(owner=user.profile.company)

class ReportsAdminView(admin.ModelAdmin, ReportBuilderMixin):
    """Admin view for generating donation reports"""

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.has_perm('donation.view_report')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def _get_filtered_donations(self, request, start_date=None, end_date=None):
        """Get donations filtered by permissions and date range"""
        donations = Donation.objects.all()
        if not request.user.is_superuser:
            donations = donations.filter(owner=request.user.profile.company)
        if start_date:
            donations = donations.filter(expected_at__gte=start_date)
        if end_date:
            donations = donations.filter(expected_at__lte=end_date)
        return donations
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('print/', self.admin_site.admin_view(self.print_receipt_view), name='donation_print_receipt'),
        ]
        return custom_urls + urls

    def print_receipt_view(self, request):
        """Nova view apenas para receber a requisição de impressão via AJAX"""
        if not self.has_view_permission(request):
            raise PermissionDenied

        if request.method != "POST" or request.headers.get('x-requested-with') != 'XMLHttpRequest':
            return JsonResponse({"error": "Requisição inválida."}, status=400)

        report_type = request.POST.get("report_type")
        if not report_type:
            return JsonResponse({"error": "Tipo de relatório não informado."}, status=400)
        action = request.POST.get("action")
            
        context = self._build_report_context(request, report_type)

        receipt_bytes = context["receipts"].get(report_type) or b''
        
        if action == "download":
            return HttpResponse(
                receipt_bytes,
                content_type="application/pdf",
                headers={"Content-Disposition": 'attachment; filename="relatorio_doacoes.pdf"'}
            )


        if not receipt_bytes:
            return JsonResponse({"error": "Nenhum relatório gerado para imprimir."}, status=400)
        
        try:
            settings = DonationSettings.get_solo()
            if not settings:
                logger.error("Configurações de doação não encontradas no banco de dados")
                return JsonResponse({"error": "Configurações do sistema não encontradas."}, status=400)


            printer_name = settings.default_printer
            if not printer_name or not printer_name.strip():
                logger.error("Nenhuma impressora padrão configurada")
                return JsonResponse({"error": "Nenhuma impressora padrão configurada."}, status=400)

            self._send_to_printer(receipt_bytes, printer_name)
        except Exception as e:
            logger.exception("Erro ao enviar para a impressora.")
            return JsonResponse({"error": f"Erro ao imprimir: {str(e)}"}, status=500)

        return JsonResponse({"success": True})


    def _send_to_printer(self, content_bytes, printer_name=None):
        """Envia bytes de conteúdo para a impressora"""
        with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
            tmpfile.write(content_bytes)
            tmpfile_path = tmpfile.name

        try:
            if platform.system() == "Windows":
                import win32print
                if not printer_name:
                    printer_name = win32print.GetDefaultPrinter()

                hprinter = win32print.OpenPrinter(printer_name)
                try:
                    job = win32print.StartDocPrinter(hprinter, 1, ("Impressão de Relatório", None, "RAW"))
                    win32print.StartPagePrinter(hprinter)
                    with open(tmpfile_path, "rb") as f:
                        win32print.WritePrinter(hprinter, f.read())
                    win32print.EndPagePrinter(hprinter)
                    win32print.EndDocPrinter(hprinter)
                finally:
                    win32print.ClosePrinter(hprinter)
            else:
                subprocess.run(["lpr", "-P", "LX-300", "-o", "raw", tmpfile_path])
        finally:
            os.remove(tmpfile_path)
            
    def changelist_view(self, request, extra_context=None):
        if not self.has_view_permission(request):
            raise PermissionDenied
        
        report_type = request.GET.get("report_type")
        context = self._build_report_summary_context(request, report_type)
        
        return TemplateResponse(request, "admin/donation/reports.html", context)

    def _build_report_context(self, request, report_type):
        """Build context dictionary for the template"""
        forms = {
            'individual': EmployeeReportForm(
                request.POST if report_type == "individual" else None, 
                request=request
            ),
            'general': GeneralReportForm(
                request.POST if report_type == "general" else None,
                request=request
            ),
            'donor': DonorReportForm(
                request.POST if report_type == "donor" else None,  
                request=request
            )
        }

        receipts = {
            'individual': b'',
            'general': b'',
            'donor': b''
        }
        action = request.POST.get("action")
    
        if report_type in forms and forms[report_type].is_valid():            
            data = forms[report_type].cleaned_data
            donations = self._get_filtered_donations(
                request, 
                data.get("start_date"), 
                data.get("end_date")
            )

            if report_type == "individual" and data.get("created_by"):
                try:
                    employee_user = EmployeeUser.objects.get(employee=data["created_by"])
                    
                    if action == "download":
                        receipts['individual'] = report_pdf.generate_employee_report_pdf(
                            employee_user.employee,
                            donations.filter(created_by=employee_user.user),
                            data["start_date"],
                            data["end_date"],
                        )
                    else:
                        receipts['individual'] = self._generate_employee_report(
                            data["start_date"],
                            data["end_date"],
                            employee_user.employee,
                            donations.filter(created_by=employee_user.user)
                        )
                except EmployeeUser.DoesNotExist:
                    logger.error(f"EmployeeUser not found for employee: {data['created_by']}")

            elif report_type == "donor" and data.get("donor"):
                if action == "download":
                    receipts['donor'] = report_pdf.generate_donor_report_pdf(
                        data["donor"],
                        donations.filter(donor=data["donor"]),
                        data["start_date"],
                        data["end_date"],
                    )
                else:
                    receipts['donor'] = self._generate_donor_report(
                        data["start_date"],
                        data["end_date"],
                        data["donor"],
                        donations.filter(donor=data["donor"])
                    )

            elif report_type == "general":
                if action == "download":
                    receipts['general'] = report_pdf.generate_general_report(
                        request.user,
                        data["start_date"],
                        data["end_date"],
                        donations
                    )
                else:
                    receipts['general'] = self._generate_general_report(
                        request.user,
                        data["start_date"],
                        data["end_date"],
                        donations
                    )
            
        return {
            "report_type": report_type,
            "receipts": receipts,
        }

    def _generate_employee_report(self, start_date, end_date, employee, donations):
        """Generate employee report using mixin methods"""
        printer = ESCPrinter()
        printer.initialize()
        printer.setMargins(2, 80)
        self._generate_report_header(
            printer,
            employee.owner,
            "RELATÓRIO DE VALORES RECEBIDOS POR FUNCIONÁRIO"
        )
        
        self.print_line_side_by_side(printer, f"Código..............: {employee.id}", "")
        self.print_line_side_by_side(printer, f"Funcionário.........: {employee.name}", "")
        self.print_line_side_by_side(
            printer,
            f"Período.............: {start_date.strftime('%d/%m/%Y')} até {end_date.strftime('%d/%m/%Y')}",
            ""
        )
        printer.lineFeed()

        self._generate_table_header(printer)
        total_previsto = 0
        total_recebido = 0
        page = 1
        first_page_items = 42  # Itens na primeira página (com cabeçalho)
        other_pages_items = 60  # Itens nas demais páginas
        items_per_page = first_page_items
        item_count = 0

        printer.condensed(True)

        for donation in list(donations):
            total_previsto += donation.amount or 0
            total_recebido += donation.paid_amount or 0
            self._generate_donation_row(printer, donation)
            item_count += 1

            # Verifica se precisa quebrar a página
            if item_count == items_per_page:
                self._generate_page_footer(printer, total_previsto, total_recebido, page)
                page += 1
                item_count = 0  # Reinicia contagem da nova página
                items_per_page = other_pages_items  # A partir da segunda página, usa mais itens

        printer.condensed(False)

        # Rodapé final da última página
        self._generate_report_footer(printer, total_previsto, total_recebido, page)
        return printer.build()

    def _generate_donor_report(self, start_date, end_date, donor, donations):
        """Generate donor report using mixin methods"""
        printer = ESCPrinter()
        printer.initialize()
        printer.setMargins(2, 80)

        self._generate_report_header(
            printer,
            donor.owner,
            "RELATÓRIO DE VALORES RECEBIDOS POR DOADOR"
        )
        
        self.print_line_side_by_side(printer, f"Código..............: {donor.id}", "")
        self.print_line_side_by_side(printer, f"Doador..............: {donor.name}", "")
        self.print_line_side_by_side(
            printer,
            f"Período.............: {start_date.strftime('%d/%m/%Y')} até {end_date.strftime('%d/%m/%Y')}",
            ""
        )
        printer.lineFeed()

        self._generate_table_header(printer)
        total_previsto = 0
        total_recebido = 0
        page = 1
        first_page_items = 42  # Itens na primeira página (com cabeçalho)
        other_pages_items = 60  # Itens nas demais páginas
        items_per_page = first_page_items
        item_count = 0

        printer.condensed(True)

        for donation in list(donations):
            total_previsto += donation.amount or 0
            total_recebido += donation.paid_amount or 0
            self._generate_donation_row(printer, donation)
            item_count += 1

            # Verifica se precisa quebrar a página
            if item_count == items_per_page:
                self._generate_page_footer(printer, total_previsto, total_recebido, page)
                page += 1
                item_count = 0  # Reinicia contagem da nova página
                items_per_page = other_pages_items  # A partir da segunda página, usa mais itens

        printer.condensed(False)
        # Rodapé final da última página
        self._generate_report_footer(printer, total_previsto, total_recebido, page)
        return printer.build()

    def _generate_general_report(self, user, start_date, end_date, donations):
        """Generate general report using mixin methods"""
        printer = ESCPrinter()
        printer.initialize()
        printer.setMargins(2, 80)

        self._generate_report_header(
            printer,
            user.profile.company,
            "RELATÓRIO GERAL DE DOAÇÕES"
        )
        
        self.print_line_side_by_side(
            printer,
            f"Período.............: {start_date.strftime('%d/%m/%Y')} até {end_date.strftime('%d/%m/%Y')}",
            ""
        )
        printer.lineFeed()

        self._generate_table_header(printer)
        total_previsto = 0
        total_recebido = 0
        page = 1
        first_page_items = 45  # Itens na primeira página (com cabeçalho)
        other_pages_items = 60  # Itens nas demais páginas
        items_per_page = first_page_items
        item_count = 0

        printer.condensed(True)

        for donation in list(donations):
            total_previsto += donation.amount or 0
            total_recebido += donation.paid_amount or 0
            self._generate_donation_row(printer, donation)
            item_count += 1

            # Verifica se precisa quebrar a página
            if item_count == items_per_page:
                self._generate_page_footer(printer, total_previsto, total_recebido, page)
                page += 1
                item_count = 0  # Reinicia contagem da nova página
                items_per_page = other_pages_items  # A partir da segunda página, usa mais itens

        printer.condensed(False)

        # Rodapé final da última página
        self._generate_report_footer(printer, total_previsto, total_recebido, page)

        return printer.build()

    def _build_report_summary_context(self, request, report_type):
        """Build context dictionary for the template"""
        forms = {
            'individual': EmployeeReportForm(
                request.GET if report_type == "individual" else None, 
                request=request
            ),
            'general': GeneralReportForm(
                request.GET if report_type == "general" else None,
                request=request
            ),
            'donor': DonorReportForm(
                request.GET if report_type == "donor" else None,  
                request=request
            )
        }

        summary_data = {
            'individual': None,
            'general': None,
            'donor': None
        }

        if report_type in forms and forms[report_type].is_valid():
            data = forms[report_type].cleaned_data
            donations = self._get_filtered_donations(
                request, 
                data.get("start_date"), 
                data.get("end_date")
            )

            if report_type == "individual" and data.get("created_by"):
                try:
                    employee_user = EmployeeUser.objects.get(employee=data["created_by"])
                    filtered_donations = donations.filter(created_by=employee_user.user)
                    summary_data['individual'] = self._generate_summary(
                        employee_user.employee.name,
                        data["start_date"],
                        data["end_date"],
                        filtered_donations
                    )
                except EmployeeUser.DoesNotExist:
                    logger.error(f"EmployeeUser not found for employee: {data['created_by']}")

            elif report_type == "donor" and data.get("donor"):
                filtered_donations = donations.filter(donor=data["donor"])
                summary_data['donor'] = self._generate_summary(
                    data["donor"].name,
                    data["start_date"],
                    data["end_date"],
                    filtered_donations
                )

            elif report_type == "general":
                summary_data['general'] = self._generate_summary(
                    "Resumo",
                    data["start_date"],
                    data["end_date"],
                    donations
                )
        
        return {
            **self.admin_site.each_context(request),
            "title": _("Relatórios de Doações"),
            "report_type": report_type,
            "summary_data": summary_data,
            "individual_form": forms['individual'],
            "general_form": forms['general'],
            "donor_form": forms['donor'],
        }

    def _generate_summary(self, title, start_date, end_date, donations):
        """Generate a simplified summary with only totals"""
        total_previsto = sum(d.amount or 0 for d in donations)
        total_recebido = sum(d.paid_amount or 0 for d in donations)
        
        try:
            dif_percentual = ((total_recebido - total_previsto) / total_previsto * 100) if total_previsto > 0 else 0.0
        except ZeroDivisionError:
            dif_percentual = 0.0

        return {
            'title': title,
            'periodo': f"{start_date.strftime('%d/%m/%Y')} a {end_date.strftime('%d/%m/%Y')}",
            'total_donations': donations.count(),
            'total_previsto': locale.currency(total_previsto, grouping=True),
            'total_recebido': locale.currency(total_recebido, grouping=True),
            'dif_percentual': f"{dif_percentual:.2f}%",
        }

    def _calculate_difference(self, expected, received):
        """Calculate the difference between expected and received amounts"""
        if expected == 0:
            return "0.00%"
        difference = ((received - expected) / expected * 100)
        return f"{difference:.2f}%"
    
class Report(models.Model):
    class Meta:
        verbose_name = "Relatório"
        verbose_name_plural = "Relatórios"
        app_label = "donation"
        managed = False