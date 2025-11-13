# Script PowerShell para configurar variáveis de ambiente do banco de dados
# Execute: .\configurar_banco.ps1

Write-Host "Configurando variáveis de ambiente para o banco de dados..." -ForegroundColor Green

$env:USE_MYSQL = "true"
$env:DB_DATABASE = "db_mqtt_teste"
$env:DB_USERNAME = "external"
$env:DB_PASSWORD = "SenhaExt123"
$env:DB_HOST = "10.1.1.243"
$env:DB_PORT = "3306"

Write-Host "Variáveis configuradas:" -ForegroundColor Yellow
Write-Host "  USE_MYSQL: $env:USE_MYSQL"
Write-Host "  DB_HOST: $env:DB_HOST"
Write-Host "  DB_DATABASE: $env:DB_DATABASE"
Write-Host "  DB_USERNAME: $env:DB_USERNAME"
Write-Host ""
Write-Host "Testando conexão..." -ForegroundColor Green

python contar_registros_mysql.py

Write-Host ""
Write-Host "Para usar essas variáveis no terminal atual, execute:" -ForegroundColor Cyan
Write-Host "  .\configurar_banco.ps1" -ForegroundColor White
Write-Host ""
Write-Host "Ou configure manualmente no arquivo .env" -ForegroundColor Cyan

