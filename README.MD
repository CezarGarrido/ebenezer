# 📦 Ebenezer

Projeto desenvolvido com [Django](https://www.djangoproject.com/).

## 🚀 Funcionalidades

- [x] Autenticação de usuários (login/logout)
- [x] Painel administrativo com Django Admin
- [x] CRUD completo para [entidades principais]
- [x] Interface usando Jazzmin

## 🧱 Pré-requisitos

Antes de começar, você vai precisar ter instalado:

- Python 3.6+
- pip
- jazzmin https://django-jazzmin.readthedocs.io/
## ⚙️ Instalação

Clone o repositório:
```bash
git clone https://github.com/CezarGarrido/ebenezer
cd ebenezer
```

### Env
```bash
python -m venv env
source env/bin/activate  # no Windows: env\Scripts\activate
pip install -r requirements.txt
```

### Aplique as migrações e crie um superusuário:
```bash
python manage.py makemigrations
python manage.py migrate
```

### ▶️ Executando o projeto
```bash
python manage.py create_admin (admin@admin.com, admin)
python manage.py createsuperuser (Opcional) Usuário personalizado

python manage.py runserver "0.0.0.0:8099"
```

Abra no navegador: http://127.0.0.1:8099/admin
