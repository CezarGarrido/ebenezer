# app/management/commands/import_donor.py
import csv
from django.core.management.base import BaseCommand
from core.models.donor import Donor
from core.models.base import Address, Phone, Person, Individual, LegalEntity
from django.contrib.auth.models import User
from datetime import datetime
from core.models.company import Company

class Command(BaseCommand):
    help = "Importa dados do CSV exportado do DataFlex"

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        Donor.objects.all().delete()
        file_path = kwargs['file_path']
        with open(file_path, newline='', encoding='utf-8', errors='replace') as raw_file:
            cleaned_file = (line.replace('\x00', '') for line in raw_file)
            reader = csv.DictReader(cleaned_file, delimiter=',')
            created_count = 0

            for row in reader:
                
                if not row:  # pula registros inválidos
                    continue

                if not row['COD_DOA']:  # pula registros inválidos
                    continue

                if not row['NOM_A']:
                    continue
                
                # Parse dates
                id = int(row.get("COD_DOA"))
                # Verifica se o ID já existe
                if Person.objects.filter(id=id).exists():
                    self.stdout.write(f"ID {id} já existe. Pulando...")
                    continue

                birth_date = self.parse_date(row.get('DAT_CON'))  # ou outro campo de nascimento, se houver
                register_date = self.parse_date(row.get('DAT_CAD'))
                person_type =  "F" 
                if row.get('DES_CLP') == 'JURIDICA':
                    person_type = "J"
                    
                created_by=User.objects.first()
                if row['COD_FUN']:
                    created_by=User.objects.filter(id=int(row['COD_FUN'])).first()

                # Cria a base Person
                person = Person.objects.create(
                    id=id,
                )

                # Cria o Donor
                donor = Donor.objects.create(
                    person_ptr=person,
                    person_type=person_type,  # Pessoa Física
                    name=row['NOM_A'].strip().strip(),
                    owner=Company.objects.first(),  # ou passe como argumento o ID da empresa
                    created_at=register_date or datetime.now(),
                    created_by=created_by,  # ou use o usuário correto
                )
                
                if person_type == "F":
                    # Cria dados individuais
                    Individual.objects.create(
                        person=person,
                        cpf=row.get('CPF_DOA', '').strip(),
                        rg=row.get('R_G_DOA', '').strip(),
                        birth_date=birth_date
                    )
                else:
                    LegalEntity.objects.create(
                        person=person,
                        trade_name=row.get('NOM_B', '').strip(),
                        cnpj=row.get('CPF_DOA', '').strip(),
                    )

                # Cria endereço
                if any([row.get('END_DOA'), row.get('BAI_DOA'), row.get('CID_DOA')]):
                    Address.objects.create(
                        person=person,
                        address_type='RES',
                        street=row.get('END_DOA', '').strip(),
                        neighborhood=row.get('BAI_DOA', '').strip(),
                        postal_code=row.get('CEP_DOA', '').strip(),
                        city=row.get('CID_DOA', '').strip(),
                        state=row.get('EST_DOA', '').strip(),
                        is_primary=True
                    )

                # Cria telefone principal
                if row.get('TEL_DOA'):
                    Phone.objects.create(
                        person=person,
                        phone=self.clean_phone(row.get('TEL_DOA')),
                        type='F',
                        is_primary=True
                    )

                # Telefone adicional
                if row.get('OUT_TEL'):
                    Phone.objects.create(
                        person=person,
                        phone=self.clean_phone(row.get('OUT_TEL')),
                        type='M'  # Alternativo
                    )

                created_count += 1
                self.stdout.write(f'Processed: {id} {donor.name}')


            self.stdout.write(self.style.SUCCESS(f'{created_count} registros importados com sucesso.'))

    def parse_date(self, val):
        if not val or val.strip() == '':
            return None
        try:
            return datetime.strptime(val.strip(), '%d/%m/%Y').date()
        except ValueError:
            return None

    def parse_decimal(self, val):
        if not val or val.strip() == '':
            return None
        try:
            # Handle decimal values (replace comma with dot if needed)
            return float(val.strip().replace('.', '').replace(',', '.'))
        except ValueError:
            return None

    def clean_phone(self, phone):
        # Remove all non-digit characters
        return ''.join(filter(str.isdigit, phone))