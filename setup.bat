@echo off
REM Script de Setup Rápido - Dashboard de Leituras
REM Este script automatiza a configuração inicial do projeto
REM Compatível com Windows

setlocal enabledelayedexpansion

REM Cores (emulação com setlocal)
set "header=[94m"
set "success=[92m"
set "error=[91m"
set "warning=[93m"
set "reset=[0m"

REM Função para limpar (Windows não suporta funções, então usamos rótulos)
echo.
echo ========================================
echo Dashboard de Leituras - Setup Windows
echo ========================================
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [91mErro: Python não encontrado. Por favor, instale Python 3.8+[0m
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version') do set "PYTHON_VERSION=%%i"
echo [92m✓ Python %PYTHON_VERSION% instalado[0m

REM Verificar Git
git --version >nul 2>&1
if errorlevel 1 (
    echo [93m⚠ Git não encontrado. Algumas funcionalidades podem não funcionar.[0m
) else (
    echo [92m✓ Git instalado[0m
)

echo.
echo ========================================
echo Configurando Projeto
echo ========================================
echo.

REM Criar ambiente virtual
if not exist "venv\" (
    echo [93m⏳ Criando ambiente virtual...[0m
    python -m venv venv
    echo [92m✓ Ambiente virtual criado[0m
) else (
    echo [92m✓ Ambiente virtual já existe[0m
)

REM Ativar ambiente virtual
echo [93m⏳ Ativando ambiente virtual...[0m
call venv\Scripts\activate.bat
echo [92m✓ Ambiente virtual ativado[0m

REM Atualizar pip
echo [93m⏳ Atualizando pip...[0m
python -m pip install --upgrade pip setuptools wheel >nul 2>&1
echo [92m✓ Pip atualizado[0m

REM Instalar dependências
echo [93m⏳ Instalando dependências...[0m
pip install -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo [91m✗ Erro ao instalar dependências[0m
    pause
    exit /b 1
)
echo [92m✓ Dependências instaladas[0m

REM Criar arquivo .env
if not exist ".env" (
    echo [93m⏳ Criando arquivo .env...[0m
    copy .env.example .env >nul
    echo [92m✓ Arquivo .env criado[0m
    echo [93m⚠ IMPORTANTE: Edite o arquivo .env com suas configurações[0m
) else (
    echo [92m✓ Arquivo .env já existe[0m
)

REM Executar migrações
echo [93m⏳ Aplicando migrações do banco...[0m
python manage.py migrate
if errorlevel 1 (
    echo [91m✗ Erro ao aplicar migrações[0m
    pause
    exit /b 1
)
echo [92m✓ Migrações aplicadas[0m

REM Coletar arquivos estáticos
echo [93m⏳ Coletando arquivos estáticos...[0m
python manage.py collectstatic --noinput >nul 2>&1
echo [92m✓ Arquivos estáticos coletados[0m

REM Criar superusuário
echo.
echo ========================================
echo Criar Superusuário?
echo ========================================
set /p choice="Deseja criar um superusuário agora? (s/n): "

if /i "!choice!"=="s" (
    python manage.py createsuperuser
    echo [92m✓ Superusuário criado[0m
)

REM Fim
echo.
echo ========================================
echo Setup Completo! ✓
echo ========================================
echo.
echo Para iniciar o servidor de desenvolvimento, execute:
echo.
echo   venv\Scripts\activate
echo   python manage.py runserver
echo.
echo A aplicação estará disponível em: http://localhost:8000
echo.
echo [93mNão esqueça de:[0m
echo   1. Editar o arquivo .env com suas configurações
echo   2. Configurar as credenciais do banco de dados
echo   3. Alterar a SECRET_KEY em produção
echo.
pause
