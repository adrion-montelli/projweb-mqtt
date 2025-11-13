# Dashboard de Leituras de Sensores - Guia Completo

## 🎯 Sobre o Projeto

O **Dashboard de Leituras de Sensores** é uma aplicação Django moderna e responsiva para monitoramento em tempo real de dados de sensores. A aplicação oferece uma interface intuitiva com gráficos interativos, cards informativos e um sistema robusto de autenticação.

### ✨ Funcionalidades Principais

- **🔐 Autenticação Segura**: Sistema de login integrado com Django
- **📊 Gráficos Interativos**: Visualização de dados com Chart.js
- **📱 Responsivo**: Interface totalmente adaptável para dispositivos móveis
- **🎨 Tema Escuro**: Suporte completo a dark mode com localStorage
- **💾 Gerenciamento de Dados**: MySQL integrado para produção
- **⚡ Performance**: Otimizado com caching e compressão
- **🔄 API RESTful**: Endpoints JSON para integração com frontend

---

## 📋 Pré-requisitos

### Sistema Operacional
- Windows 10+, macOS, ou Linux

### Softwares Necessários
- **Python** 3.8 ou superior
- **pip** (gerenciador de pacotes Python)
- **MySQL** (opcional, SQLite disponível para desenvolvimento)
- **Git** (para controle de versão)

### Verificar Versões
```bash
python --version
pip --version
mysql --version  # Se usar MySQL
```

---

## 🚀 Instalação e Configuração

### 1️⃣ Clonar o Repositório
```bash
git clone https://github.com/adrion-montelli/projweb-mqtt.git
cd projweb-mqtt
```

### 2️⃣ Criar Ambiente Virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Instalar Dependências
```bash
pip install -r requirements.txt
```

### 4️⃣ Configurar Variáveis de Ambiente
Criar arquivo `.env` na raiz do projeto (baseado em `.env.example`):

```env
# Django
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Banco de Dados
USE_MYSQL=False
DB_DATABASE=leituras_db
DB_USERNAME=root
DB_PASSWORD=sua-senha
DB_HOST=127.0.0.1
DB_PORT=3306

# Aplicação
APP_NAME=Dashboard de Leituras
TIME_ZONE=America/Sao_Paulo
LANGUAGE_CODE=pt-br
```

### 5️⃣ Executar Migrações
```bash
python manage.py migrate
```

### 6️⃣ Criar Superusuário
```bash
python manage.py createsuperuser
# Preencha com seu username, email e senha
```

### 7️⃣ Coletar Arquivos Estáticos
```bash
python manage.py collectstatic --noinput
```

---

## 🏃 Executar a Aplicação

### Desenvolvimento Local
```bash
python manage.py runserver
```

Acesse em: **http://localhost:8000**

### Com Gunicorn (Produção)
```bash
gunicorn leituras_project.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

---

## 📁 Estrutura do Projeto

```
ProjetoFinalRev4/
├── leituras/                     # App principal Django
│   ├── models.py                 # Modelos de dados
│   ├── views.py                  # Lógica de views
│   ├── urls.py                   # Rotas da app
│   ├── admin.py                  # Configurações de admin
│   ├── management/               # Comandos customizados
│   │   └── commands/
│   │       ├── agregar_leituras.py
│   │       └── contar_registros.py
│   └── migrations/               # Migrações de banco
│
├── leituras_project/             # Configurações do projeto
│   ├── settings.py               # Configurações Django
│   ├── urls.py                   # URLs principais
│   ├── wsgi.py                   # Configuração WSGI
│   └── asgi.py                   # Configuração ASGI
│
├── templates/                    # Templates HTML
│   ├── base.html                 # Template base (navbar, footer)
│   ├── login.html                # Página de login
│   ├── dashboard.html            # Dashboard principal
│   └── leituras/
│       └── index.html            # Listagem de leituras
│
├── static/                       # Arquivos estáticos
│   ├── images/
│   │   └── favicon.ico
│   └── src/
│       ├── css/
│       │   ├── style.css         # Estilos customizados
│       │   └── app.css           # Estilos da app
│       └── js/
│           ├── dashboard.js      # Scripts do dashboard
│           └── app.js            # Scripts gerais
│
├── staticfiles/                  # Arquivos estáticos coletados (produção)
│
├── .env.example                  # Template de variáveis de ambiente
├── requirements.txt              # Dependências Python
├── manage.py                     # Gerenciador Django
├── README.md                     # Este arquivo
└── database/                     # Diretório para arquivos de banco local
```

---

## 🔧 Configuração Avançada

### Configurar MySQL (Produção)

1. **Criar banco de dados:**
```sql
CREATE DATABASE leituras_db;
CREATE USER 'leituras_user'@'localhost' IDENTIFIED BY 'senha_segura';
GRANT ALL PRIVILEGES ON leituras_db.* TO 'leituras_user'@'localhost';
FLUSH PRIVILEGES;
```

2. **Atualizar `.env`:**
```env
USE_MYSQL=True
DB_DATABASE=leituras_db
DB_USERNAME=leituras_user
DB_PASSWORD=senha_segura
DB_HOST=localhost
DB_PORT=3306
```

3. **Executar migrações:**
```bash
python manage.py migrate
```

### Configurar Modo Escuro (Dark Mode)

A aplicação detecta automaticamente a preferência do sistema e salva no localStorage. Clique no ícone de brilho (☀️/🌙) na navbar para alternar temas.

### Habilitar HTTPS

Editar `leituras_project/settings.py`:
```python
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

---

## 🚢 Deploy

### Render.com (Recomendado)

1. **Criar conta em** https://render.com
2. **Conectar repositório GitHub**
3. **Configurar variáveis de ambiente:**
   - `SECRET_KEY`
   - `DEBUG=False`
   - `DATABASE_URL` (MySQL)
4. **Deploy automático**

### Railway.app

```bash
# Instalar CLI do Railway
npm i -g @railway/cli

# Login
railway login

# Deploy
railway up
```

### Heroku (Legado)

```bash
# Instalar Heroku CLI
# Deploy
heroku create seu-app-name
git push heroku main
```

### Docker

Criar `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "leituras_project.wsgi:application", "--bind", "0.0.0.0:8000"]
```

Executar:
```bash
docker build -t dashboard-leituras .
docker run -p 8000:8000 -e SECRET_KEY=sua-chave dashboard-leituras
```

---

## 📊 Tecnologias Utilizadas

| Camada | Tecnologia | Versão |
|--------|-----------|--------|
| **Backend** | Django | 4.2.7 |
| **Banco** | MySQL / SQLite | - |
| **Frontend** | Bootstrap 5 | 5.3.3 |
| **CSS Extra** | Tailwind CSS | 3.x |
| **Gráficos** | Chart.js | 4.4.0 |
| **Ícones** | Material Icons | Latest |
| **Server** | Gunicorn | 22.0.0 |

---

## 🔐 Segurança

### Boas Práticas Implementadas

✅ **CSRF Protection**: Django CSRF middleware ativo
✅ **SQL Injection Prevention**: ORM Django
✅ **XSS Protection**: Django template escaping
✅ **Password Hashing**: PBKDF2 com Django
✅ **HTTPS**: Configurável em produção
✅ **Secret Key**: Variável de ambiente

### Checklist de Segurança para Produção

- [ ] `DEBUG=False`
- [ ] `SECRET_KEY` alterada
- [ ] `ALLOWED_HOSTS` configurado
- [ ] Banco de dados seguro (senha forte)
- [ ] HTTPS/SSL ativo
- [ ] Backup automático do banco
- [ ] Monitoramento de erros (Sentry)

---

## 📝 Comandos Úteis Django

```bash
# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Shell interativo
python manage.py shell

# Executar testes
python manage.py test

# Coletar arquivos estáticos
python manage.py collectstatic

# Limpar cache
python manage.py clear_cache

# Contar registros
python manage.py contar_registros
```

---

## 🐛 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'django'"
**Solução:** Ativar ambiente virtual
```bash
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

### Erro: "Connection refused (port 3306)"
**Solução:** Verificar se MySQL está rodando
```bash
# Windows
net start MySQL80  # ou seu nome de serviço

# macOS
brew services start mysql

# Linux
sudo systemctl start mysql
```

### Erro: "ProgrammingError: table does not exist"
**Solução:** Executar migrações
```bash
python manage.py migrate
```

### Porta 8000 já em uso
**Solução:** Usar outra porta
```bash
python manage.py runserver 8001
```

---

## 📚 Documentação Adicional

- [Django Documentation](https://docs.djangoproject.com)
- [Bootstrap 5 Docs](https://getbootstrap.com/docs/5.3/)
- [Chart.js Docs](https://www.chartjs.org/docs/latest/)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)

---

## 🤝 Contribuindo

1. Fazer fork do projeto
2. Criar branch para feature (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push para branch (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

---

## 📄 Licença

Este projeto está sob licença MIT. Veja `LICENSE` para detalhes.

---

## 👨‍💻 Autor

**Adrion Montelli**
- GitHub: [@adrion-montelli](https://github.com/adrion-montelli)

---

## 🎉 Agradecimentos

- Django Foundation
- Bootstrap Community
- Chart.js Contributors
- Comunidade Python Brasil

---

## 📞 Suporte

Para reportar bugs ou sugerir features:
1. Abrir issue no GitHub
2. Descrever problema detalhadamente
3. Incluir logs/screenshots se necessário

**Última atualização:** Novembro 2024
