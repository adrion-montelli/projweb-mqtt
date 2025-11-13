# Instruções para Contar Registros no Banco db_mqtt_teste

## Opção 1: Usando o Script Python (Recomendado)

### 1. Configure as credenciais do MySQL

Você pode configurar de três formas:

#### A) Via variáveis de ambiente (Windows PowerShell):
```powershell
$env:DB_HOST="127.0.0.1"
$env:DB_PORT="3306"
$env:DB_USERNAME="root"
$env:DB_PASSWORD="sua_senha_aqui"
$env:DB_DATABASE="db_mqtt_teste"
python contar_registros_mysql.py
```

#### B) Via variáveis de ambiente (Windows CMD):
```cmd
set DB_HOST=127.0.0.1
set DB_PORT=3306
set DB_USERNAME=root
set DB_PASSWORD=sua_senha_aqui
set DB_DATABASE=db_mqtt_teste
python contar_registros_mysql.py
```

#### C) Editando o arquivo `contar_registros_mysql.py`:
Edite as linhas 12-18 do arquivo e configure:
```python
DB_CONFIG = {
    'host': '127.0.0.1',        # Host do MySQL
    'port': 3306,                # Porta do MySQL
    'user': 'root',              # Usuário do MySQL
    'password': 'sua_senha',     # Senha do MySQL
    'database': 'db_mqtt_teste', # Nome do banco
    'charset': 'utf8mb4'
}
```

### 2. Execute o script:
```bash
python contar_registros_mysql.py
```

## Opção 2: Usando o Comando Django (se o banco estiver configurado no Django)

Se você configurou o Django para usar o banco `db_mqtt_teste`, você pode usar:

```bash
python manage.py contar_registros
```

**Nota:** Para usar o banco `db_mqtt_teste` no Django, configure o arquivo `.env`:
```env
USE_MYSQL=true
DB_DATABASE=db_mqtt_teste
DB_USERNAME=root
DB_PASSWORD=sua_senha
DB_HOST=127.0.0.1
DB_PORT=3306
```

## Opção 3: Consulta SQL Direta no PHPMyAdmin

Se preferir usar o PHPMyAdmin diretamente, execute estas queries:

### Contar registros em cada tabela:
```sql
SELECT 
    'corrente_brunidores' as tabela, COUNT(*) as total FROM corrente_brunidores
UNION ALL
SELECT 'corrente_descascadores', COUNT(*) FROM corrente_descascadores
UNION ALL
SELECT 'corrente_polidores', COUNT(*) FROM corrente_polidores
UNION ALL
SELECT 'temperaturas', COUNT(*) FROM temperaturas
UNION ALL
SELECT 'umidades', COUNT(*) FROM umidades
UNION ALL
SELECT 'grandezas_eletricas', COUNT(*) FROM grandezas_eletricas
UNION ALL
SELECT 'dados_agregados', COUNT(*) FROM dados_agregados
ORDER BY tabela;
```

### Ver todas as tabelas e seus registros:
```sql
SELECT 
    TABLE_NAME as tabela,
    TABLE_ROWS as registros_aproximados
FROM information_schema.TABLES 
WHERE TABLE_SCHEMA = 'db_mqtt_teste'
ORDER BY TABLE_NAME;
```

### Contagem exata de todas as tabelas (pode ser lento):
```sql
SELECT 
    TABLE_NAME as tabela,
    (SELECT COUNT(*) FROM information_schema.TABLES t2 
     WHERE t2.TABLE_SCHEMA = 'db_mqtt_teste' 
     AND t2.TABLE_NAME = t1.TABLE_NAME) as total
FROM information_schema.TABLES t1
WHERE TABLE_SCHEMA = 'db_mqtt_teste'
ORDER BY TABLE_NAME;
```

## Resolução de Problemas

### Erro: "Can't connect to MySQL server"
- Verifique se o MySQL está rodando
- Verifique se a porta está correta (padrão: 3306)
- Verifique se o host está correto (127.0.0.1 para localhost)

### Erro: "Access denied"
- Verifique se o usuário e senha estão corretos
- Verifique se o usuário tem permissão para acessar o banco `db_mqtt_teste`

### Erro: "Unknown database 'db_mqtt_teste'"
- Verifique se o banco existe
- Crie o banco se necessário: `CREATE DATABASE db_mqtt_teste;`

