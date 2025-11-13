# Sistema de Leituras - Django

Sistema de monitoramento e agregação de leituras de sensores desenvolvido com Django.

## 📋 Requisitos

- Python 3.8+
- MySQL 5.7+ (ou SQLite para desenvolvimento)
- Node.js 16+ (para build de assets)
- pip

## 🚀 Instalação

1. **Clone o repositório e navegue até a pasta**

2. **Crie um ambiente virtual**
```bash
python -m venv venv
```

3. **Ative o ambiente virtual**
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. **Instale as dependências Python**
```bash
pip install -r requirements.txt
```
> Observação: o projeto utiliza `PyMySQL`, que não requer compilação no Windows.

5. **Instale as dependências Node.js**
```bash
npm install
```

6. **Configure o banco de dados**
- Crie um arquivo `.env` na raiz do projeto
- Configure as credenciais do MySQL (adicione `USE_MYSQL=true` para ativar):
```env
USE_MYSQL=true
DB_DATABASE=leituras_db
DB_USERNAME=root
DB_PASSWORD=sua_senha
DB_HOST=127.0.0.1
DB_PORT=3306
```
- Sem `USE_MYSQL=true`, o projeto utilizará automaticamente SQLite (`database/database.sqlite`).

7. **Execute as migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

8. **Crie um superusuário (opcional)**
```bash
python manage.py createsuperuser
```

9. **Compile os assets estáticos**
```bash
npm run build
```

10. **Execute o servidor de desenvolvimento**
```bash
python manage.py runserver
```

11. **Acesse o sistema**
- Frontend: http://127.0.0.1:8000
- Admin: http://127.0.0.1:8000/admin

## 📁 Estrutura do Projeto

```
leituras_project/           # Configurações do projeto Django
├── settings.py            # Configurações principais
├── urls.py               # URLs principais
├── wsgi.py              # WSGI config
└── asgi.py              # ASGI config

leituras/                 # App principal
├── models.py            # Models Django
├── views.py             # Views (controllers)
├── urls.py              # URLs do app
├── admin.py             # Configuração do Django Admin
└── management/
    └── commands/
        └── agregar_leituras.py  # Comando customizado

templates/               # Templates HTML Django
├── base.html           # Template base
└── leituras/
    └── index.html      # Template principal

static/                 # Arquivos estáticos
├── src/               # Código fonte (CSS/JS)
│   ├── css/
│   └── js/
├── dist/              # Arquivos compilados (gerado pelo Vite)
└── images/            # Imagens

database/              # Banco de dados
└── database.sqlite    # SQLite (desenvolvimento)
```

## 🔧 Comandos Disponíveis

### Agregar dados
```bash
python manage.py agregar_leituras --periodo hora
```

Opções de período: `hora`, `dia`, `semana`

### Coletar arquivos estáticos (produção)
```bash
python manage.py collectstatic
```

### Criar migrations
```bash
python manage.py makemigrations
```

### Aplicar migrations
```bash
python manage.py migrate
```

### Executar servidor de desenvolvimento
```bash
python manage.py runserver
```

### Build de assets (desenvolvimento)
```bash
npm run dev
```

### Build de assets (produção)
```bash
npm run build
```

## 🎨 Frontend

O frontend utiliza:
- **Bootstrap 5** para layout responsivo
- **Tailwind CSS** (via Vite) para estilização
- **Chart.js** para gráficos (se necessário)
- **Vite** para build de assets

Principais componentes:
- Navbar responsivo
- Cards com estatísticas
- Filtros dinâmicos
- Tabela de dados responsiva
- Sistema de mensagens (alerts)

## 📊 Funcionalidades

✅ Listagem de dados agregados  
✅ Filtros por cliente, equipamento e data  
✅ Agregação de dados por hora/dia/semana  
✅ Exportação para CSV  
✅ Dashboard com estatísticas  
✅ Design responsivo com Bootstrap  
✅ Sistema de mensagens (success/error)  
✅ Interface administrativa Django  

## 🗄️ Banco de Dados

O sistema utiliza as seguintes tabelas:

- `corrente_brunidores` - Leituras de corrente dos brunidores
- `corrente_descascadores` - Leituras de corrente dos descascadores
- `corrente_polidores` - Leituras de corrente dos polidores
- `temperaturas` - Leituras de temperatura
- `umidades` - Leituras de umidade
- `grandezas_eletricas` - Grandezas elétricas (tensão, corrente, potência)
- `dados_agregados` - Dados agregados por período

## 🔐 Segurança

- CSRF Protection habilitado
- SQL Injection protection (Django ORM)
- XSS Protection
- Configurações de segurança no settings.py
- Validação de dados nos models

## 🛠️ Tecnologias

- **Backend:** Django 4.2.7
- **Database:** MySQL (produção) / SQLite (desenvolvimento)
- **Frontend:** Bootstrap 5, Tailwind CSS, Vite
- **JavaScript:** Chart.js, Axios

## 📝 Notas

- Timezone configurado para `America/Sao_Paulo`
- Charset UTF-8 em todo o sistema
- Compatível com MySQL 5.7+
- Responsive design para mobile
- Assets compilados via Vite para otimização

## 🚀 Deploy

Para produção:

1. Configure `DEBUG = False` em `settings.py`
2. Configure `ALLOWED_HOSTS` com seu domínio
3. Execute `python manage.py collectstatic`
4. Configure servidor web (Nginx/Apache) e WSGI (Gunicorn/uWSGI)
5. Configure variáveis de ambiente no servidor

## 📄 Licença

Este projeto está sob a licença MIT.
