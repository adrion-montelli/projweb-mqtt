# 🚀 Passo a Passo: Conectar Projeto ao Banco Remoto

## Opção 1: Usando Arquivo .env (Recomendado)

### 1. Crie o arquivo `.env` na raiz do projeto

Crie um arquivo chamado `.env` (sem extensão) na pasta raiz do projeto com este conteúdo:

```env
USE_MYSQL=true
DB_DATABASE=db_mqtt_teste
DB_USERNAME=external
DB_PASSWORD=SenhaExt123
DB_HOST=10.1.1.243
DB_PORT=3306
```

### 2. Teste a conexão

```bash
python manage.py testar_conexao
```

Se funcionar, você verá: `✓ Conexão estabelecida com sucesso!`

### 3. Verifique as migrations

```bash
python manage.py showmigrations
```

### 4. Se necessário, marque as migrations como aplicadas (o banco já tem dados)

```bash
python manage.py migrate --fake
```

### 5. Execute o servidor

```bash
python manage.py runserver
```

Acesse: http://127.0.0.1:8000

---

## Opção 2: Usando Variáveis de Ambiente (Windows PowerShell)

### 1. Execute o script de configuração

```powershell
.\configurar_banco.ps1
```

Ou configure manualmente:

```powershell
$env:USE_MYSQL="true"
$env:DB_DATABASE="db_mqtt_teste"
$env:DB_USERNAME="external"
$env:DB_PASSWORD="SenhaExt123"
$env:DB_HOST="10.1.1.243"
$env:DB_PORT="3306"
```

### 2. Teste a conexão

```bash
python manage.py testar_conexao
```

### 3. Execute o servidor (no mesmo terminal PowerShell)

```bash
python manage.py runserver
```

---

## Opção 3: Usando Variáveis de Ambiente (Windows CMD)

### 1. Execute o script de configuração

```cmd
configurar_banco.bat
```

Ou configure manualmente:

```cmd
set USE_MYSQL=true
set DB_DATABASE=db_mqtt_teste
set DB_USERNAME=external
set DB_PASSWORD=SenhaExt123
set DB_HOST=10.1.1.243
set DB_PORT=3306
```

### 2. Teste a conexão

```bash
python manage.py testar_conexao
```

### 3. Execute o servidor (no mesmo terminal CMD)

```bash
python manage.py runserver
```

---

## ✅ Verificação Rápida

Execute estes comandos para verificar se está tudo configurado:

```bash
# 1. Testar conexão
python manage.py testar_conexao

# 2. Contar registros (deve mostrar os dados do banco)
python contar_registros_mysql.py

# 3. Verificar configuração do Django
python manage.py shell -c "from django.conf import settings; print('Banco:', settings.DATABASES['default']['NAME']); print('Host:', settings.DATABASES['default']['HOST'])"
```

---

## 🔧 Resolução de Problemas

### Erro: "Can't connect to MySQL server"
- Verifique se consegue acessar o PHPMyAdmin: http://10.1.1.243/phpmyadmin
- Teste o ping: `ping 10.1.1.243`
- Verifique se o firewall permite conexões na porta 3306

### Erro: "Access denied"
- Verifique se as credenciais estão corretas
- Teste no PHPMyAdmin com as mesmas credenciais

### Erro: "Unknown database"
- Verifique se o banco `db_mqtt_teste` existe
- Acesse o PHPMyAdmin e confirme

### As variáveis de ambiente não funcionam
- Use o arquivo `.env` (Opção 1)
- Certifique-se de que está no mesmo terminal onde configurou as variáveis

---

## 📝 Notas Importantes

1. **Arquivo .env**: Se você criar o arquivo `.env`, ele será ignorado pelo Git (está no `.gitignore`), o que é correto para segurança.

2. **Migrations**: Como o banco já tem dados, você provavelmente não precisa executar `migrate`. Use `migrate --fake` apenas se necessário.

3. **Dados Existentes**: O banco já possui 112.728 registros nas tabelas da aplicação, então você pode começar a usar imediatamente.

4. **Servidor Remoto**: O banco está em `10.1.1.243`, então você precisa estar na mesma rede ou ter acesso VPN.

