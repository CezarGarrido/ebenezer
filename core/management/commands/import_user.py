import csv
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from pathlib import Path
import unicodedata
import re
from django.contrib.auth.models import Group
from django.db import IntegrityError

from core.models.company import UserProfile

def normalize_text(text: str) -> str:
    # Remove acentos
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ASCII', 'ignore').decode('ASCII')
    # Remove qualquer outro caractere que não seja letra, número, ponto ou underline
    text = re.sub(r'[^a-zA-Z0-9._]+', '', text)
    return text

def format_cpf(cpf: str) -> str:
    digits = ''.join(filter(str.isdigit, cpf))
    if len(digits) != 11:
        return cpf  # retorna como está se não tiver 11 dígitos
    return f"{digits[:3]}.{digits[3:6]}.{digits[6:9]}-{digits[9:]}"

class Command(BaseCommand):
    help = 'Importa usuários a partir de um arquivo CSV'

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str, help='Caminho para o arquivo CSV')

    def handle(self, *args, **options):
        csv_path = Path(options['csv_path'])

        if not csv_path.exists():
            self.stderr.write(self.style.ERROR(f"Arquivo não encontrado: {csv_path}"))
            return

        with csv_path.open(encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0

            for row in reader:
                id = int(row['COD_FUN'].strip())

                nome = row['NOM_FUN'].strip()
                cpf = row['CPF_FUN'].replace('.', '').replace('-', '').strip()
                senha = row.get('SEN_ACE', '123456') or '123456'

                if not cpf:
                    self.stderr.write(f"CPF vazio, ignorando: {nome}")
                    continue

                cpf_raw = row['CPF_FUN'].strip()
                cpf_digits = ''.join(filter(str.isdigit, cpf_raw))
                if len(cpf_digits) != 11:
                    self.stderr.write(f"CPF inválido, ignorando: {nome}")
                    continue

                username = format_cpf(cpf_digits)                
                email = f"{normalize_text(nome.lower().replace(' ', '.'))}@eben.com"

                if User.objects.filter(username=username).exists():
                    self.stdout.write(f"Usuário já existe: {username}")
                    continue

                user = User.objects.create_user(
                    id=id,
                    username=username,
                    email=email,
                    password=senha,
                    first_name=nome.split()[0],
                    last_name=' '.join(nome.split()[1:]) if len(nome.split()) > 1 else '',
                    is_staff=True,
                )

                # -----------------------------------------------------------------------------------
                # Lê o valor do campo 'DES_SET' do CSV
                setor = row.get('DES_SET', '').strip().upper()

                # Verifica se o setor contém a palavra 'ADMINISTRATIVO'
                if 'ADMINISTRATIVO' in setor:
                    grupo_nome = 'ADMINISTRATIVO'
                # Se não, verifica se é 'TELEMARKETING'
                elif 'TELEMARKETING' in setor:
                    grupo_nome = 'TELEMARKETING'
                # Caso não seja nenhum dos dois, não atribui grupo
                else:
                    grupo_nome = None

                # Se foi identificado um grupo válido ('ADMINISTRATIVO' ou 'TELEMARKETING')
                if grupo_nome:
                    try:
                        # Busca no banco o grupo pelo nome
                        grupo = Group.objects.get(name=grupo_nome)

                        # Adiciona o usuário recém-criado ao grupo
                        user.groups.add(grupo)

                        # Informa no terminal que o vínculo foi feito com sucesso
                        self.stdout.write(self.style.SUCCESS(f"Usuário {username} adicionado ao grupo {grupo_nome}"))

                    except Group.DoesNotExist:
                        # Caso o grupo não exista, avisa no terminal
                        self.stderr.write(self.style.ERROR(f"Grupo {grupo_nome} não encontrado para {username}"))
                else:
                    # Caso o setor não tenha correspondência com nenhum grupo, emite um aviso
                    self.stderr.write(self.style.WARNING(f"Grupo indefinido para {username}, DES_SET: '{setor}'"))

                count += 1
                self.stdout.write(self.style.SUCCESS(f"Usuário criado: {username} {senha}"))

            self.stdout.write(self.style.SUCCESS(f"Total de usuários criados: {count}"))
