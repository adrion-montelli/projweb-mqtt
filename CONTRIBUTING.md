# Contribuindo para o Dashboard de Leituras

Obrigado por estar interessado em contribuir! 🎉

Este documento fornece diretrizes e instruções para contribuir com o projeto.

## 📋 Código de Conduta

- Seja respeitoso com outros colaboradores
- Forneça feedback construtivo
- Respeite a diversidade de opiniões
- Mantenha discussões profissionais e técnicas

## 🚀 Como Começar

### 1. Fork o Repositório

Clique em "Fork" no canto superior direito do repositório.

### 2. Clone seu Fork

```bash
git clone https://github.com/SEU-USUARIO/projweb-mqtt.git
cd projweb-mqtt
```

### 3. Criar uma Branch

```bash
git checkout -b feature/minha-feature
# ou para bug fix
git checkout -b fix/meu-bug
```

**Convenção de nomes:**
- `feature/nome-descritivo` - Para novas funcionalidades
- `fix/nome-descritivo` - Para correções de bugs
- `docs/nome-descritivo` - Para documentação
- `refactor/nome-descritivo` - Para refatoração

### 4. Configurar Ambiente de Desenvolvimento

```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Criar arquivo .env
cp .env.example .env

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser
```

### 5. Fazer Mudanças

- Edite os arquivos necessários
- Siga as convenções de código (ver seção abaixo)
- Escreva testes para novas funcionalidades
- Atualize documentação se necessário

### 6. Testar Mudanças

```bash
# Executar servidor local
python manage.py runserver

# Executar testes
python manage.py test

# Verificar qualidade do código
pylint leituras/
flake8 leituras/
```

### 7. Commit e Push

```bash
# Staged das mudanças
git add .

# Commit com mensagem descritiva
git commit -m "feat: adicionar novo gráfico de consumo"

# Push para seu fork
git push origin feature/minha-feature
```

### 8. Abrir Pull Request

1. Vá para seu fork no GitHub
2. Clique em "New Pull Request"
3. Selecione sua branch
4. Preencha a descrição do PR seguindo o template
5. Clique em "Create Pull Request"

---

## 💻 Convenções de Código

### Python (Backend)

**PEP 8 Compliant:**

```python
# ❌ Ruim
def func(x):return x*2

# ✅ Bom
def calculate_double(value):
    """Calcula o dobro de um valor."""
    return value * 2


# ❌ Ruim
class MyClass:
    def __init__(self):
        self.some_property = None

# ✅ Bom
class TemperatureSensor:
    """Modelo para sensor de temperatura."""
    
    def __init__(self, name: str):
        """Inicializar sensor."""
        self.name = name
        self.temperature: float = 0.0
```

**Imports:**

```python
# Ordem: Standard Library, Third-party, Local
import os
from datetime import datetime

from django.db import models
from django.utils import timezone

from leituras.models import Temperatura
```

**Docstrings:**

```python
def fetch_temperature_data(sensor_id: int, days: int = 7) -> dict:
    """
    Buscar dados de temperatura de um sensor.
    
    Args:
        sensor_id: ID do sensor
        days: Número de dias para retornar (padrão: 7)
        
    Returns:
        Dicionário com dados de temperatura formatados
        
    Raises:
        ValueError: Se sensor_id for inválido
        
    Example:
        >>> data = fetch_temperature_data(1, days=30)
        >>> print(data['average_temp'])
        25.5
    """
    pass
```

### HTML/Templates Django

```django-html
{# ❌ Ruim - sem espaço e indentação inconsistente #}
<div class="card">
    <h5>{{titulo}}</h5>
{%if condicao%}<p>Texto</p>{%endif%}
</div>

{# ✅ Bom - bem formatado #}
<div class="card">
    <h5>{{ titulo }}</h5>
    
    {% if condicao %}
        <p>Texto</p>
    {% endif %}
</div>
```

### CSS

```css
/* ❌ Ruim */
.my-class{color:red;margin:10px;padding:5px;}

/* ✅ Bom */
.my-class {
    color: red;
    margin: 10px;
    padding: 5px;
}

/* Usar variáveis e comentários */
:root {
    --primary-color: #0d6efd;
    --spacing-unit: 1rem;
}

/* Seção de componentes */
.card {
    background-color: var(--primary-color);
}
```

### JavaScript

```javascript
// ❌ Ruim
var x = 5;
const getData = async () => fetch('/api/data').then(r => r.json());

// ✅ Bom
const VALUE = 5;

async function fetchChartData() {
    try {
        const response = await fetch('/api/chart-data/');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Erro ao buscar dados:', error);
        throw error;
    }
}
```

---

## 📝 Tipos de Contribuição

### 🐛 Reportar Bugs

**Template de Issue:**

```markdown
## Descrição
Breve descrição do problema.

## Passos para Reproduzir
1. Ir para...
2. Clicar em...
3. Ver erro

## Comportamento Esperado
O que deveria acontecer.

## Comportamento Atual
O que está acontecendo.

## Informações do Sistema
- SO: Windows 10 / macOS / Ubuntu
- Navegador: Chrome, Firefox
- Versão Python: 3.11
- Versão Django: 4.2.7

## Screenshots/Logs
Se aplicável, adicione capturas de tela ou logs.
```

### ✨ Sugerir Melhorias

**Template:**

```markdown
## Descrição da Melhoria
Explicar brevemente a ideia.

## Justificativa
Por que isso seria útil?

## Exemplo de Implementação (Opcional)
Como você visualiza isso funcionando?

## Alternativas Consideradas
Outras formas de resolver?
```

### 📚 Melhorar Documentação

- Corrigir typos
- Adicionar exemplos
- Melhorar clareza
- Atualizar screenshots

### ♻️ Refatoração

- Melhorar qualidade do código
- Aumentar performance
- Reduzir complexidade
- Remover código duplicado

---

## 🧪 Testes

Toda nova funcionalidade deve ter testes.

```python
# tests/test_models.py
from django.test import TestCase
from leituras.models import Temperatura

class TemperaturaModelTest(TestCase):
    def setUp(self):
        self.temp = Temperatura.objects.create(
            id_cliente='CLIENTE_001',
            id_equipamento='EQUIP_001',
            temperatura=25.5
        )
    
    def test_criacao_temperatura(self):
        """Teste de criação de registro de temperatura."""
        self.assertEqual(self.temp.id_cliente, 'CLIENTE_001')
        self.assertEqual(self.temp.temperatura, 25.5)
    
    def test_temperatura_str(self):
        """Teste da representação em string."""
        self.assertEqual(str(self.temp), 'Temperatura: 25.5°C')
```

### Executar Testes

```bash
# Rodar todos os testes
python manage.py test

# Rodar teste específico
python manage.py test leituras.tests.TemperaturaModelTest

# Com cobertura
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

---

## 📋 Checklist Antes de Submeter PR

- [ ] Code segue PEP 8 / convenções do projeto
- [ ] Testes foram adicionados/atualizados
- [ ] Documentação foi atualizada
- [ ] Sem conflitos com branch principal
- [ ] Commits têm mensagens descritivas
- [ ] Nenhum arquivo sensível foi adicionado
- [ ] Testado localmente em múltiplos navegadores (se frontend)

---

## 🔄 Processo de Review

1. **Revisão Inicial**: Verificamos se segue as convenções
2. **Testes**: Executamos a suite de testes
3. **Review Técnico**: Analisamos o código
4. **Feedback**: Comentários e sugestões
5. **Ajustes**: Você faz os ajustes necessários
6. **Merge**: Mesclamos na branch principal

---

## 🎯 Prioridades de Contribuição

**Alto Prioridade:**
- Correções de bugs críticos
- Melhorias de segurança
- Documentação importante

**Média Prioridade:**
- Novas funcionalidades
- Refatoração
- Testes

**Baixa Prioridade:**
- Melhorias cosméticas
- Reorganização de comentários

---

## 📞 Dúvidas?

- Abra uma issue com tag `question`
- Deixe comentário no PR
- Verifique a documentação existente

---

## 🙏 Agradecimentos

Obrigado por contribuir com o projeto! Sua ajuda é importante para mantê-lo melhor.

---

**Versionamento:** v1.0.0  
**Última Atualização:** Novembro 2024
