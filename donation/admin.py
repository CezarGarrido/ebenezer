
from django.contrib import messages
from django.contrib import admin
from django import forms
from django.urls import reverse
from .models import Donation
from django.contrib.admin.utils import quote
from django.utils.html import format_html

from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib import messages

from django.template.loader import render_to_string

from django.contrib import messages
from django.utils.html import format_html

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
        print(lowered)
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
    list_display = ("donor", "amount", "paid", "received_at", "created_by", "created_at")  # Campos visíveis na listagem
    exclude = ("owner", "created_by")
    verbose_name = "Doação"
    verbose_name_plural = "Doações"
    entity_labels = {
        'singular': 'Doação',
        'plural': 'Doações',
        'gender': 'feminine',
    }
    #autocomplete_fields = ['donor']
    def save_model(self, request, obj, form, change):
        if not obj.created_by:  # Define apenas se for um novo objeto
            obj.created_by = request.user
            obj.owner = request.user.profile.company
        super().save_model(request, obj, form, change)
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        donation = self.model.objects.get(pk=object_id)
        extra_context['receipt_html'] = render_to_string("admin/donation/receipt_block.html", {"donation": donation})
        return super().change_view(request, object_id, form_url, extra_context)

# Register your models here.
admin.site.register(Donation, DonationAdmin)