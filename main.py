import tkinter as tk
from tkinter import messagebox
import threading
import sys
import os
from django.core.management import execute_from_command_line
import platform
import subprocess
import re
from django.contrib.auth import get_user_model
server_thread = None
running = False

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
def create_superuser():
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@admin.com', 'admin')
        print("Superusuário criado: admin / admin")
    else:
        print("Superusuário já existe.")
        
def start_django_server():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ebenezer.settings')
    execute_from_command_line(['manage.py', 'makemigrations'])
    execute_from_command_line(['manage.py', 'migrate'])
    execute_from_command_line(['manage.py', 'create_admin'])
    # Cria o superusuário se não existir
    create_superuser()
    
    execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8099', '--noreload'])

def start_server():
    global server_thread, running
    if not running:
        try:
            server_thread = threading.Thread(target=start_django_server, daemon=True)
            server_thread.start()
            running = True
            ip = get_first_ipv4()
            status_label.config(text=f"Servidor rodando em http://{ip}:8099")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao iniciar servidor:\n{e}")
    else:
        messagebox.showinfo("Aviso", "Servidor já está em execução.")

def stop_server():
    global running
    if running:
        messagebox.showinfo("Aviso", "Feche a janela para encerrar o servidor.")
    else:
        messagebox.showinfo("Aviso", "Servidor não está em execução.")

def on_close():
    if running:
        messagebox.showinfo("Servidor ativo", "Encerrando o servidor...")
    root.destroy()
    sys.exit()

# GUI
root = tk.Tk()
root.title("Gerenciador do Servidor Django")
root.geometry("400x150")
root.resizable(False, False)

frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

tk.Button(frame, text="Iniciar Servidor", width=20, command=start_server).pack(pady=5)
tk.Button(frame, text="Parar Servidor", width=20, command=stop_server).pack(pady=5)

status_label = tk.Label(root, text="Servidor parado.", fg="blue")
status_label.pack()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
