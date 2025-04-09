import csv
from pathlib import Path
from datetime import datetime
from decimal import Decimal
from django.core.management.base import BaseCommand
from donation.models import Donation
from core.models.donor import Donor
from django.contrib.auth.models import User
from core.models.company import Company

class Command(BaseCommand):
    help = "Importa doações de um CSV"

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str, help='Caminho para o arquivo CSV')

    def handle(self, *args, **options):
        path = Path(options['csv_path'])
        company = Company.objects.first()
        user = User.objects.first()

        if not path.exists():
            self.stderr.write(f"Arquivo não encontrado: {path}")
            return

        with path.open(encoding='utf-8') as f:
            reader = csv.DictReader(f)
            count = 0

            for row in reader:
                if not row['NR_MOV']:  # pula registros inválidos
                    continue
                id = int(row.get("NR_MOV"))
                if Donation.objects.filter(id=id).exists():
                    self.stderr.write(f"Donation com ID {id} não encontrado. Pulando...")
                    continue
                
                donor_id = int(row.get("COD_DOA", "0") or "0")
                try:
                    donor = Donor.objects.get(id=donor_id)
                except Donor.DoesNotExist:
                    self.stderr.write(f"Doador com ID {donor_id} não encontrado. Pulando...")
                    continue

                try:
                    amount = Decimal(row['VAL_DOA'].replace(',', '.'))
                except Exception:
                    self.stderr.write(f"Valor inválido: {row['VAL_DOA']}. Pulando...")
                    continue

                expected_at = self.parse_date(row.get('DAT_EMI'))
                paid_at = self.parse_date(row.get('DAT_REC'))
                val_rec = row.get('VAL_REC')
                paid = bool(paid_at and val_rec and val_rec.strip().replace(',', '.').replace('0', '') != "")

                notes = " ".join([
                    row.get('OBS_001', '').strip(),
                    row.get('OBS_002', '').strip(),
                    row.get('OBS_003', '').strip()
                ]).strip()
                
                created_by=user
                if row['COD_FUN']:
                    created_by=User.objects.filter(id=int(row['COD_FUN'])).first()

                Donation.objects.create(
                    id=id,
                    donor=donor,
                    owner=company,
                    created_by=created_by,
                    amount=amount,
                    expected_at=expected_at,
                    paid_at=paid_at if paid else None,
                    paid=paid,
                    notes=notes if notes else None
                )

                count += 1
                self.stdout.write(f"Doação registrada para doador ID {donor_id}")

            self.stdout.write(self.style.SUCCESS(f"{count} doações importadas com sucesso."))

    def parse_date(self, val):
        if not val or val.strip() == '':
            return None
        try:
            return datetime.strptime(val.strip(), '%d/%m/%Y')
        except ValueError:
            return None
