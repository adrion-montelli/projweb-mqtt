# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
e este projeto adota [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [1.0.0] - 2024-11-13

### Adicionado
- ✨ Dashboard interativo com cards informativos
- 📊 Gráficos dinâmicos com Chart.js
- 🔐 Sistema de autenticação com Django Auth
- 📱 Interface completamente responsiva
- 🎨 Suporte a tema escuro/claro (Dark Mode)
- 🎯 API RESTful para dados dos gráficos
- 📚 Documentação completa (README, DEPLOYMENT, CONTRIBUTING)
- 🐳 Suporte a Docker e Docker Compose
- 📋 Configuração para deploy em Render, Railway e servidores Linux
- ✅ Script de setup automático (Windows e Linux)
- 🔒 Boas práticas de segurança implementadas
- 💾 Integração com MySQL para produção

### Mudanças
- 🔄 Refatoração completa do frontend com Bootstrap 5
- 🎨 Migração do Materialize para Bootstrap 5 + Tailwind CSS
- 📦 Atualização de dependências para versões estáveis
- 🏗️ Reorganização da estrutura de arquivos estáticos

### Corrigido
- 🐛 Problemas de responsividade em dispositivos móveis
- 🐛 Performance de gráficos com grande volume de dados
- 🐛 Validação de formulários no frontend
- 🐛 Temas de cores inconsistentes

### Removido
- ❌ Materialize CSS (substituído por Bootstrap 5)
- ❌ Estilos customizados antigos
- ❌ Dependências não utilizadas
- ❌ Arquivos de backup desnecessários

## [0.9.0] - 2024-11-01

### Adicionado
- Estrutura inicial do projeto Django
- Modelos de dados para leituras de sensores
- Views básicas para listagem de dados
- Templates HTML simples

### Trabalho em Progresso
- [ ] Testes unitários completos
- [ ] Integração contínua com GitHub Actions
- [ ] Sistema de notificações em tempo real (WebSockets)
- [ ] Exportação de dados em CSV/PDF
- [ ] API GraphQL
- [ ] Aplicativo mobile (React Native/Flutter)

---

## Plano Futuro

### v1.1.0 (Próximas Semanas)
- [ ] Sistema de alertas e notificações
- [ ] Relatórios automatizados por email
- [ ] Dashboard customizável por usuário
- [ ] Histórico de auditoria

### v1.2.0 (Próximos Meses)
- [ ] Integração com banco de dados em tempo real
- [ ] Multi-tenancy (múltiplos clientes)
- [ ] Análise preditiva com ML
- [ ] Aplicação mobile nativa

### v2.0.0 (Futuro)
- [ ] Microserviços
- [ ] Escalabilidade horizontal
- [ ] Blockchain para auditoria
- [ ] IA/ML avançado

---

## Como Contribuir com Mudanças

Veja [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes sobre como:
- Reportar bugs
- Sugerir melhorias
- Submeter Pull Requests

---

## Política de Versionamento

Este projeto segue [Semantic Versioning](https://semver.org/lang/pt-BR/):

- **MAJOR** (1.0.0): Mudanças incompatíveis na API
- **MINOR** (1.1.0): Novas funcionalidades compatíveis com versões anteriores
- **PATCH** (1.1.1): Correções de bugs

---

## Suporte a Versões

| Versão | Status | Data de Lançamento | Fim de Vida |
|--------|--------|-------------------|-------------|
| 1.0.x  | ✅ Estável | 13/11/2024 | 13/11/2026 |
| 0.9.x  | ⚠️ Descontinuado | 01/11/2024 | 13/11/2024 |

---

**Última Atualização:** 13 de Novembro de 2024
