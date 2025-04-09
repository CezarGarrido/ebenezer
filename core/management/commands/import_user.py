import csv
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from pathlib import Path
import unicodedata
import re

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

                count += 1
                self.stdout.write(self.style.SUCCESS(f"Usuário criado: {username} {senha}"))

            self.stdout.write(self.style.SUCCESS(f"Total de usuários criados: {count}"))
