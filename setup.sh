#!/bin/bash

# Script de Setup Rápido - Dashboard de Leituras
# Este script automatiza a configuração inicial do projeto
# Compatível com macOS e Linux

set -e  # Parar em caso de erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # Sem cor

# Função para imprimir com cores
print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Verificações iniciais
print_header "Verificando Pré-requisitos"

# Verificar Python
if ! command -v python3 &> /dev/null; then
    print_error "Python3 não encontrado. Por favor, instale Python 3.8+"
    exit 1
fi
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
print_success "Python $PYTHON_VERSION instalado"

# Verificar Git
if ! command -v git &> /dev/null; then
    print_warning "Git não encontrado. Algumas funcionalidades podem não funcionar."
else
    print_success "Git instalado"
fi

# Setup
print_header "Configurando Projeto"

# 1. Criar ambiente virtual
if [ ! -d "venv" ]; then
    print_warning "Criando ambiente virtual..."
    python3 -m venv venv
    print_success "Ambiente virtual criado"
else
    print_success "Ambiente virtual já existe"
fi

# 2. Ativar ambiente virtual
print_warning "Ativando ambiente virtual..."
source venv/bin/activate
print_success "Ambiente virtual ativado"

# 3. Atualizar pip
print_warning "Atualizando pip..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
print_success "Pip atualizado"

# 4. Instalar dependências
print_warning "Instalando dependências..."
pip install -r requirements.txt > /dev/null 2>&1
print_success "Dependências instaladas"

# 5. Criar arquivo .env se não existir
if [ ! -f ".env" ]; then
    print_warning "Criando arquivo .env..."
    cp .env.example .env
    print_success "Arquivo .env criado (edite antes de executar)"
    print_warning "IMPORTANTE: Edite o arquivo .env com suas configurações"
else
    print_success "Arquivo .env já existe"
fi

# 6. Executar migrações
print_warning "Aplicando migrações do banco..."
python manage.py migrate
print_success "Migrações aplicadas"

# 7. Coletar arquivos estáticos
print_warning "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput > /dev/null 2>&1
print_success "Arquivos estáticos coletados"

# 8. Criar superusuário (se solicitado)
print_header "Criar Superusuário?"
read -p "Deseja criar um superusuário agora? (s/n): " choice
if [[ $choice == "s" || $choice == "S" ]]; then
    python manage.py createsuperuser
    print_success "Superusuário criado"
fi

# Fim
print_header "Setup Completo! ✓"
echo ""
echo "Para iniciar o servidor de desenvolvimento, execute:"
echo -e "${BLUE}source venv/bin/activate${NC}"
echo -e "${BLUE}python manage.py runserver${NC}"
echo ""
echo "A aplicação estará disponível em: http://localhost:8000"
echo ""
print_warning "Não esqueça de:"
echo "  1. Editar o arquivo .env com suas configurações"
echo "  2. Configurar as credenciais do banco de dados"
echo "  3. Alterar a SECRET_KEY em produção"
echo ""
