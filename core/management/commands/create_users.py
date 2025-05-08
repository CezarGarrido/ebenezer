from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group

class Command(BaseCommand):
    help = 'Adicionar usuários aos grupos TELEMARKETING e ADMINISTRATIVO'

    def handle(self, *args, **options):
        # Verifica se o grupo TELEMARKETING existe
        group_telemarketing = Group.objects.get(name='TELEMARKETING')
        if not group_telemarketing:
            self.stdout.write(self.style.ERROR('Grupo TELEMARKETING não encontrado.'))
            return

        # Verifica se o grupo ADMINISTRATIVO existe
        group_administrativo = Group.objects.get(name='ADMINISTRATIVO')
        if not group_administrativo:
            self.stdout.write(self.style.ERROR('Grupo ADMINISTRATIVO não encontrado.'))
            return

        # Cria o usuário Telemarketing, se não existir
        user_tele, created = User.objects.get_or_create(
            email='telemarketing@empresa.com',
            defaults={'username': 'telemarketing@empresa.com'}
        )

        if created:
            user_tele.set_password('teleM123')
            user_tele.save()
            user_tele.groups.add(group_telemarketing)  # Adiciona ao grupo TELEMARKETING
            self.stdout.write(self.style.SUCCESS('Usuário TELEMARKETING criado e atribuído ao grupo.'))
        else:
            user_tele.groups.add(group_telemarketing)
            self.stdout.write('Usuário TELEMARKETING já existe, mas foi atribuído ao grupo.')

        # Cria o usuário Administrativo, se não existir
        user_admin, created = User.objects.get_or_create(
            email='admin@empresa.com',
            defaults={'username': 'admin@empresa.com'}
        )

        if created:
            user_admin.set_password('adminA123')
            user_admin.save()
            user_admin.groups.add(group_administrativo)  # Adiciona ao grupo ADMINISTRATIVO
            self.stdout.write(self.style.SUCCESS('Usuário ADMINISTRATIVO criado e atribuído ao grupo.'))
        else:
            user_admin.groups.add(group_administrativo)
            self.stdout.write('Usuário ADMINISTRATIVO já existe, mas foi atribuído ao grupo.')
