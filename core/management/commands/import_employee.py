# app/management/commands/import_employee.py
import csv
from django.core.management.base import BaseCommand
from core.models.employee import Employee
from core.models.base import Address, Phone, Person, Individual
from django.contrib.auth.models import User
from datetime import datetime
from core.models.company import Company

class Command(BaseCommand):
    help = "Importa dados do CSV exportado do DataFlex"

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        with open(file_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=',')
            created_count = 0

            for row in reader:
                print(row)
                if not row['COD_FUN']:  # skip se registro inválido
                    continue

                # Parse dates
                birth_date = self.parse_date(row.get('NAS_FUN'))
                hire_date = self.parse_date(row.get('DAT_ADM'))
                termination_date = self.parse_date(row.get('DAT_DEM'))

                # First create the base Person
                person = Person.objects.create(
                    person_type='F',  # Pessoa Física
                    name=row['NOM_FUN'].strip(),
                    created_by=User.objects.first(),  # or set a specific user
                    created_at= datetime.now(),
                )

                # Then create the Employee
                employee = Employee.objects.create(
                    person_ptr=person,
                    name=row['NOM_FUN'].strip(),
                    owner=Company.objects.first(),  # You need to set the company
                    date_of_birth=birth_date,
                    hire_date=hire_date,
                    termination_date=termination_date,
                    ctps=row.get('CTPS', '').strip(),
                    position=row.get('DES_SET', '').strip(),
                    department=row.get('COD_SET', '').strip(),
                    salary=self.parse_decimal(row.get('SAL_FUN')),
                    created_at= datetime.now(),
                )

                # Create Individual data
                Individual.objects.create(
                    person=person,
                    cpf=row.get('CPF_FUN', '').strip(),
                    rg=row.get('RG_FUN', '').strip(),
                    birth_date=birth_date
                )

                # Create Address
                if any([row.get('END_FUN'), row.get('BAI_FUN'), row.get('CID_FUN')]):
                    Address.objects.create(
                        person=person,
                        address_type='RES',
                        street=row.get('END_FUN', '').strip(),
                        neighborhood=row.get('BAI_FUN', '').strip(),
                        postal_code=row.get('CEP_FUN', '').strip(),
                        city=row.get('CID_FUN', '').strip(),
                        state=row.get('EST_FUN', '').strip(),
                        is_primary=True
                    )

                # Create Phone if exists
                if row.get('TEL_RES'):
                    Phone.objects.create(
                        person=person,
                        phone=self.clean_phone(row.get('TEL_RES')),
                        type='F',  # Fixo
                        is_primary=True
                    )

                created_count += 1
                self.stdout.write(f'Processed: {employee.name}')

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