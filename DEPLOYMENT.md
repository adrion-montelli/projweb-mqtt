# Guia Completo de Deploy - Dashboard de Leituras

## 📋 Índice

1. [Preparação para Produção](#preparação-para-produção)
2. [Deploy Local com Docker](#deploy-local-com-docker)
3. [Deploy Render.com](#deploy-rendercom)
4. [Deploy Railway.app](#deploy-railwayapp)
5. [Deploy em Servidor Linux Dedicado](#deploy-em-servidor-linux-dedicado)
6. [Monitoramento e Manutenção](#monitoramento-e-manutenção)

---

## 🔧 Preparação para Produção

### 1. Gerar SECRET_KEY Segura

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copie a saída e guarde em segurança.

### 2. Atualizar settings.py para Produção

```python
# leituras_project/settings.py

# Segurança
DEBUG = False
ALLOWED_HOSTS = ['seu-dominio.com', 'www.seu-dominio.com']
SECRET_KEY = 'sua-secret-key-gerada-acima'

# HTTPS/SSL
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Headers de Segurança
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_SECURITY_POLICY = {
    "default-src": ("'self'",),
    "script-src": ("'self'", "'unsafe-inline'", "cdn.jsdelivr.net", "cdn.tailwindcss.com"),
    "style-src": ("'self'", "'unsafe-inline'", "cdn.jsdelivr.net", "fonts.googleapis.com"),
    "font-src": ("'self'", "fonts.gstatic.com"),
    "img-src": ("'self'", "data:"),
}

# Banco de Dados (MySQL em produção)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_DATABASE'),
        'USER': os.environ.get('DB_USERNAME'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', 3306),
    }
}
```

### 3. Testar Localmente em Modo Produção

```bash
# Definir DEBUG=False localmente
export DEBUG=False

# Coletar arquivos estáticos
python manage.py collectstatic

# Rodar com Gunicorn
gunicorn leituras_project.wsgi:application --bind 0.0.0.0:8000
```

---

## 🐳 Deploy Local com Docker

### Pré-requisitos
- Docker Desktop instalado
- Docker Compose instalado

### Passos

1. **Criar arquivo `.env.docker`:**
```bash
DEBUG=False
SECRET_KEY=sua-secret-key-aqui
ALLOWED_HOSTS=localhost,127.0.0.1
USE_MYSQL=True
DB_DATABASE=leituras_db
DB_USERNAME=leituras_user
DB_PASSWORD=senha_segura_123
DB_HOST=mysql
DB_PORT=3306
```

2. **Executar Docker Compose:**
```bash
docker-compose up --build
```

3. **Acessar a aplicação:**
```
http://localhost:80
```

4. **Criar superusuário:**
```bash
docker-compose exec web python manage.py createsuperuser
```

5. **Parar containers:**
```bash
docker-compose down
```

---

## 🚀 Deploy Render.com (Recomendado)

### Pré-requisitos
- Repositório GitHub com seu código
- Conta em render.com

### Passos Passo a Passo

#### 1. Preparar Código

```bash
# Criar arquivo render.yaml na raiz do projeto
```

**render.yaml:**
```yaml
services:
  - type: web
    name: leituras-api
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
    startCommand: gunicorn leituras_project.wsgi:application --bind 0.0.0.0:$PORT --workers 4
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: DEBUG
        value: false
      - key: SECRET_KEY
        generateValue: true
      - key: ALLOWED_HOSTS
        value: leituras-api.onrender.com
      - key: USE_MYSQL
        value: true
      - fromGroup: mysql

  - type: mysql
    name: leituras-mysql
    plan: free
    ipAllowList: []
    envVars:
      - key: MYSQL_DATABASE
        value: leituras_db
      - key: MYSQL_USER
        value: leituras_user
      - key: MYSQL_PASSWORD
        generateValue: true
      - key: MYSQL_ROOT_PASSWORD
        generateValue: true
```

#### 2. Conectar ao Render

1. Acessar https://render.com
2. Clicar em "New +" > "Blueprint"
3. Conectar repositório GitHub
4. Selecionar branch principal
5. Render detectará `render.yaml` automaticamente

#### 3. Configurar Variáveis de Ambiente

1. No dashboard Render, ir para "Environment"
2. Adicionar:
   - `DB_HOST`: copiar hostname MySQL do Render
   - `DB_PORT`: 3306
   - `SECRET_KEY`: gerar nova
   - `ALLOWED_HOSTS`: seu-dominio.onrender.com

#### 4. Deploy

```bash
# Push para GitHub (Render faz deploy automático)
git push origin main
```

#### 5. Verificar Status

```
Render Dashboard > Logs > Ver status de deploy
```

---

## 🚃 Deploy Railway.app

### Pré-requisitos
- Repositório GitHub
- Conta em railway.app
- CLI do Railway (opcional)

### Usando Web Dashboard

1. Acessar https://railway.app
2. Clique em "New Project"
3. Selecione "Deploy from GitHub"
4. Autorize GitHub
5. Selecione seu repositório

### Configurar Variáveis

Na aba "Variables":
```
DJANGO_SETTINGS_MODULE=leituras_project.settings
ENVIRONMENT=production
DEBUG=False
SECRET_KEY=sua-secret-key-aqui
ALLOWED_HOSTS=seu-app.railway.app
USE_MYSQL=True
DB_DATABASE=leituras
DB_USERNAME=railway_user
DB_PASSWORD=auto-gerado-pelo-railway
DB_HOST=seu-mysql-railway.railway.app
DB_PORT=3306
```

### Build Command

```
pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
```

### Start Command

```
gunicorn leituras_project.wsgi:application --bind 0.0.0.0:$PORT
```

---

## 🖥️ Deploy em Servidor Linux Dedicado

### Pré-requisitos
- Servidor com Ubuntu 20.04+
- SSH acesso ao servidor
- Domínio (opcional)
- SSL (Let's Encrypt)

### 1. Preparar Servidor

```bash
# SSH no servidor
ssh usuario@seu-servidor.com

# Atualizar pacotes
sudo apt update && sudo apt upgrade -y

# Instalar dependências
sudo apt install -y python3.11 python3.11-venv python3-pip \
    mysql-server mysql-client libmysqlclient-dev \
    nginx git supervisor certbot python3-certbot-nginx
```

### 2. Clonar e Configurar Aplicação

```bash
# Criar diretório
sudo mkdir -p /var/www/leituras
cd /var/www/leituras

# Clonar repositório
sudo git clone https://github.com/seu-usuario/projweb-mqtt.git .

# Criar ambiente virtual
python3.11 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 3. Configurar Banco de Dados

```bash
# Acessar MySQL
sudo mysql -u root -p

# Criar banco e usuário
CREATE DATABASE leituras_db;
CREATE USER 'leituras_user'@'localhost' IDENTIFIED BY 'senha_segura_123';
GRANT ALL PRIVILEGES ON leituras_db.* TO 'leituras_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 4. Configurar Django

```bash
# Criar arquivo .env
sudo nano /var/www/leituras/.env

# Adicionar:
DEBUG=False
SECRET_KEY=sua-secret-key-gerada
ALLOWED_HOSTS=seu-dominio.com,www.seu-dominio.com
USE_MYSQL=True
DB_DATABASE=leituras_db
DB_USERNAME=leituras_user
DB_PASSWORD=senha_segura_123
DB_HOST=127.0.0.1
DB_PORT=3306
```

### 5. Executar Migrações

```bash
cd /var/www/leituras
source venv/bin/activate
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### 6. Configurar Gunicorn

```bash
# Arquivo systemd
sudo nano /etc/systemd/system/leituras.service
```

```ini
[Unit]
Description=Leituras Dashboard Gunicorn
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/leituras
Environment="PATH=/var/www/leituras/venv/bin"
ExecStart=/var/www/leituras/venv/bin/gunicorn \
    --workers 4 \
    --worker-class sync \
    --bind unix:/var/www/leituras/leituras.sock \
    leituras_project.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
# Ativar serviço
sudo systemctl daemon-reload
sudo systemctl start leituras
sudo systemctl enable leituras
```

### 7. Configurar Nginx

```bash
sudo nano /etc/nginx/sites-available/leituras
```

```nginx
server {
    listen 80;
    server_name seu-dominio.com www.seu-dominio.com;

    client_max_body_size 20M;

    location = /favicon.ico {
        access_log off;
        log_not_found off;
    }

    location /static/ {
        alias /var/www/leituras/staticfiles/;
    }

    location /media/ {
        alias /var/www/leituras/media/;
    }

    location / {
        proxy_pass http://unix:/var/www/leituras/leituras.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Ativar site
sudo ln -s /etc/nginx/sites-available/leituras /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 8. Configurar SSL (Let's Encrypt)

```bash
sudo certbot --nginx -d seu-dominio.com -d www.seu-dominio.com
```

---

## 📊 Monitoramento e Manutenção

### Verificar Status

```bash
# Systemd
sudo systemctl status leituras

# Logs
sudo journalctl -u leituras -f

# Nginx
sudo systemctl status nginx
```

### Backup do Banco de Dados

```bash
# Backup manual
mysqldump -u leituras_user -p leituras_db > backup_$(date +%Y%m%d).sql

# Backup automático (Cron)
# Adicionar ao crontab -e
0 2 * * * mysqldump -u leituras_user -p'senha' leituras_db > /backup/leituras_$(date +\%Y\%m\%d).sql
```

### Atualizar Aplicação

```bash
# SSH no servidor
ssh usuario@seu-servidor.com
cd /var/www/leituras
source venv/bin/activate

# Pull novas mudanças
git pull origin main

# Instalar novas dependências
pip install -r requirements.txt

# Aplicar migrações
python manage.py migrate

# Coletar estáticos
python manage.py collectstatic --noinput

# Reiniciar serviço
sudo systemctl restart leituras
```

### Monitoramento com Sentry (Opcional)

```bash
# Instalar
pip install sentry-sdk

# Adicionar ao settings.py
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="sua-sentry-dsn",
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.1,
    send_default_pii=False
)
```

---

## ✅ Checklist Final

- [ ] Gerar nova SECRET_KEY
- [ ] Configurar ALLOWED_HOSTS
- [ ] DEBUG = False
- [ ] Banco de dados configurado em produção
- [ ] HTTPS/SSL ativo
- [ ] Arquivo .env seguro (não versionado)
- [ ] Arquivos estáticos coletados
- [ ] Testes locais em modo produção executados
- [ ] Backup do banco antes de deploy
- [ ] Monitoramento configurado
- [ ] Email de erros configurado

---

## 🆘 Troubleshooting

### Erro 500 em Produção

```bash
# Verificar logs
tail -f /var/log/nginx/error.log
sudo journalctl -u leituras -f
```

### Arquivos estáticos não carregam

```bash
# Re-coletar
python manage.py collectstatic --clear --noinput

# Verificar permissões
sudo chown -R www-data:www-data /var/www/leituras/staticfiles
```

### Banco de dados conectando

```bash
# Testar conexão
mysql -h localhost -u leituras_user -p -e "SELECT 1"

# Verificar .env
cat /var/www/leituras/.env | grep DB_
```

---

**Última Atualização:** Novembro 2024
