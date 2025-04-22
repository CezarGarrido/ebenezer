from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models.company import Company, UserProfile
#----------------------------------------------------
from django.contrib.auth.models import Group, Permission    # permissões e grupos
from core.models.donor import Donor     # modelos que vão ter permissões específicas
from donation.models import Donation
from django.contrib.contenttypes.models import ContentType  # filtrar permissões por modelo

class Command(BaseCommand):
    help = 'Criar empresa e usuário iniciais'

    def handle(self, *args, **options):
        User = get_user_model()

        # Verifica se o usuário já existe
        user, created = User.objects.get_or_create(
            email='admin@admin.com',
            defaults={'username': 'admin@admin.com', 'is_superuser': True, 'is_staff': True}
        )
        if created:
            user.set_password('admin')
            user.save()
            self.stdout.write(self.style.SUCCESS('Usuário admin criado.'))
        else:
            self.stdout.write('Usuário admin já existe.')

        # Cria empresa, se não existir
        company, created = Company.objects.get_or_create(
            name='Ebenezer',
            defaults={
                'person_type': 'J',
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Empresa criada.'))
        else:
            self.stdout.write('Empresa já existe.')

        # Cria perfil do usuário com a empresa
        UserProfile.objects.get_or_create(user=user, company=company)

        #-------------------------------------------------------------------------------
        # cria (se não existir) o grupo ADMINISTRATIVO
        admin_group, admin_created = Group.objects.get_or_create(name='ADMINISTRATIVO') 

        # cria (se não existir) o grupo TELEMARKETING
        tele_group, tele_created = Group.objects.get_or_create(name='TELEMARKETING')

        if admin_created:
            # Só define todas as permissões se o grupo foi criado agora
            admin_permissions = Permission.objects.all()
            admin_group.permissions.set(admin_permissions)
            self.stdout.write(self.style.SUCCESS(f'Permissões atribuídas ao grupo {admin_group.name}.'))
        else:
            self.stdout.write(f'Grupo {admin_group.name} já existia, permissões não foram alteradas.')

        if tele_created:
            # Pega todas as permissões de Donor
            donor_ct = ContentType.objects.get_for_model(Donor)
            donor_permissions = Permission.objects.filter(content_type=donor_ct)

            # Pega todas as permissões de Donation
            donation_ct = ContentType.objects.get_for_model(Donation)
            donation_permissions = Permission.objects.filter(content_type=donation_ct)

            # Junta as permissões
            tele_permissions = list(donor_permissions) + list(donation_permissions)

            # Aplica ao grupo TELEMARKETING
            tele_group.permissions.set(tele_permissions)
            self.stdout.write(self.style.SUCCESS(f'Permissões atribuídas ao grupo {tele_group.name}.'))
        else:
            self.stdout.write(f'Grupo {tele_group.name} já existia, permissões não foram alteradas.')
