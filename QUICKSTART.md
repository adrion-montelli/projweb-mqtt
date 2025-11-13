# 🚀 Quick Start - Dashboard de Leituras

## ⚡ 5 Minutos para Rodar Localmente

### 1. Clonar e Navegar
```bash
git clone https://github.com/adrion-montelli/projweb-mqtt.git
cd projweb-mqtt
```

### 2. Setup Automático

#### Windows
```bash
setup.bat
```

#### Linux / macOS
```bash
bash setup.sh
```

### 3. Executar
```bash
python manage.py runserver
```

### 4. Acessar
Abra seu navegador em: **http://localhost:8000**

### 5. Login
- Username: `admin` (criado no setup)
- Senha: (a que você definiu)

---

## 🐳 Com Docker

```bash
docker-compose up --build
```

Acesse em: **http://localhost:80**

---

## 📋 Checklist Pré-requisitos

- [ ] Python 3.8+ instalado
- [ ] pip funcionando
- [ ] MySQL (opcional - SQLite é padrão)
- [ ] Git instalado

---

## 🎨 Alterar Tema

Clique no ícone ☀️/🌙 na navbar superior.

---

## 📚 Documentação

- **Instalação Completa:** [README.md](README.md)
- **Deploy em Produção:** [DEPLOYMENT.md](DEPLOYMENT.md)
- **Contribuir:** [CONTRIBUTING.md](CONTRIBUTING.md)
- **O que Mudou:** [REFACTORING_SUMMARY.md](REFACTORING_SUMMARY.md)

---

## ❓ Problemas?

### Erro: "Command not found: python3"
Instale Python 3.8+ em https://python.org

### Erro: "ModuleNotFoundError: No module named 'django'"
Execute: `pip install -r requirements.txt`

### Porta 8000 em uso
Use outra porta: `python manage.py runserver 8001`

---

## ✨ Próximos Passos

1. ✅ Explore o dashboard
2. 📊 Verifique os gráficos
3. 🔐 Teste a autenticação
4. 🌙 Alterne tema escuro
5. 📱 Teste em celular
6. 🚀 Leia DEPLOYMENT.md para produção

---

**Bem-vindo ao Dashboard! 🎉**
