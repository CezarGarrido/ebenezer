import csv
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from pathlib import Path
import unicodedata
import re
from django.contrib.auth.models import Group
import sys
import os
from core.management.commands import importer

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
        parser.add_argument('data_path', type=str, help='Caminho para o arquivo DAT')
        parser.add_argument('data_output', type=str, help='Caminho para o arquivo CSV')

    def handle(self, *args, **kwargs):
        data_path = kwargs['data_path']
        data_output = kwargs['data_output']
        
        if not os.path.isdir(data_path):
            print(f"Error: {data_path} is not a valid directory")
            sys.exit(1)
        
        importer.process_directory(data_path, data_output)