from types import SimpleNamespace
from django.http import HttpResponse, JsonResponse
from django.urls import path
from django.contrib import admin
from django import forms
from django.core.exceptions import PermissionDenied
from django.template.response import TemplateResponse
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Q
import logging
import platform
import subprocess
import tempfile
import os
from datetime import datetime

from donation import report_pdf, report_escp
from .models import Donation, DonationSettings
from core.models.donor import Donor
from core.models.employee import Employee, EmployeeUser

logger = logging.getLogger(__name__)

# -------------------- FORMS --------------------
User = get_user_model()

class BaseReportForm(forms.Form):
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
    pass


class EmployeeReportForm(BaseReportForm):
    created_by = forms.ChoiceField(
        label=_("Funcionário ou Usuário"),
        required=True,
        choices=[],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.request.user if self.request else None
        if user:
            if user.is_superuser:
                employees = Employee.objects.all()
                # usuários que não estão em nenhum EmployeeUser
                linked_user_ids = EmployeeUser.objects.values_list('user_id', flat=True)
                unlinked_users = User.objects.exclude(id__in=linked_user_ids)
            else:
                employees = Employee.objects.filter(owner=user.profile.company)
                linked_user_ids = EmployeeUser.objects.values_list('user_id', flat=True)
                unlinked_users = User.objects.exclude(id__in=linked_user_ids).filter(
                    profile__company=user.profile.company
                )

            employee_choices = [(f"emp:{e.id}", f"{e.name} (Funcionário)") for e in employees]
            user_choices = [(f"user:{u.id}", f"{u} (Usuário)") for u in unlinked_users]

            self.fields['created_by'].choices = [('', '---------')] + employee_choices + user_choices

class DonorReportForm(BaseReportForm):
    donor = forms.ModelChoiceField(
        label=_("Doador"),
        required=True,
        queryset=Donor.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.request.user if self.request else None
        if user:
            if user.is_superuser:
                self.fields['donor'].queryset = Donor.objects.all()
            else:
                self.fields['donor'].queryset = Donor.objects.filter(owner=user.profile.company)


# -------------------- ADMIN --------------------

class ReportsAdminView(admin.ModelAdmin):
    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.has_perm('donation.view_report')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_urls(self):
        return [
            path('print/', self.admin_site.admin_view(self.print_receipt_view), name='donation_print_receipt'),
        ] + super().get_urls()

    def changelist_view(self, request, extra_context=None):
        if not self.has_view_permission(request):
            raise PermissionDenied

        report_type = request.GET.get("report_type")
        context = self._get_context(request, report_type)
        return TemplateResponse(request, "admin/donation/reports.html", context)

    def print_receipt_view(self, request):
        if not self.has_view_permission(request):
            raise PermissionDenied

        if request.method != "POST" or request.headers.get('x-requested-with') != 'XMLHttpRequest':
            return JsonResponse({"error": "Requisição inválida."}, status=400)

        report_type = request.POST.get("report_type")
        action = request.POST.get("action")
        if not report_type:
            return JsonResponse({"error": "Tipo de relatório não informado."}, status=400)

        forms = self._get_forms(request, report_type, request.POST)
        form = forms[report_type]

        if not form.is_valid():
            return JsonResponse({
                "error": "Formulário inválido.",
                "form_errors": form.errors
            }, status=422)

        
        context = self._build_report_context(request, report_type, action, form)
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
            printer_name = settings.default_printer.strip() if settings and settings.default_printer else None
            if not printer_name:
                return JsonResponse({"error": "Nenhuma impressora padrão configurada."}, status=400)

            self._send_to_printer(receipt_bytes, printer_name)
        except Exception as e:
            logger.exception("Erro ao enviar para a impressora.")
            return JsonResponse({"error": f"Erro ao imprimir: {str(e)}"}, status=500)

        return JsonResponse({"success": True})

    def _send_to_printer(self, content_bytes, printer_name):
        with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
            tmpfile.write(content_bytes)
            tmpfile_path = tmpfile.name

        try:
            if platform.system() == "Windows":
                import win32print
                hprinter = win32print.OpenPrinter(printer_name)
                try:
                    win32print.StartDocPrinter(hprinter, 1, ("Relatório", None, "RAW"))
                    win32print.StartPagePrinter(hprinter)
                    with open(tmpfile_path, "rb") as f:
                        win32print.WritePrinter(hprinter, f.read())
                    win32print.EndPagePrinter(hprinter)
                    win32print.EndDocPrinter(hprinter)
                finally:
                    win32print.ClosePrinter(hprinter)
            else:
                subprocess.run(["lpr", "-P", printer_name, "-o", "raw", tmpfile_path], check=True)
        finally:
            os.remove(tmpfile_path)

    def _get_filtered_donations(self, request, start_date=None, end_date=None):
        queryset = Donation.objects.all()
        if not request.user.is_superuser:
            queryset = queryset.filter(owner=request.user.profile.company)
        if start_date:
            queryset = queryset.filter(expected_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(expected_at__lte=end_date)
        return queryset

    def _get_forms(self, request, report_type, data_source):
        return {
            'individual': EmployeeReportForm(data_source if report_type == "individual" else None, request=request),
            'general': GeneralReportForm(data_source if report_type == "general" else None, request=request),
            'donor': DonorReportForm(data_source if report_type == "donor" else None, request=request)
        }

    def _get_context(self, request, report_type):
        forms = self._get_forms(request, report_type, request.GET)
        return {
            **self.admin_site.each_context(request),
            "title": _("Relatórios de Doações"),
            "report_type": report_type,
            "individual_form": forms['individual'],
            "general_form": forms['general'],
            "donor_form": forms['donor']
        }

    def _build_report_context(self, request, report_type, action, form):
        data = form.cleaned_data
        donations = self._get_filtered_donations(request, data.get("start_date"), data.get("end_date"))
        receipts = {"individual": b"", "general": b"", "donor": b""}

        if report_type == "individual" and data.get("created_by"):
            value = data["created_by"]
            try:
                prefix, obj_id = value.split(":")
                if prefix == "emp":
                    employee = Employee.objects.get(id=obj_id)
                    employee_user = EmployeeUser.objects.filter(employee=employee).first()
                    if employee_user:
                        filtered_donations = donations.filter(
                            Q(received_by=employee) | Q(received_by__isnull=True, created_by=employee_user.user)
                        )
                    else:
                        filtered_donations = donations.filter(received_by=employee)
       
                    receipts["individual"] = report_pdf.generate_employee_report_pdf(
                        employee,
                        filtered_donations,
                        data["start_date"],
                        data["end_date"]
                    ) if action == "download" else report_escp.generate_employee_report(
                        employee,
                        data["start_date"],
                        data["end_date"],
                        filtered_donations
                    )
                elif prefix == "user":
                    user = User.objects.get(id=obj_id)

                    # Tenta encontrar vínculo atual com algum funcionário
                    employee_user = EmployeeUser.objects.filter(user=user).first()

                    if employee_user:
                        employee = employee_user.employee
                        employee_filter = Q(received_by=employee)
                    else:
                        # Alternativa: encontra todos os funcionários que têm doações criadas por esse user
                        employee_ids = donations.filter(created_by=user, received_by__isnull=False).values_list("received_by_id", flat=True)
                        employee_filter = Q(received_by__in=employee_ids)

                    # Filtro final: doações criadas pelo user ou recebidas por funcionários ligados ao user
                    filtered_donations = donations.filter(
                        Q(created_by=user) | employee_filter
                    ).distinct()

                    fake_employee = SimpleNamespace(
                        id=user.id,
                        name=user.get_full_name() or user.username,
                        owner=user.profile.company
                    )

                    receipts["individual"] = report_pdf.generate_employee_report_pdf(
                        fake_employee,
                        filtered_donations,
                        data["start_date"],
                        data["end_date"]
                    ) if action == "download" else report_escp.generate_employee_report(
                        fake_employee,
                        data["start_date"],
                        data["end_date"],
                        filtered_donations
                    )

            except (ValueError, Employee.DoesNotExist, User.DoesNotExist) as e:
                logger.warning(f"Erro ao processar created_by: {e}")

        elif report_type == "donor" and data.get("donor"):
            receipts["donor"] = report_pdf.generate_donor_report_pdf(
                data["donor"],
                donations.filter(donor=data["donor"]),
                data["start_date"],
                data["end_date"]
            ) if action == "download" else report_escp.generate_donor_report(
                data["donor"],
                data["start_date"],
                data["end_date"],
                donations.filter(donor=data["donor"])
            )

        elif report_type == "general":
            receipts["general"] = report_pdf.generate_general_report(
                request.user,
                data["start_date"],
                data["end_date"],
                donations
            ) if action == "download" else report_escp.generate_general_report(
                request.user,
                data["start_date"],
                data["end_date"],
                donations
            )

        return {"report_type": report_type, "receipts": receipts}


# -------------------- DUMMY MODEL --------------------

class Report(models.Model):
    class Meta:
        verbose_name = "Relatório"
        verbose_name_plural = "Relatórios"
        app_label = "donation"
        managed = False
