# Sistema de Leituras - Django

Conversão do sistema Laravel para Django mantendo todas as funcionalidades.

## 📋 Requisitos

- Python 3.8+
- MySQL 5.7+
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

4. **Instale as dependências**
```bash
pip install -r requirements.txt
```

5. **Configure o banco de dados**
- Copie `.env.example` para `.env`
- Configure as credenciais do MySQL no arquivo `.env`

6. **Execute as migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

7. **Crie um superusuário (opcional)**
```bash
python manage.py createsuperuser
```

8. **Execute o servidor**
```bash
python manage.py runserver
```

9. **Acesse o sistema**
- Frontend: http://127.0.0.1:8000
- Admin: http://127.0.0.1:8000/admin

## 📁 Estrutura do Projeto

```
leituras_project/           # Configurações do projeto
├── settings.py            # Configurações principais
├── urls.py               # URLs principais
└── wsgi.py              # WSGI config

leituras/                 # App principal
├── models.py            # Models (equivalente às migrations Laravel)
├── views.py             # Views (equivalente aos Controllers Laravel)
├── urls.py              # URLs do app
├── admin.py             # Configuração do Django Admin
└── management/
    └── commands/
        └── agregar_leituras.py  # Comando customizado (equivalente ao Artisan)

templates/               # Templates HTML
└── leituras/
    └── index.html      # Template principal (equivalente às views Blade)
```

## 🔧 Comandos Disponíveis

### Agregar dados
```bash
python manage.py agregar_leituras --periodo hora
```

### Exportar dados
Acesse a interface web e clique em "Exportar CSV"

### Atualizar dados
Clique no botão "Atualizar Dados" na interface

## 🎨 Frontend

O frontend utiliza **Bootstrap 5** para manter a responsividade e design moderno.

Principais componentes:
- Navbar responsivo
- Cards com estatísticas
- Filtros dinâmicos
- Tabela de dados responsiva
- Sistema de mensagens (alerts)

## 🔄 Equivalências Laravel → Django

| Laravel | Django |
|---------|--------|
| Routes (web.php) | URLs (urls.py) |
| Controllers | Views (views.py) |
| Migrations | Models (models.py) |
| Blade Templates | Django Templates |
| Artisan Commands | Management Commands |
| Eloquent ORM | Django ORM |
| `.env` | `.env` + settings.py |

## 📊 Funcionalidades

✅ Listagem de dados agregados  
✅ Filtros por cliente, equipamento e data  
✅ Agregação de dados por hora  
✅ Exportação para CSV  
✅ Dashboard com estatísticas  
✅ Design responsivo com Bootstrap  
✅ Sistema de mensagens (success/error)  

## 🗄️ Banco de Dados

O sistema mantém a mesma estrutura de banco de dados do Laravel:

- `corrente_brunidores`
- `corrente_descascadores`
- `corrente_polidores`
- `temperaturas`
- `umidades`
- `grandezas_eletricas`
- `dados_agregados`

## 🔐 Segurança

- CSRF Protection habilitado
- SQL Injection protection (Django ORM)
- XSS Protection
- Configurações de segurança no settings.py

## 📝 Notas

- Timezone configurado para America/Sao_Paulo
- Charset UTF-8 em todo o sistema
- Compatível com MySQL 5.7+
- Responsive design para mobile
