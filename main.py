import sys
import os
import platform
import subprocess
import re
from django.core.management import execute_from_command_line

def get_first_ipv4():
    system = platform.system()
    try:
        if system == 'Windows':
            output = subprocess.check_output("ipconfig", encoding='utf-8')
            matches = re.findall(r'IPv4.*?:\s*([\d\.]+)', output)
            for ip in matches:
                if not ip.startswith("127."):
                    return ip
        else:
            output = subprocess.check_output(['hostname', '-I'], encoding='utf-8').strip()
            ips = [ip for ip in output.split() if '.' in ip and not ip.startswith('127.')]
            return ips[0] if ips else '127.0.0.1'
    except Exception:
        return '127.0.0.1'

def start_django_server():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ebenezer.settings')
    execute_from_command_line(['manage.py', 'makemigrations'])
    execute_from_command_line(['manage.py', 'migrate'])
    execute_from_command_line(['manage.py', 'create_admin'])
    ip = get_first_ipv4()
    print(f"Servidor rodando em http://{ip}:8099")
    execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8099', '--noreload'])

def main():
    print("Iniciando servidor Django...")
    try:
        start_django_server()
    except KeyboardInterrupt:
        print("\nServidor interrompido pelo usuário.")
    except Exception as e:
        print(f"Erro ao iniciar o servidor: {e}")

if __name__ == "__main__":
    main()
