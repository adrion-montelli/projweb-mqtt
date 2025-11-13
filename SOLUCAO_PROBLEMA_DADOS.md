# 🔧 Solução: Dados não aparecem na tela

## Problema Identificado

O servidor Django estava sendo iniciado **sem as variáveis de ambiente configuradas**, então estava usando o **SQLite local** (vazio) em vez do **MySQL remoto** (com 1.848 registros).

## ✅ Solução Implementada

Atualizei o `settings.py` para usar `python-decouple`, que **carrega automaticamente o arquivo `.env`**.

Agora você tem **3 opções** para garantir que os dados apareçam:

---

## Opção 1: Criar arquivo `.env` (RECOMENDADO - Permanente)

1. **Crie um arquivo `.env` na raiz do projeto** (mesma pasta do `manage.py`)

2. **Cole este conteúdo:**

```env
USE_MYSQL=true
DB_DATABASE=db_mqtt_teste
DB_USERNAME=external
DB_PASSWORD=SenhaExt123
DB_HOST=10.1.1.243
DB_PORT=3306
```

3. **Salve o arquivo**

4. **Execute o servidor normalmente:**

```bash
python manage.py runserver
```

**Pronto!** Agora o Django vai carregar automaticamente as configurações do `.env`.

---

## Opção 2: Usar Scripts de Inicialização

### Windows PowerShell:
```powershell
.\iniciar_servidor.ps1
```

### Windows CMD:
```cmd
iniciar_servidor.bat
```

Esses scripts:
- Configuram as variáveis de ambiente
- Testam a conexão
- Verificam os dados
- Iniciam o servidor

---

## Opção 3: Configurar Variáveis Manualmente

### PowerShell:
```powershell
$env:USE_MYSQL="true"
$env:DB_DATABASE="db_mqtt_teste"
$env:DB_USERNAME="external"
$env:DB_PASSWORD="SenhaExt123"
$env:DB_HOST="10.1.1.243"
$env:DB_PORT="3306"
python manage.py runserver
```

### CMD:
```cmd
set USE_MYSQL=true
set DB_DATABASE=db_mqtt_teste
set DB_USERNAME=external
set DB_PASSWORD=SenhaExt123
set DB_HOST=10.1.1.243
set DB_PORT=3306
python manage.py runserver
```

---

## ✅ Verificação

Após iniciar o servidor, você deve ver:

1. **Total de Leituras**: 1.848 (ou mais, dependendo dos filtros)
2. **Última Atualização**: Data/hora da última agregação
3. **Dados na tabela**: Registros aparecendo

---

## 🔍 Como Verificar se Está Funcionando

### 1. Teste a conexão:
```bash
python manage.py testar_conexao
```

Deve mostrar:
```
✓ Conexão estabelecida com sucesso!
✓ Banco conectado: db_mqtt_teste
✓ Total de tabelas: 18
```

### 2. Verifique os dados:
```bash
python manage.py shell -c "from leituras.models import DadosAgregados; print('Total:', DadosAgregados.objects.count())"
```

Deve mostrar:
```
Total: 1848
```

### 3. Verifique qual banco está sendo usado:
```bash
python manage.py shell -c "from django.conf import settings; db = settings.DATABASES['default']; print('Engine:', db['ENGINE']); print('Database:', db['NAME']); print('Host:', db['HOST'])"
```

Deve mostrar:
```
Engine: django.db.backends.mysql
Database: db_mqtt_teste
Host: 10.1.1.243
```

---

## ⚠️ Importante

- **Sempre use o arquivo `.env`** para desenvolvimento (Opção 1)
- O arquivo `.env` está no `.gitignore`, então não será commitado
- Se você já tem um servidor rodando, **pare e reinicie** após criar o `.env`
- O Django agora carrega o `.env` automaticamente graças ao `python-decouple`

---

## 🚀 Próximos Passos

1. Crie o arquivo `.env` com as credenciais
2. Pare o servidor atual (se estiver rodando)
3. Inicie novamente: `python manage.py runserver`
4. Acesse: http://127.0.0.1:8000
5. Você deve ver os 1.848 registros!

