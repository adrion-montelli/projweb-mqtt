# Configuração do Banco de Dados Remoto

## Passo 1: Criar arquivo .env

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```env
# Django Settings
SECRET_KEY=django-insecure-change-this-in-production
DEBUG=True

# Database Configuration (MySQL) - Banco Remoto
USE_MYSQL=true
DB_DATABASE=db_mqtt_teste
DB_USERNAME=external
DB_PASSWORD=SenhaExt123
DB_HOST=10.1.1.243
DB_PORT=3306

# Timezone
TIME_ZONE=America/Sao_Paulo

# Allowed Hosts (comma-separated)
ALLOWED_HOSTS=localhost,127.0.0.1,10.1.1.243
```

## Passo 2: Configurar variáveis de ambiente (Alternativa)

Se preferir não usar arquivo .env, configure as variáveis de ambiente:

### Windows PowerShell:
```powershell
$env:USE_MYSQL="true"
$env:DB_DATABASE="db_mqtt_teste"
$env:DB_USERNAME="external"
$env:DB_PASSWORD="SenhaExt123"
$env:DB_HOST="10.1.1.243"
$env:DB_PORT="3306"
```

### Windows CMD:
```cmd
set USE_MYSQL=true
set DB_DATABASE=db_mqtt_teste
set DB_USERNAME=external
set DB_PASSWORD=SenhaExt123
set DB_HOST=10.1.1.243
set DB_PORT=3306
```

### Linux/Mac:
```bash
export USE_MYSQL=true
export DB_DATABASE=db_mqtt_teste
export DB_USERNAME=external
export DB_PASSWORD=SenhaExt123
export DB_HOST=10.1.1.243
export DB_PORT=3306
```

## Passo 3: Testar a conexão

Execute o comando para testar a conexão:

```bash
python manage.py dbshell
```

Ou use o script de teste:

```bash
python contar_registros_mysql.py
```

## Passo 4: Verificar migrations

O banco já possui dados, então você provavelmente não precisa criar as tabelas. Mas pode verificar:

```bash
python manage.py showmigrations
```

Se houver migrations pendentes, execute:

```bash
python manage.py migrate
```

**ATENÇÃO:** Se o banco já tem dados, as migrations podem falhar se as tabelas já existirem. Nesse caso, você pode marcar as migrations como aplicadas:

```bash
python manage.py migrate --fake
```

## Passo 5: Executar o servidor

```bash
python manage.py runserver
```

Acesse: http://127.0.0.1:8000

## Resolução de Problemas

### Erro: "Can't connect to MySQL server"
- Verifique se o servidor 10.1.1.243 está acessível
- Verifique se o firewall permite conexões na porta 3306
- Teste a conexão: `ping 10.1.1.243`

### Erro: "Access denied"
- Verifique se as credenciais estão corretas
- Verifique se o usuário 'external' tem permissão para acessar o banco 'db_mqtt_teste'

### Erro: "Unknown database"
- Verifique se o banco 'db_mqtt_teste' existe no servidor

