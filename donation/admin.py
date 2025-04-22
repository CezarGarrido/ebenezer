import locale
from django.contrib import messages
from django.contrib import admin
from django import forms
from core.models.donor import Donor
from core.models.employee import Employee
from donation.views import Report, ReportsAdminView
from .models import Donation
from django.utils.html import format_html
from django.http import HttpResponseRedirect
from django import forms
from .models import ThankYouMessage, ThankYouMessageLine
import platform

# Só importa win32print se for Windows
if platform.system() == "Windows":
    import win32print
            
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
            'expected_at': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'paid_at': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }

    class Media:
        js = ("js/vendor/jquery.mask.min.js", "js/mask/money.js",)  # Adicionamos um script personalizado

class DonationAdmin(GenderedMessageMixin, admin.ModelAdmin):
    form = DonationForm
    exclude = ('created_by', 'company')  # Esconde o campo no formulário
    list_display = ("id", "donor", "format_amount", "paid", "format_paid_amount", "paid_at", "created_by", "created_at", "updated_at")  # Campos visíveis na listagem
    exclude = ("owner", "created_by")
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

    def save_model(self, request, obj, form, change):
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

        ("Recibo", {
            "fields": ("thank_you_message", "get_receipt", ),
            "classes": ("collapse",)  # ou remova isso para deixar sempre visível
        }),
    )
    
    readonly_fields = ("created_by", "created_at", "updated_at", "get_receipt")

        
    def get_receipt(self, obj):
        from django.utils.safestring import mark_safe
        return mark_safe(f'''
            <hr/>
            <div class="receipt">
                {obj.receipt_html()}
            </div>
            <hr/>
            <div class="form-group">
                <input type="button" class="btn btn-outline-success form-control" value="Imprimir no Navegador" onclick="window.print()" name="_print_browser" />
            </div>
            
            <div class="form-group">
                <input type="submit" class="btn btn-outline-warning form-control" value="Imprimir na Impressora" name="_print_receipt" />
            </div>
            
            <div class="help-block">
                * Recibo gerado com os dados da última edição salva.
            </div>
        ''')
    
    get_receipt.short_description = ""
    
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
    
    format_amount.short_description = "Valor Esperado"
    format_paid_amount.short_description = "Valor Recebido"

    def response_change(self, request, obj):
        if '_print_receipt' in request.POST:
            # Lógica personalizada aqui
            print("gerando....")
            if platform.system() == "Windows":
                self.print_with_win32(obj.receipt())
                messages.success(request, "Recibo gerado com sucesso.")
            else:
                messages.warning(request, "Disponível apenas para Windows")

            return HttpResponseRedirect(request.get_full_path())

        return super().response_change(request, obj)
    
        
    def get_printers(self):
        if platform.system() == "Windows":
            return [p[2] for p in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)]
        else:
            return []
        
    def print_with_win32(self, text, printer="EPSON LX-350"):
        printers = self.get_printers()
        
        bytes_text = text.encode("latin1", errors="replace")

        if printer in printers:
            printer_name = printer
            print(f"Usando impressora preferida: {printer_name}")
        else:
            printer_name = win32print.GetDefaultPrinter()
            print(f"A impressora '{printer}' não foi encontrada. Usando padrão: {printer_name}")

        try:
            hPrinter = win32print.OpenPrinter(printer_name)
            hJob = win32print.StartDocPrinter(hPrinter, 1, ("Recibo de Doação", None, "RAW"))
            win32print.StartPagePrinter(hPrinter)
            win32print.WritePrinter(hPrinter, bytes_text)
            win32print.EndPagePrinter(hPrinter)
            win32print.EndDocPrinter(hPrinter)
            print(f"Recibo impresso com sucesso na '{printer_name}'.")
        except Exception as e:
            print("Erro ao imprimir:", e)
        finally:
            try:
                win32print.ClosePrinter(hPrinter)
            except:
                print("Erro ao fechar impressora:", e)
            
admin.site.register(Donation, DonationAdmin)
admin.site.register(Report, ReportsAdminView)
