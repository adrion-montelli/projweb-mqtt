@echo off
REM Script batch para iniciar o servidor Django com as configurações corretas do banco
REM Execute: iniciar_servidor.bat

echo Configurando variáveis de ambiente...

set USE_MYSQL=true
set DB_DATABASE=db_mqtt_teste
set DB_USERNAME=external
set DB_PASSWORD=SenhaExt123
set DB_HOST=10.1.1.243
set DB_PORT=3306

echo.
echo Variáveis configuradas!
echo.
echo Testando conexão...
python manage.py testar_conexao

echo.
echo Verificando dados...
python manage.py shell -c "from leituras.models import DadosAgregados; print('Total de registros:', DadosAgregados.objects.count())"

echo.
echo Iniciando servidor Django...
echo Acesse: http://127.0.0.1:8000
echo.
python manage.py runserver

pause

