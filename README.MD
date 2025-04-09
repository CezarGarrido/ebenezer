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

## ⚙️ Instalação

Clone o repositório:

```bash
git clone https://github.com/CezarGarrido/ebenezer
cd ebenezer
```

### Env
```bash
python -m venv env
source env/bin/activate  # no Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Aplique as migrações e crie um superusuário:
```bash
python manage.py migrate
python manage.py createsuperuser
```

### ▶️ Executando o projeto
```bash
python manage.py runserver
```
