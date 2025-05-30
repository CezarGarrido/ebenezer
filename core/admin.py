from datetime import datetime
from django import forms
from django.contrib import admin
from donation.models import Donation
from .models.company import Company, UserProfile, GroupCompany
from .models.employee import Employee, EmployeeUser
from .models.donor import Donor
from .models.base import Individual, LegalEntity, Address, Email, Phone
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.db.models import Sum, Count
import locale
from django.db.models import Q

class CustomAdminSite(admin.AdminSite):
    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        
        now = datetime.now()
        current_month = now.month
        current_year = now.year
        total_donations = Donation.objects.filter(paid=True).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
        monthly_donations = Donation.objects.filter(paid=True, created_at__month=current_month, created_at__year=current_year).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
                # Últimas doações pagas
        latest_donations = Donation.objects.filter(paid=True).order_by('-created_at')[:5]

        # Pagamentos em atraso: não pagos e vencidos
        overdue_donations = Donation.objects.filter(
            Q(paid=False), Q(expected_at__lt=now.date())
        ).order_by('expected_at')[:5]

        stats = {
            'total_donations': locale.currency(total_donations, grouping=True),
            'donation_count': Donation.objects.count(),
            'donor_count': Donor.objects.count(),
            'monthly_donations': locale.currency(monthly_donations, grouping=True),
            'latest_donations': latest_donations,
            'overdue_donations': overdue_donations,
            'today': now.date(),
        }
        
        extra_context.update(stats)

        return super().index(request, extra_context)

# Substitui o site padrão
admin.site.__class__ = CustomAdminSite

class PhoneForm(forms.ModelForm):
    class Meta:
        model = Phone
        fields = "__all__"
        
        widgets = {
            'phone': forms.TextInput(attrs={'data-mask-phone': ""}),
        }
        
    class Media:
        js = ("js/vendor/jquery.mask.min.js", "js/mask/phone.js",)  # Adicionamos um script personalizado

class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = "__all__"
        
        widgets = {
            'email': forms.TextInput(attrs={'data-mask-email': "", "placeholder":"exemplo@dominio.com"}),
        }
        
    class Media:
        js = ("js/vendor/jquery.mask.min.js", "js/mask/email.js",)  # Adicionamos um script personalizado


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = "__all__"
        
        widgets = {
            'postal_code': forms.TextInput(attrs={'data-mask-cep': "00000-000",  "id": "id_cep"}),
        }
        
    class Media:
        js = ("js/vendor/jquery.mask.min.js", "js/mask/cep.js")  # Adicionamos um script personalizado

class IndividualForm(forms.ModelForm):
    class Meta:
        model = Individual
        fields = "__all__"
        
        widgets = {
            'cpf': forms.TextInput(attrs={'data-mask-cpf': ""}),
        }
        
    class Media:
        js = ("js/vendor/jquery.mask.min.js", "js/mask/cpf.js",)  # Adicionamos um script personalizado

class LegalEntityForm(forms.ModelForm):
    class Meta:
        model = LegalEntity
        fields = "__all__"
        
        widgets = {
            'cnpj': forms.TextInput(attrs={'data-mask-cnpj': ""}),
        }
        
    class Media:
        js = ("js/vendor/jquery.mask.min.js", "js/mask/cnpj.js",)  # Adicionamos um script personalizado


class IndividualInline(admin.StackedInline):
    model = Individual
    form = IndividualForm
    can_delete = False
    max_num = 1
    verbose_name = "Pessoa Física"
    verbose_name_plural = "Dados de Pessoa Física"
    classes = ["individual-inline-tab"]
    ordering_field = ("cpf",)
    
class LegalEntityInline(admin.StackedInline):
    model = LegalEntity
    form = LegalEntityForm
    can_delete = False
    max_num = 1
    verbose_name = "Pessoa Jurídica"
    verbose_name_plural = "Dados de Pessoa Jurídica"
    classes = ["legal-inline-tab"]
    ordering_field = ("cnpj",)


class AddressInline(admin.StackedInline):
    model = Address
    form = AddressForm
    extra = 1
    verbose_name = "Endereço"
    verbose_name_plural = "Endereços"
    ordering_field = ("postal_code",)
    
    
    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        # Ordernar para que o cep apareça no topo do formulario
        fields = ['postal_code'] + [field for field in fields if field != 'postal_code']
        return fields
    
class EmailInline(admin.TabularInline):
    model = Email
    form = EmailForm
    extra = 1
    verbose_name = "Email"
    verbose_name_plural = "Emails"
    ordering_field = ("email",)

class PhoneInline(admin.TabularInline):
    form = PhoneForm
    model = Phone
    extra = 1
    verbose_name = "Telefone"
    verbose_name_plural = "Telefones"
    ordering_field = ("phone",)

class EmployeeUserInline(admin.TabularInline):
    model = EmployeeUser
    extra = 1
    verbose_name = "Usuário"
    verbose_name_plural = "Usuários Vinculados"
    
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == "user" and not request.user.is_superuser:
            company = request.user.profile.company
            # Só usuários da empresa e que ainda não estão vinculados
            kwargs["queryset"] = User.objects.filter(profile__company=company).exclude(
                id__in=EmployeeUser.objects.values_list("user_id", flat=True)
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
class BasePersonAdmin(admin.ModelAdmin):
    inlines = [IndividualInline, LegalEntityInline, AddressInline, EmailInline, PhoneInline]
    list_per_page = 10  # valor fixo
    list_display = ("id", "name", "created_by", "created_at", "updated_at")
    search_fields = ("name", "id")  # Depende dos campos de identificação disponíveis
    list_filter = ("created_at",)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ("-created_at",)
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)

        if fieldsets:
            first_label, first_fields = fieldsets[0]
            if first_label in (None, '', 'General'):
                # Substitui o título do primeiro fieldset
                fieldsets = (("Geral", first_fields),) + tuple(fieldsets[1:])

        return fieldsets
    
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = "__all__"
        
        widgets = {
            'salary': forms.TextInput(attrs={'data-mask-money': ""}),
        }
        
    class Media:
        js = ("js/vendor/jquery.mask.min.js", "js/mask/money.js",)  # Adicionamos um script personalizado

@admin.register(Employee)
class EmployeeAdmin(BasePersonAdmin):
    form = EmployeeForm
    list_display = ("id", "name", "position", "created_by", "created_at", "updated_at")
    search_fields = ("name", "position")
    exclude = ("owner", "person_type", "created_by")
    inlines = [IndividualInline, AddressInline, EmailInline, PhoneInline, EmployeeUserInline]

    def save_model(self, request, obj, form, change):
        if not obj.created_by:  # Define apenas se for um novo objeto
            obj.created_by = request.user
            obj.owner = request.user.profile.company
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user.profile.company)

@admin.register(Donor)
class DonorAdmin(BasePersonAdmin):
    search_fields = ("name",)
    list_display = ("id", "name", "person_type_badge", "created_by", "created_at", "updated_at")

    exclude = ("owner", "created_by")
    list_filter = ("created_at", "person_type")

    class Media:
        js = ('js/inline.js',)  # Carrega o script no Django Admin

    def person_type_badge(self, obj):
        if obj.person_type == "F":
            return format_html('<span class="badge badge-primary">Pessoa Física</span>')
        elif obj.person_type == "J":
            return format_html('<span class="badge badge-success">Pessoa Jurídica</span>')
        return format_html('<span class="badge badge-secondary">Desconhecido</span>')
    person_type_badge.short_description = 'Tipo de Pessoa'
    
    def save_model(self, request, obj, form, change):
        if not obj.created_by:  # Define apenas se for um novo objeto
            obj.created_by = request.user
            obj.owner = request.user.profile.company
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user.profile.company)
    
@admin.register(Company)
class CompanyAdmin(BasePersonAdmin):
    inlines = [LegalEntityInline, AddressInline, EmailInline, PhoneInline]
    list_display = ('image_tag', "name", "created_at", "updated_at")
    search_fields = []
    list_filter = []
    exclude = ("person_type", "created_by")
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def save_model(self, request, obj, form, change):
        if not obj.created_by:  # Define apenas se for um novo objeto
            obj.created_by = request.user
            obj.person_type = 'J'
        super().save_model(request, obj, form, change)
        
    def get_queryset(self, request):
        """ Filtra usuários da mesma empresa do admin logado. """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Superusuário vê as empresas
        return qs.filter(id=request.user.profile.company.id)

    def image_tag(self, obj):
        if obj.logo_file:
            return format_html('<img class="img-circle" src="{}" width="40" height="40"/>', obj.logo_file.url)
        return "-"

    image_tag.short_description = 'Logo'
    image_tag.allow_tags = True
    
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name = "Instituição"
    verbose_name_plural = "Instituição"

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    
    def get_queryset(self, request):
        """ Filtra usuários da mesma empresa do admin logado. """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Superusuário vê todos os usuários
        return qs.filter(profile__company=request.user.profile.company)

    def save_model(self, request, obj, form, change):
        """ Garante que um novo usuário seja vinculado à empresa do admin logado """
        obj.save()
           
        if not hasattr(obj, 'profile'):
            UserProfile.objects.create(user=obj, company=request.user.profile.company)
            
    #-------------------------------------------------------------------------------------
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """ Personaliza a exibição dos nomes dos grupos """
        field = super().formfield_for_manytomany(db_field, request, **kwargs)
        if db_field.name == 'groups':
            # Exibe o nome do grupo somente com a primeira letra maiúscula
            field.label_from_instance = lambda obj: obj.name.capitalize()
        return field

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

class GroupCompanyInline(admin.StackedInline):
    model = GroupCompany
    can_delete = False
    verbose_name = "Instituição"
    verbose_name_plural = "Instituição"
    
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == "company" and not request.user.is_superuser:
            kwargs["queryset"] = Company.objects.filter(id=request.user.profile.company.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
class CustomGroupAdmin(admin.ModelAdmin):
    inlines = (GroupCompanyInline,)
    filter_horizontal = ('permissions',)
    
    def get_queryset(self, request):
        """ Filtra grupos da mesma empresa do admin logado. """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(group_company__company=request.user.profile.company)

    def save_model(self, request, obj, form, change):
        """ Garante que um novo grupo seja vinculado à empresa do admin logado """
        obj.save()
        if not hasattr(obj, 'group_company'):
            GroupCompany.objects.create(user=obj, company=request.user.profile.company)
            
    #--------------------------------------------------------------------------------------------
    # Exibir o nome com apenas a primeira letra maiúscula
    def capitalized_name(self, obj):
        return obj.name.capitalize()
    
    # Adicionando ao list_display a função capitalized_name
    list_display = ('capitalized_name',)
    
    capitalized_name.short_description = "Nome"



admin.site.unregister(Group)
admin.site.register(Group, CustomGroupAdmin)