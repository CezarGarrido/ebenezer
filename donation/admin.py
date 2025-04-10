
from django.contrib import messages
from django.contrib import admin
from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Donation
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django import forms

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
        }

        
    class Media:
        js = ("js/vendor/jquery.mask.min.js", "js/mask/money.js",)  # Adicionamos um script personalizado

class DonationAdmin(GenderedMessageMixin, admin.ModelAdmin):
    form=DonationForm
    exclude = ('created_by', 'company')  # Esconde o campo no formulário
    list_display = ("id", "donor", "amount", "paid", "paid_at", "created_by", "created_at", "updated_at")  # Campos visíveis na listagem
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
    #autocomplete_fields = ['donor']
    def save_model(self, request, obj, form, change):
        if not obj.created_by:  # Define apenas se for um novo objeto
            obj.created_by = request.user
            obj.owner = request.user.profile.company
        super().save_model(request, obj, form, change)
    fieldsets = (
        ("Informações da Doação", {
            "fields": ("donor", "amount", "expected_at", "notes")
        }),
        ("Informações de Pagamento", {
            "fields": ("paid", "paid_at", "method"),
            "classes": ("collapse",)  # ou remova isso para deixar sempre visível
        }),
    )
    readonly_fields = ("created_at", "updated_at")

    def response_change(self, request, obj):
        if '_print_receipt' in request.POST:
            # Lógica personalizada aqui
            print("gerando....")
            
            messages.success(request, "Recibo gerado com sucesso.")
            
            # Redireciona de volta para a mesma página (edição do objeto)
            url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[obj.pk])
            return HttpResponseRedirect(url)

        return super().response_change(request, obj)
    
# Register your models here.
admin.site.register(Donation, DonationAdmin)


class DonationReportForm(forms.Form):
    start_date = forms.DateField(label="Data inicial", required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label="Data final", required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    created_by = forms.ModelChoiceField(
        label="Usuário",
        required=False,
        queryset=User.objects.none(),  # Inicialmente vazio
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if self.request:
            user = self.request.user
            if user.is_superuser:
                self.fields['created_by'].queryset = User.objects.all()
            else:
                self.fields['created_by'].queryset = User.objects.filter(profile__company=user.profile.company)


class ReportsAdminView(admin.ModelAdmin):
    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.has_perm('donation.view_report')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
                # Verifica a permissão antes de continuar
        if not self.has_view_permission(request):
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied

        form = DonationReportForm(request.GET or None, request=request)
        donations = Donation.objects.all()

        user = request.user
        if not user.is_superuser:
            donations = donations.filter(owner=user.profile.company)

        if form.is_valid():
            start = form.cleaned_data.get('start_date')
            end = form.cleaned_data.get('end_date')
            created_by = form.cleaned_data.get('created_by')

            if start:
                donations = donations.filter(paid_at__date__gte=start)
            if end:
                donations = donations.filter(paid_at__date__lte=end)
            if created_by:
                donations = donations.filter(created_by=created_by)

        # PAGINAÇÃO
        paginator = Paginator(donations, 20)  # 20 por página
        page_number = request.GET.get('page')
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        context = dict(
            self.admin_site.each_context(request),
            title="Relatórios de Doações",
            donations=page_obj,
            form=form,
            paginator=paginator,
            page_obj=page_obj,
            is_paginated=page_obj.has_other_pages(),
        )
        return TemplateResponse(request, "admin/donation/reports.html", context)


class Report(models.Model):
    class Meta:
        verbose_name = "Relatório"
        verbose_name_plural = "Relatórios"
        app_label = "donation"  # para agrupar no mesmo menu se quiser
        managed = False  # não cria tabela no banco

admin.site.register(Report, ReportsAdminView)
