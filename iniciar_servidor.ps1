# Script PowerShell para iniciar o servidor Django com as configurações corretas do banco
# Execute: .\iniciar_servidor.ps1

Write-Host "Configurando variáveis de ambiente..." -ForegroundColor Green

$env:USE_MYSQL = "true"
$env:DB_DATABASE = "db_mqtt_teste"
$env:DB_USERNAME = "external"
$env:DB_PASSWORD = "SenhaExt123"
$env:DB_HOST = "10.1.1.243"
$env:DB_PORT = "3306"

Write-Host "Variáveis configuradas!" -ForegroundColor Yellow
Write-Host ""
Write-Host "Testando conexão..." -ForegroundColor Green
python manage.py testar_conexao

Write-Host ""
Write-Host "Verificando dados..." -ForegroundColor Green
python manage.py shell -c "from leituras.models import DadosAgregados; print('Total de registros:', DadosAgregados.objects.count())"

Write-Host ""
Write-Host "Iniciando servidor Django..." -ForegroundColor Green
Write-Host "Acesse: http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host ""
python manage.py runserver

