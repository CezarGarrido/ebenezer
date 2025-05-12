from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models.base import Address, Email, Individual, LegalEntity, Person, Phone
from core.models.company import Company, UserProfile, GroupCompany
from django.contrib.auth.models import Group, Permission
from core.models.donor import Donor
from donation.models import Donation, DonationSettings, ThankYouMessage, ThankYouMessageLine
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError

from donation.views import Report

class Command(BaseCommand):
    help = 'Criar empresa e usuário iniciais'

    def handle(self, *args, **options):
        User = get_user_model()

        # Criação do usuário admin
        try:
            user, created = User.objects.get_or_create(
                email='admin@admin.com',
                defaults={'username': 'admin@admin.com', 'is_superuser': True, 'is_staff': True}
            )
        except IntegrityError:
            user = User.objects.get(email='admin@admin.com')
            created = False

        if created:
            user.set_password('admin')
            user.save()
            self.stdout.write(self.style.SUCCESS('Usuário admin criado.'))
        else:
            self.stdout.write('Usuário admin já existe.')

        # Criação da empresa
        try:
            company, created = Company.objects.get_or_create(
                name='Ebenezer',
                defaults={'person_type': 'J'}
            )
        except IntegrityError:
            company = Company.objects.get(name='Ebenezer')
            created = False

        if created:
            self.stdout.write(self.style.SUCCESS('Empresa criada.'))
        else:
            self.stdout.write('Empresa já existe.')

        # Criação do perfil do usuário
        try:
            UserProfile.objects.get_or_create(user=user, company=company)
        except IntegrityError:
            pass  # Já existe

        # Criação do grupo ADMINISTRATIVO
        try:
            admin_group, admin_created = Group.objects.get_or_create(name='ADMINISTRATIVO')
        except IntegrityError:
            admin_group = Group.objects.get(name='ADMINISTRATIVO')
            admin_created = False

        try:
            GroupCompany.objects.get_or_create(group=admin_group, company=company)
        except IntegrityError:
            pass

        # Criação do grupo TELEMARKETING
        try:
            tele_group, tele_created = Group.objects.get_or_create(name='TELEMARKETING')
        except IntegrityError:
            tele_group = Group.objects.get(name='TELEMARKETING')
            tele_created = False

        try:
            GroupCompany.objects.get_or_create(group=tele_group, company=company)
        except IntegrityError:
            pass

        # Atribuição de permissões ao grupo ADMINISTRATIVO
        if admin_created:
            admin_permissions = Permission.objects.all()
            admin_group.permissions.set(admin_permissions)
            self.stdout.write(self.style.SUCCESS(f'Permissões atribuídas ao grupo {admin_group.name}.'))
        else:
            self.stdout.write(f'Grupo {admin_group.name} já existia, permissões não foram alteradas.')

        # Atribuição de permissões ao grupo TELEMARKETING
        if tele_created:
            # Modelos cujas permissões devem ser atribuídas
            all_models = [
                Individual, LegalEntity, Address, Email, Phone,
                Donor, Donation, Report, ThankYouMessage, ThankYouMessageLine, DonationSettings
            ]

            # Coleta todas as permissões padrão dos modelos
            all_permissions = []
            for model in all_models:
                ct = ContentType.objects.get_for_model(model)
                perms = Permission.objects.filter(content_type=ct)
                all_permissions.extend(perms)

            # Atribui ao grupo
            tele_group.permissions.set(all_permissions)
            
            self.stdout.write(self.style.SUCCESS(f'Permissões atribuídas ao grupo {tele_group.name}.'))
        else:
            self.stdout.write(f'Grupo {tele_group.name} já existia, permissões não foram alteradas.')
