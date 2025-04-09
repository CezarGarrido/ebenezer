from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models.company import Company, UserProfile

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
