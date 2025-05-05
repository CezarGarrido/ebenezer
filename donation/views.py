import locale
from django.contrib import admin
from django import forms
from django.db import models
from core.escbuilder.escbuilder import ESCBuilder
from django.core.exceptions import ObjectDoesNotExist
from core.models.donor import Donor
from core.models.employee import Employee, EmployeeUser
from .models import Donation
from django.utils.translation import gettext_lazy as _
from django.template.response import TemplateResponse
from datetime import datetime
from django.core.exceptions import PermissionDenied

class BaseReportForm(forms.Form):
    """Base form for all report types with common date fields"""
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
    start_date = forms.DateField(
        label="Data inicial", 
        required=True, 
        widget=forms.DateInput(attrs={'type': 'date', 'value': datetime.now().date(), 'class': 'form-control'})
    )
    end_date = forms.DateField(
        label="Data final", 
        required=True, 
        widget=forms.DateInput(attrs={'type': 'date', 'value': datetime.now().date(), 'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date and end_date < start_date:
            self.add_error('end_date', "A data final não pode ser anterior à data inicial.")


class GeneralReportForm(BaseReportForm):
    """Form for general reports (only date fields)"""
    pass


class EmployeeReportForm(BaseReportForm):
    """Form for employee-specific reports"""
    created_by = forms.ModelChoiceField(
        label="Funcionário",
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
        label="Doador",
        required=True,
        queryset=Donor.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.request:
            user = self.request.user
            if user.is_superuser:
                self.fields['donor'].queryset = Donor.objects.all()
            else:
                self.fields['donor'].queryset = Donor.objects.filter(owner=user.profile.company)


class ReportBuilderMixin:
    """Mixin containing common report building functionality"""
    
    CENTER_WIDTH = 66
    PAGE_WIDTH = CENTER_WIDTH + 40
    
    def _linha_lado_lado(self, esquerda, direita, largura=None):
        largura = largura or self.PAGE_WIDTH
        return f"{esquerda}{' ' * (largura - len(esquerda) - len(direita))}{direita}"
  
    def _linha_pontilhada(self, esquerda, direita, largura=None):
        largura = largura or self.PAGE_WIDTH
        return f"{esquerda}{'.' * (largura - len(esquerda) - len(direita))}{direita}"

    def _build_report_header(self, builder, company, title):
        """Build common header for all reports"""
        builder.text(self._linha_lado_lado(
            company.name, 
            f"Emissão: {datetime.now().strftime('%d/%m/%Y')}"
        )).linefeed()
        
        try:
            legal = company.legalentity
            cnpj = legal.cnpj or "-"
        except ObjectDoesNotExist:
            cnpj = "-"

        builder.text(self._linha_lado_lado(
            "Inscrição Estadual Nº ISENTO",
            f"C.G.C Nº: {cnpj}"
        )).linefeed(3)

        builder.bold(True)
        builder.text(title.center(self.PAGE_WIDTH))
        builder.bold(False).linefeed(3)
        return builder

    def _build_report_table_header(self, builder):
        """Build common table header for all reports"""
        builder.text("-" * self.PAGE_WIDTH).linefeed()
        builder.text(
            "CÓDIGO".ljust(10) + 
            "DATA".ljust(12) +
            "DOADOR".ljust(38) + 
            "VALOR PREVISTO".rjust(15) + 
            "   VALOR RECEBIDO".rjust(18) + 
            "   DIFERENÇA".rjust(13)
        ).linefeed()
        builder.text("-" * self.PAGE_WIDTH).linefeed()
        return builder

    def _build_donation_row(self, builder, donation, itens_na_pagina, pagina):
        """Build a single donation row for the report"""
        valor_previsto = donation.amount or 0
        valor_pago = donation.paid_amount or 0

        builder.text(f"{donation.id}".ljust(10))
        
        if donation.expected_at:
            builder.text(f"{donation.expected_at.strftime('%d/%m/%Y')}".ljust(12))
        else:
            builder.text(f"-".ljust(12))

        builder.text(f"{donation.donor.id} - {donation.donor.name}".ljust(38))
       
        amount_formated = locale.currency(donation.amount, grouping=True)
        paid_amount_formated =locale.currency(valor_pago, grouping=True)
        
        builder.text(f"{amount_formated}".rjust(15))
        builder.text(f"{paid_amount_formated}".rjust(18))
        
        dif_percentual = ((valor_pago - valor_previsto) / valor_previsto * 100) if valor_previsto > 0 else 0.0
        builder.text(f"{dif_percentual:.2f}%".rjust(13))
        builder.linefeed()
        
        itens_na_pagina += 1
        if (pagina == 1 and itens_na_pagina == 47) or (pagina > 1 and itens_na_pagina == 62):
            builder.text(f"--- Página {pagina} ---".center(self.PAGE_WIDTH))
            builder.linefeed()
            pagina += 1
            itens_na_pagina = 0
            
        return builder, itens_na_pagina, pagina

    def _build_report_footer(self, builder, total_previsto, total_recebido, pagina):
        """Build common footer for all reports"""
        builder.text("-" * self.PAGE_WIDTH).linefeed()
        builder.linefeed()
        
        diferenca_total = ((total_recebido - total_previsto) / total_previsto * 100) if total_previsto > 0 else 0.0
        
        total_expected_formated = locale.currency(total_previsto, grouping=True)
        total_paid_formated =locale.currency(total_recebido, grouping=True)
        
        builder.text(self._linha_pontilhada("Total Previsto", f":{total_expected_formated}")).linefeed()
        builder.text(self._linha_pontilhada("Total Recebido", f":{total_paid_formated}")).linefeed()
        builder.text(self._linha_pontilhada("Diferença", f":{diferenca_total:.2f}%")).linefeed()
        builder.text(f"--- Página {pagina} ---".center(self.PAGE_WIDTH))
        builder.linefeed().linefeed(2).form_feed()
        return builder


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

    def changelist_view(self, request, extra_context=None):
        if not self.has_view_permission(request):
            raise PermissionDenied

        report_type = request.GET.get("report_type")
        context = self._build_report_context(request, report_type)
        return TemplateResponse(request, "admin/donation/reports.html", context)

    def _build_report_context(self, request, report_type):
        """Build context dictionary for the template"""
        individual_form = EmployeeReportForm(
            request.GET if report_type == "individual" else None, 
            request=request
        )
        general_form = GeneralReportForm(
            request.GET if report_type == "general" else None
        )
        donor_form = DonorReportForm(
            request.GET if report_type == "donor" else None,  
            request=request
        )

        receipt_individual = ""
        receipt_general = ""
        receipt_donor = ""

        if report_type == "individual" and individual_form.is_valid():
            data = individual_form.cleaned_data
            donations = self._get_filtered_donations(
                request, 
                data["start_date"], 
                data["end_date"]
            )
            if data["created_by"]:
                employee = EmployeeUser.objects.get(employee=data["created_by"])
                donations = donations.filter(created_by=employee.user)
            receipt_individual = self.receipt_by_employee(
                data["start_date"], 
                data["end_date"], 
                employee.employee, 
                donations
            )
        elif report_type == "donor" and donor_form.is_valid():
            data = donor_form.cleaned_data
            donations = self._get_filtered_donations(
                request, 
                data["start_date"], 
                data["end_date"]
            )
            if data["donor"]:
                donations = donations.filter(donor=data["donor"])
            receipt_donor = self.receipt_by_donor(
                data["start_date"], 
                data["end_date"], 
                data["donor"],
                donations
            )
        elif report_type == "general" and general_form.is_valid():
            data = general_form.cleaned_data
            donations = self._get_filtered_donations(
                request, 
                data.get("start_date"), 
                data.get("end_date")
            )
            receipt_general = self.receipt_general(
                request.user, 
                data.get("start_date"), 
                data.get("end_date"), 
                donations
            )

        return dict(
            self.admin_site.each_context(request),
            title="Relatórios de Doações",
            report_type=report_type,
            individual_form=individual_form,
            general_form=general_form,
            donor_form=donor_form,
            receipt_individual=receipt_individual,
            receipt_general=receipt_general,
            receipt_donor=receipt_donor,
        )

    def receipt_by_employee(self, start_date, end_date, employee, donations):
        """Generate receipt for employee-specific report"""
        b = ESCBuilder()
        b.set_charset().font(draft=True)
        
        self._build_report_header(
            b, 
            employee.owner, 
            "RELATÓRIO DE VALORES RECEBIDOS POR FUNCIONÁRIO"
        )
        
        b.text(f"Código..............: {employee.id}").linefeed()
        b.text(f"Funcionário.........: {employee.employee.name}").linefeed()
        b.text(f"Período.............: {start_date.strftime('%d/%m/%Y')} até {end_date.strftime('%d/%m/%Y')}").linefeed()
        b.linefeed()

        self._build_report_table_header(b)
        
        total_previsto = 0
        total_recebido = 0
        itens_na_pagina = 0
        pagina = 1
        
        for donation in list(donations) * 30:
            valor_previsto = donation.amount or 0
            total_previsto += valor_previsto
            total_recebido += donation.paid_amount or 0
            
            b, itens_na_pagina, pagina = self._build_donation_row(
                b, donation, itens_na_pagina, pagina
            )

        self._build_report_footer(b, total_previsto, total_recebido, pagina)
        return b.to_html(b.build())

    def receipt_by_donor(self, start_date, end_date, donor, donations):
        """Generate receipt for donor-specific report"""
        b = ESCBuilder()
        b.set_charset().font(draft=True)
        
        self._build_report_header(
            b, 
            donor.owner, 
            "RELATÓRIO DE VALORES RECEBIDOS POR DOADOR"
        )
        
        b.text(f"Código..............: {donor.id}").linefeed()
        b.text(f"Doador..............: {donor.name}").linefeed()
        b.text(f"Período.............: {start_date.strftime('%d/%m/%Y')} até {end_date.strftime('%d/%m/%Y')}").linefeed()
        b.linefeed()

        self._build_report_table_header(b)
        
        total_previsto = 0
        total_recebido = 0
        itens_na_pagina = 0
        pagina = 1
        
        for donation in donations:
            valor_previsto = donation.amount or 0
            total_previsto += valor_previsto
            total_recebido += donation.paid_amount or 0
            
            b, itens_na_pagina, pagina = self._build_donation_row(
                b, donation, itens_na_pagina, pagina
            )

        self._build_report_footer(b, total_previsto, total_recebido, pagina)
        return b.to_html(b.build())

    def receipt_general(self, user, start_date, end_date, donations):
        """Generate receipt for general report"""
        b = ESCBuilder()
        b.set_charset().font(draft=True)
        
        self._build_report_header(b, user.profile.company, "RELATÓRIO GERAL")
        
        b.text("-" * self.PAGE_WIDTH).linefeed()
        b.text(f"Período.............: {start_date.strftime('%d/%m/%Y')} até {end_date.strftime('%d/%m/%Y')}").linefeed()
        b.text("-" * self.PAGE_WIDTH).linefeed()
        b.linefeed()

        self._build_report_table_header(b)
        
        total_previsto = 0
        total_recebido = 0
        itens_na_pagina = 0
        pagina = 1
        
        for donation in list(donations) * 30:
            valor_previsto = donation.amount or 0
            total_previsto += valor_previsto
            total_recebido += donation.paid_amount or 0
            
            b, itens_na_pagina, pagina = self._build_donation_row(
                b, donation, itens_na_pagina, pagina
            )

        self._build_report_footer(b, total_previsto, total_recebido, pagina)
        return b.to_html(b.build())


class Report(models.Model):
    class Meta:
        verbose_name = "Relatório"
        verbose_name_plural = "Relatórios"
        app_label = "donation"
        managed = False