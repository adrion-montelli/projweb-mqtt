#!/usr/bin/env python
import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'leituras_project.settings')
django.setup()

User = get_user_model()

# Criar superuser
username = 'adrion.costa'
email = 'adrionmontellicosta@gmail.com'
password = 'Senha@123'  # Altere conforme necessário

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"✓ Superuser '{username}' criado com sucesso!")
    print(f"  Email: {email}")
    print(f"  Acesse http://127.0.0.1:8000/admin para login")
else:
    print(f"✗ Superuser '{username}' já existe.")
