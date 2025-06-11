import datetime
import locale
import subprocess
from django.contrib import messages
from django.contrib import admin
from django import forms
import urllib.parse
from core.models.donor import Donor
from core.models.employee import Employee, EmployeeUser
from donation.views import Report, ReportsAdminView
from .models import Donation, DonationSettings
from django.utils.html import format_html
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from .models import ThankYouMessage, ThankYouMessageLine, PAYMENT_METHOD_CHOICES
import platform
from django.utils.safestring import mark_safe

import logging
logger = logging.getLogger(__name__)
            
class ThankYouMessageLineInline(admin.TabularInline):
    model = ThankYouMessageLine
    extra = 0

@admin.register(ThankYouMessage)
class ThankYouMessageAdmin(admin.ModelAdmin):
    inlines = [ThankYouMessageLineInline]
    list_display = ['name','get_lines', 'created_by', 'created_at', 'updated_at']
    readonly_fields = ("created_by", "created_at",)
    exclude = ("owner", "created_by")
    search_fields = ("get_lines",)
    def save_model(self, request, obj, form, change):
        if not obj.created_by:  # Define apenas se for um novo objeto
            obj.created_by = request.user
            obj.owner = request.user.profile.company
        super().save_model(request, obj, form, change)
    
    def get_lines(self, obj):
        return obj.get_lines_text()
    
    get_lines.short_description ="Mensagem"
    
    def get_model_perms(self, request):
        # Retorna permissões vazias para esconder da sidebar
        return {}


class DonationSettingsForm(forms.ModelForm):
    class Meta:
        model = DonationSettings
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Obter lista de impressoras disponíveis
        printers = self.get_printers()
        
        # Criar choices para o campo default_printer
        printer_choices = [('', '---------')]  # Opção vazia
        printer_choices += [(printer, printer) for printer in printers]
        
        # Atualizar o campo no formulário
        self.fields['default_printer'].widget = forms.Select(choices=printer_choices)
    
    def get_printers(self):
        """Retorna a lista de impressoras disponíveis no sistema"""
        printers = []
        
        if platform.system() == "Windows":
            import win32print
            try:
                flags = win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
                printers_info = win32print.EnumPrinters(flags)
                printers = [printer[2] for printer in printers_info]
            except Exception:
                printers = ["Erro ao obter impressoras - verifique permissões"]
        else:
            # Para Linux/Mac
            try:
                output = subprocess.check_output(["lpstat", "-e"]).decode().splitlines()
                printers = output
            except Exception:
                printers = ["Erro ao obter impressoras - verifique se o CUPS está instalado"]
        
        return printers
    def clean(self):
        cleaned_data = super().clean()
        # Verifica se já existe um registro e se este não é o registro existente
        if DonationSettings.objects.exists() and not self.instance.pk:
            raise forms.ValidationError("Já existe um registro de configuração. Você pode apenas editá-lo.")
        return cleaned_data
    
@admin.register(DonationSettings)
class DonationSettingsAdmin(admin.ModelAdmin):
    form = DonationSettingsForm
    list_display = ('thank_you_message', 'default_printer', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    exclude = ('owner', 'created_by')
    
    def has_add_permission(self, request):
        # Impede a criação de novos registros se já existir um
        return not DonationSettings.objects.exists()
    
    def save_model(self, request, obj, form, change):
        # Garante que o owner seja definido automaticamente
        if not obj.created_by:  # Define apenas se for um novo objeto
            obj.created_by = request.user
            obj.owner = request.user.profile.company
        super().save_model(request, obj, form, change)

    def get_model_perms(self, request):
        # Retorna permissões vazias para esconder da sidebar
        return {}

class GenderedMessageMixin:
    """
    Corrige automaticamente mensagens do Django Admin de acordo com o gênero e número da entidade.

    Configuração esperada na subclasse Admin:
        - `entity_labels`: dicionário com as formas da entidade, por exemplo:
            {
                'singular': 'doação',
                'plural': 'doações',
                'gender': 'feminine'  # ou 'masculine'
            }
        - `messages_by_action` (opcional): dicionário para customizar mensagens por operação:
            {
                'add': 'A {entity} {link} foi adicionada com sucesso.',
                'change': 'A {entity} {link} foi alterada com sucesso.',
                'delete': 'A {entity} {link} foi excluída com sucesso.',
            }
    """

    entity_labels = {
        'singular': 'entidade',
        'plural': 'entidades',
        'gender': 'feminine',
    }

    messages_by_action = {
        'add':     {'feminine': 'A {entity} "{link}" foi adicionada com sucesso.',
                    'masculine': 'O {entity} "{link}" foi adicionado com sucesso.'},
        'change':  {'feminine': 'A {entity} "{link}" foi alterada com sucesso.',
                    'masculine': 'O {entity} "{link}" foi alterado com sucesso.'},
        'delete':  {'feminine': 'A {entity} "{link}" foi excluída com sucesso.',
                    'masculine': 'O {entity} "{link}" foi excluído com sucesso.'},
    }

    def message_user(self, request, message, level=messages.SUCCESS, extra_tags='', fail_silently=False):
        if not isinstance(message, str):
            return super().message_user(request, message, level, extra_tags, fail_silently)

        labels = self.entity_labels
        gender = labels.get('gender', 'masculine')
        singular = labels.get('singular', 'entidade')

        # Detecta se há link
        link_start = message.find('<a href="')
        has_link = link_start != -1

        if has_link:
            link_end = message.find('</a>') + 4
            link_html = message[link_start:link_end]
            obj_name = message.split('>')[-2].split('<')[0]
            url = link_html.split('"')[1]
            link = format_html('<a href="{}">{}</a>', url, obj_name)
            
        else:
            link = singular

        # Detecta tipo de operação (rústico mas funcional)
        action = 'change'  # padrão
        lowered = message.lower()
        if 'adicionado' in lowered or 'adicionada' in lowered:
            action = 'add'
        elif 'deletado' in lowered or 'deletada' in lowered:
            action = 'delete'

        # Gera nova mensagem formatada
        template = self.messages_by_action.get(action, {}).get(gender)
        if template:
            new_message = format_html(template.format(entity=singular, link=link))
            message = new_message

        return super().message_user(request, message, level, extra_tags, fail_silently)

        
class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = "__all__"

        widgets = {
            'amount': forms.TextInput(attrs={'data-mask-money': ""}),
            'paid_amount': forms.TextInput(attrs={'data-mask-money': ""}),
            'expected_at': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
            'paid_at': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
        }


    class Media:
        js = ("js/vendor/jquery.mask.min.js", "js/mask/money.js", "js/payment.js", "js/save_date.js",)  # Adicionamos um script personalizado
        
    def clean(self):
        cleaned_data = super().clean()
        paid = cleaned_data.get("paid")
        paid_amount = cleaned_data.get("paid_amount")
        paid_at = cleaned_data.get("paid_at")
        method = cleaned_data.get("method")

        if paid:
            # 1. Valor recebido é obrigatório e maior que zero
            if paid_amount is None:
                self.add_error("paid_amount", "Informe o valor recebido.")
            elif paid_amount <= 0:
                self.add_error("paid_amount", "O valor recebido deve ser maior que zero.")

            # 2. Data de pagamento é obrigatória
            if paid_at is None:
                self.add_error("paid_at", "Informe a data de pagamento.")

            # 3. Meio de pagamento obrigatório
            if not method:
                self.add_error("method", "Informe o meio de pagamento.")

        else:
            # Se não foi pago, limpa os campos de pagamento
            cleaned_data["paid_amount"] = None
            cleaned_data["paid_at"] = None
            cleaned_data["method"] = None

        return cleaned_data


def action_set_paid(modeladmin, request, queryset):

    atualizadas = 0

    for doacao in queryset:
        if not doacao.paid:
            doacao.paid = True
            doacao.paid_amount = doacao.amount
            try:
                employee_user = EmployeeUser.objects.get(user=doacao.created_by)
                doacao.received_by = employee_user.employee
            except:
                pass

            doacao.paid_at = datetime.datetime.now()
            doacao.save()
            atualizadas += 1

    messages.success(request, f"{atualizadas} doações atualizadas como pagas.")

action_set_paid.short_description = "Marcar como paga (valor total e funcionário atual)"


from .filter import DateRangeFilter

class ExpectedAtFilter(DateRangeFilter):
    parameter_name = "expected_at"
    title = "Dt. Vencimento"

class PaidAtFilter(DateRangeFilter):
    parameter_name = "paid_at"
    title = "Dt. Pagamento"

class DonationAdmin(GenderedMessageMixin, admin.ModelAdmin):
    form = DonationForm
    list_display = ("id", "expected_at", "paid_status", "donor_display", "format_amount", "format_paid_amount", "method", "paid_at", "created_by_display", "received_by_display", "action_buttons")  # Campos visíveis na listagem
    verbose_name = "Doação"
    verbose_name_plural = "Doações"
    entity_labels = {
        'singular': 'Doação',
        'plural': 'Doações',
        'gender': 'feminine',
    }
        # Filtros para facilitar a navegação
    list_filter = (
        ExpectedAtFilter,
        PaidAtFilter,
    )

    class Media:
        js = ("js/vendor/moment.min.js", "js/vendor/datetimerange-picker.js", "js/daterange.js", "js/donation_list.js")  # Adicionamos um script personalizado

    # Campos pesquisáveis
    search_fields = (
        "id",
        "donor__name",     # Nome do doador
        "notes",           # Notas da doação
    )    
    list_per_page = 10  # valor fixo

    autocomplete_fields = ['donor']
    
    exclude = ['owner', 'created_by']

    def donor_display(self, obj):
        return obj.donor.name.upper()
    donor_display.short_description = "Doador"
    donor_display.admin_order_field = "donor"
    
    def created_by_display(self, obj):
        user = obj.created_by
        if not user:
            return "-"

        try:
            # Verifica se existe um EmployeeUser vinculado
            employee_user = user.employeeuser
            name = str(employee_user.employee)  # usa o __str__ do modelo Employee
        except EmployeeUser.DoesNotExist:
            name = user.get_full_name() or user.username


        initials = "".join(part[0].upper() for part in name.split()[:2])

        html = format_html(
            '<span style="'
            'display: inline-block; width: 24px; height: 24px; '
            'line-height: 24px; border-radius: 50%; background-color: #007bff; '
            'color: white; text-align: center; font-size: 12px; margin-right: 8px;">{}</span>'
            '{}',
            initials,
            name
        )
        return html

    def received_by_display(self, obj):
        employee = obj.received_by
        if not employee:
            return "-"
        
        name = employee.name
        initials = "".join(part[0].upper() for part in name.split()[:2])

        html = format_html(
            '<span style="'
            'display: inline-block; width: 24px; height: 24px; '
            'line-height: 24px; border-radius: 50%; background-color: #007bff; '
            'color: white; text-align: center; font-size: 12px; margin-right: 8px;">{}</span>'
            '{}',
            initials,
            name
        )
        return 
        
    received_by_display.short_description = "Recebido por"
    received_by_display.admin_order_field = 'received_by'

    created_by_display.short_description = "Criado por"
    created_by_display.admin_order_field = 'created_by'

    def format_paid_amount(self, obj):
        if not obj.paid_amount:
            return ""
        
        return format_html(
            '<strong style="font-size: 1.1em;">{}</strong>',
            locale.currency(obj.paid_amount, grouping=True),
        )

    format_paid_amount.short_description = "Valor Recebido"
    format_paid_amount.admin_order_field = 'paid_amount'

    def action_buttons(self, obj):
        from django.urls import reverse
        modal_id = f"modal-baixa-{obj.pk}"
        url_payment = reverse('admin:donation_donation_change', args=[obj.pk]) + '#informações-de-pagamento-tab'
        change_url = reverse("admin:donation_donation_change", args=[obj.pk])
        print_url = reverse("admin:donation_donation_changelist") + f'?action=print_batch&ids={obj.pk}'

        btn_edit = format_html(
            '<a href="{}" '
            'class="btn btn-sm btn-primary me-2" '
            'title="Editar Doação #{}">'
            '<i class="fas fa-pencil-alt"></i> Editar</a>',
            change_url, obj.pk
        )

        btn_delete = format_html(
            '<a class="btn btn-sm btn-danger me-2" href="{}" title="Excluir Doação #{}"><i class="fas fa-trash"></i> Excluir</a>',
            reverse('admin:donation_donation_delete', args=[obj.pk]), obj.pk
        )

        btn_print = format_html(
            '<a class="btn btn-sm btn-outline-dark me-2" href="{}" title="Imprimir Doação #{}"><i class="fas fa-print"></i> Recibo</a>',
            print_url, obj.pk
        )

        return format_html('{} {} {}', btn_edit, btn_delete, btn_print)

    action_buttons.short_description = ''
    action_buttons.allow_tags = True

    def get_exclude(self, request, obj=None):
        exclude = list(super().get_exclude(request, obj) or [])
        if request.user.is_superuser and 'created_by' in exclude:
            exclude.remove('created_by')
        return exclude

    def save_model(self, request, obj, form, change):
        if not obj.received_by: 
            try:
             obj.received_by = EmployeeUser.objects.get(user=request.user).employee
            except:
                pass  # Ou raise, ou log, conforme a lógica do seu sistema
            
        if not obj.created_by:  # Define apenas se for um novo objeto
            obj.created_by = request.user
            obj.owner = request.user.profile.company
        super().save_model(request, obj, form, change)
        
    fieldsets = (
        ("Informações da Doação", {
            "fields": ("donor", "amount", "expected_at", "notes", "created_by", "created_at", "updated_at")
        }),
        ("Informações de Pagamento", {
            "fields": ("paid", "paid_at", "paid_amount", "method", "received_by"),
            "classes": ("collapse",)  # ou remova isso para deixar sempre visível
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        base_readonly = ["created_at", "updated_at", "get_receipt"]

        if not request.user.is_superuser:
            base_readonly.append("created_by")

        return base_readonly

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        user_company = request.user.profile.company
        if db_field.name == "donor":
            kwargs["queryset"] = Donor.objects.filter(owner=user_company)
        elif db_field.name == "received_by":
            kwargs["queryset"] = Employee.objects.filter(owner=user_company)
        elif db_field.name == "thank_you_message":
            kwargs["queryset"] = ThankYouMessage.objects.filter(owner=user_company)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def format_amount(self, obj):
        return locale.currency(obj.amount, grouping=True)
    
    def paid_status(self, obj):
        if obj.paid:
            return format_html('<span class="badge badge-success" title="Doação paga">Pago</span>')
        # Ainda dentro do prazo
        return format_html('<span class="badge badge-warning" title="Aguardando pagamento">Aguardando Pagamento</span>')

    paid_status.short_description = "Situação"
    paid_status.admin_order_field = 'paid'

    format_amount.short_description = "Valor Esperado"
    format_amount.admin_order_field = 'amount'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        action = request.GET.get("action")
        obj = self.get_object(request, object_id)

        if action == "download_receipt_pdf":
            try:
                settings = DonationSettings.get_solo()
                if not settings:
                    messages.error(request, "Configurações do sistema não encontradas.")
                    logger.error("Configurações de doação não encontradas no banco de dados")
                    return HttpResponseRedirect(request.path)

                content_pdf = obj.get_receipt_pdf(settings)  # deve retornar o conteúdo binário do PDF
                response = HttpResponse(content_pdf, content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename=recibo_de_doacao_{obj.pk}.pdf'
                return response

            except Exception as e:
                messages.error(request, "Erro ao gerar o PDF.")
                logger.error(f"Erro ao gerar PDF: {str(e)}", exc_info=True)
                return HttpResponseRedirect(request.path)

        elif action == "print_receipt":
            try:
                logger.info(f"Iniciando processo de impressão de recibo para doação ID: {obj.id}")
                if not obj or not obj.pk:
                    messages.error(request, "Doação inválida ou não encontrada.")
                    logger.error(f"Objeto de doação inválido: {obj}")
                    return HttpResponseRedirect(request.path)

                settings = DonationSettings.get_solo()
                if not settings:
                    messages.error(request, "Configurações do sistema não encontradas.")
                    logger.error("Configurações de doação não encontradas no banco de dados")
                    return HttpResponseRedirect(request.path)

                printer_name = settings.default_printer
                if not printer_name or not printer_name.strip():
                    messages.error(request, "Nenhuma impressora padrão configurada.")
                    logger.error("Nenhuma impressora configurada nas settings")
                    return HttpResponseRedirect(request.path)

                obj.print_receipt(settings)
                messages.success(request, f"Recibo enviado com sucesso para a impressora: {printer_name}")
                logger.info(f"Recibo impresso com sucesso para doação ID: {obj.id}")

            except Exception as e:
                messages.error(request, "Erro ao imprimir o recibo.")
                logger.error(f"Erro ao imprimir recibo: {str(e)}", exc_info=True)
                return HttpResponseRedirect(request.path)

            return HttpResponseRedirect(request.path)

        # Fluxo padrão
        return super().change_view(request, object_id, form_url, extra_context)
    
    def changelist_view(self, request, extra_context=None):
        action = request.GET.get("action")
        if action == "print_batch":
            ids = request.GET.getlist("ids")
            if not ids:
                messages.error(request, "Nenhuma doação selecionada.")
                return super().changelist_view(request, extra_context)

            # Imprime em lote
            try:
                settings = DonationSettings.get_solo()
                printer_name = settings.default_printer

                for pk in ids:
                    obj = self.model.objects.get(pk=pk)
                    obj.print_receipt(settings)

                messages.success(request, f"{len(ids)} recibo(s) enviados para a impressora {printer_name}.")

            except Exception as e:
                messages.error(request, "Erro ao imprimir em lote.")
                logger.error(f"Erro ao imprimir em lote: {str(e)}", exc_info=True)

            # Retorna à tela de listagem
            return HttpResponseRedirect(request.path.replace('?action=print_batch', ''))

        return super().changelist_view(request, extra_context)

admin.site.register(Donation, DonationAdmin)
admin.site.register(Report, ReportsAdminView)
