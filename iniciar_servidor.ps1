# Script PowerShell para iniciar o servidor Django com as configurações corretas do banco
# Execute: .\iniciar_servidor.ps1
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
