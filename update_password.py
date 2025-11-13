#!/usr/bin/env python
import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'leituras_project.settings')
django.setup()

User = get_user_model()

username = 'adrion.costa'
password = 'Senha@123'

try:
    user = User.objects.get(username=username)
    user.set_password(password)
    user.save()
    print(f"✓ Senha do superuser '{username}' atualizada com sucesso!")
    print(f"  Nova senha: {password}")
    print(f"  Acesse http://127.0.0.1:8000/admin para login")
except User.DoesNotExist:
    print(f"✗ Superuser '{username}' não encontrado.")
