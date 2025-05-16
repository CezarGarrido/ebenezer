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
from .models import ThankYouMessage, ThankYouMessageLine
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
        js = ("js/vendor/jquery.mask.min.js", "js/mask/money.js", "js/payment.js")  # Adicionamos um script personalizado
        
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
    
class DonationAdmin(GenderedMessageMixin, admin.ModelAdmin):
    form = DonationForm
    list_display = ("id", "paid_status", "expected_at", "donor", "format_amount", "format_paid_amount", "paid_at", "created_by", "created_at", "updated_at")  # Campos visíveis na listagem
    verbose_name = "Doação"
    verbose_name_plural = "Doações"
    entity_labels = {
        'singular': 'Doação',
        'plural': 'Doações',
        'gender': 'feminine',
    }
        # Filtros para facilitar a navegação
    list_filter = (
        "paid",             # Se foi paga ou não
        "method",           # Método de pagamento
        "created_by",       # Usuário que criou
    )

    # Campos pesquisáveis
    search_fields = (
        "id",
        "donor__name",     # Nome do doador
        "notes",           # Notas da doação
    )
    
    
    autocomplete_fields = ['donor']
    
    exclude = ['owner', 'created_by']

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
    
    def format_paid_amount(self, obj):
        if obj.paid_amount:
            return locale.currency(obj.paid_amount, grouping=True)
        return "-"
    
    def paid_status(self, obj):
        if obj.paid:
            return format_html('<span class="badge badge-success" title="Doação paga">Pago</span>')

        # Verifica se está vencida (expected_at no passado)
        if obj.expected_at and obj.expected_at < datetime.datetime.now().date():
            return format_html('<span class="badge badge-warning" title="Doação vencida e não paga">Atrasado</span>')

        # Ainda dentro do prazo
        return format_html('<span class="badge badge-danger" title="Ainda no prazo de pagamento">Pendente</span>')

    paid_status.short_description = "Situação"
    format_amount.short_description = "Valor Esperado"
    format_paid_amount.short_description = "Valor Recebido"

    def response_change(self, request, obj):
        if '_download_receipt_pdf' in request.POST:
            # Obter configurações com validação
            try:
                settings = DonationSettings.get_solo()
                if not settings:
                    messages.error(request, "Configurações do sistema não encontradas.")
                    logger.error("Configurações de doação não encontradas no banco de dados")
                    return HttpResponseRedirect(request.get_full_path())
            except Exception as e:
                messages.error(request, "Erro ao acessar configurações do sistema.")
                logger.error(f"Erro ao acessar DonationSettings: {str(e)}", exc_info=True)
                return HttpResponseRedirect(request.get_full_path())
                
            content_pdf = obj.get_receipt_pdf(settings)  # deve retornar o conteúdo binário do PDF

            response = HttpResponse(content_pdf, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename=recibo_de_doacao_{obj.pk}.pdf'
            return response

        if '_print_receipt' in request.POST:
            try:
                logger.info(f"Iniciando processo de impressão de recibo para doação ID: {obj.id}")
                
                # Validação básica do objeto
                if not obj or not obj.pk:
                    messages.error(request, "Doação inválida ou não encontrada.")
                    logger.error(f"Objeto de doação inválido: {obj}")
                    return HttpResponseRedirect(request.get_full_path())
                
                # Obter configurações com validação
                try:
                    settings = DonationSettings.get_solo()
                    if not settings:
                        messages.error(request, "Configurações do sistema não encontradas.")
                        logger.error("Configurações de doação não encontradas no banco de dados")
                        return HttpResponseRedirect(request.get_full_path())
                except Exception as e:
                    messages.error(request, "Erro ao acessar configurações do sistema.")
                    logger.error(f"Erro ao acessar DonationSettings: {str(e)}", exc_info=True)
                    return HttpResponseRedirect(request.get_full_path())
                
                # Validação da impressora
                printer_name = settings.default_printer
                if not printer_name or not printer_name.strip():
                    messages.error(request, "Nenhuma impressora padrão configurada.")
                    logger.error("Nenhuma impressora configurada nas settings")
                    return HttpResponseRedirect(request.get_full_path())
                
                # Tentativa de impressão
                try:
                    logger.info(f"Enviando recibo para impressora: {printer_name}")
                    obj.print_receipt(settings)
                    messages.success(request, f"Recibo enviado com sucesso para a impressora: {printer_name}")
                    logger.info(f"Recibo impresso com sucesso para doação ID: {obj.id}")
                except Exception as e:
                    messages.error(request, "Erro inesperado ao imprimir recibo.")
                    logger.error(f"Erro inesperado ao imprimir recibo: {str(e)}", exc_info=True)
                
            except Exception as e:
                messages.error(request, "Ocorreu um erro durante o processo de impressão.")
                logger.critical(f"Erro crítico no processamento de recibo: {str(e)}", exc_info=True)
            
            return HttpResponseRedirect(request.get_full_path())

        return super().response_change(request, obj)

admin.site.register(Donation, DonationAdmin)
admin.site.register(Report, ReportsAdminView)
