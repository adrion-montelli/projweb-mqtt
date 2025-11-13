@echo off
REM Script batch para configurar variáveis de ambiente do banco de dados
REM Execute: configurar_banco.bat

echo Configurando variáveis de ambiente para o banco de dados...

set USE_MYSQL=true
set DB_DATABASE=db_mqtt_teste
set DB_USERNAME=external
set DB_PASSWORD=SenhaExt123
set DB_HOST=10.1.1.243
set DB_PORT=3306

echo.
echo Variáveis configuradas:
echo   USE_MYSQL=%USE_MYSQL%
echo   DB_HOST=%DB_HOST%
echo   DB_DATABASE=%DB_DATABASE%
echo   DB_USERNAME=%DB_USERNAME%
echo.
echo Testando conexão...
echo.

python contar_registros_mysql.py

echo.
echo Para usar essas variáveis, execute este script antes de usar o Django:
echo   configurar_banco.bat
echo.
echo Ou configure manualmente no arquivo .env
pause

