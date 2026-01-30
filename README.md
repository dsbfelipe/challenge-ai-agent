# 🔍 Sistema de Busca Inteligente para E-commerce

Um sistema de busca semântica avançado que utiliza IA para encontrar produtos mesmo com erros de digitação, abreviações ou palavras similares. O sistema combina normalização de texto, correção ortográfica, busca vetorial e sugestão de alternativas usando modelos de linguagem.

## 🌟 Características

- **🧠 Busca Semântica**: Encontra produtos por significado, não apenas por palavras exatas
- **✏️ Correção Ortográfica**: Corrige automaticamente erros de digitação
- **🔄 Normalização de Texto**: Remove acentos e padroniza consultas
- **💡 Sugestões Inteligentes**: Usa IA (Groq) para sugerir alternativas quando nenhum produto é encontrado
- **⚡ Alta Performance**: Busca vetorial com FAISS para respostas rápidas
- **🌐 Multilíngue**: Suporte para português e outros idiomas

## 📋 Pré-requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)
- Conta gratuita na Groq (para sugestões com IA)

## 🚀 Instalação

### 1. Clone o repositório
```bash
git clone <seu-repositorio>
cd challenge-ai-agent
```

### 2. Crie um ambiente virtual
```bash
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

Ou instale manualmente:
```bash
pip install sentence-transformers==5.2.2
pip install faiss-cpu==1.13.2
pip install RapidFuzz==3.14.3
pip install Unidecode==1.4.0
pip install groq==1.0.0
```

### 4. **IMPORTANTE**: Crie os índices antes de usar

⚠️ **Este passo é obrigatório antes de rodar a aplicação pela primeira vez!**

```bash
# Criar o índice vetorial FAISS
python3 -m tools.indexer
```

Estes comandos irão:
- Processar todos os produtos do catálogo
- Gerar embeddings vetoriais com o modelo multilíngue
- Criar o índice FAISS em `vectorstore/index.faiss`
- Criar o vocabulário em `vectorstore/grammar.json`
- Criar mapeamento de IDs em `vectorstore/product_ids.json`

### 5. Configure a API Key da Groq (Opcional, mas recomendado)

Para usar o recurso de sugestões inteligentes:

1. Crie uma conta gratuita em: https://console.groq.com/
2. Gere uma API Key em: https://console.groq.com/keys
3. Configure a variável de ambiente:

```bash
export GROQ_API_KEY='sua-chave-aqui'
```

Para tornar permanente, adicione ao seu `~/.bashrc` ou `~/.zshrc`:
```bash
echo 'export GROQ_API_KEY="sua-chave-aqui"' >> ~/.bashrc
source ~/.bashrc
```

### 6. Pronto! Execute a aplicação

```bash
python3 main.py
```

## 📁 Estrutura do Projeto

```
challenge-ai-agent/
│
├── main.py                 # Aplicação principal (interface CLI)
│
├── agent/
│   ├── agent.py            # Orquestrador da busca
│   └── prompt.py           # Prompts do sistema
│
├── data/
│   └── products.py         # Catálogo de produtos (50+ produtos)
│
├── tools/
│   ├── normalize.py        # Normalização de texto
│   ├── spellcheck.py       # Correção ortográfica
│   ├── semantic_search.py  # Busca vetorial com FAISS
│   ├── suggest_alternatives.py  # Sugestões com IA (Groq)
│   ├── build_index.py      # 🔧 Script para criar índice FAISS (rodar antes!)
│   └── build_grammar.py    # 🔧 Script para criar vocabulário (rodar antes!)
│
└── vectorstore/            # ⚠️ Criado pelos scripts de indexação
    ├── index.faiss         # Índice vetorial dos produtos (gerado)
    ├── product_ids.json    # Mapeamento de IDs (gerado)
    └── grammar.json        # Vocabulário para correção (gerado)
```

## 💻 Como Usar

### Modo Interativo

Execute a aplicação principal:

```bash
python main.py
```

Você verá uma interface interativa:

```
Busca inteligente (digite 'exit' para sair)
Buscar: notebook
```

Digite suas consultas e pressione Enter. Para sair, digite `exit`.

### Exemplos de Uso

#### 1. Busca Normal
```
Buscar: notebook
```
**Resultado**: Lista notebooks disponíveis com scores de relevância

#### 2. Busca com Erro de Digitação
```
Buscar: notbok
```
**Resultado**: Sistema corrige automaticamente e retorna notebooks

#### 3. Busca Semântica
```
Buscar: computador portátil
```
**Resultado**: Encontra equipamentos relacionados a informática

#### 4. Produto Não Encontrado ou gramática excessivamente errada (com API configurada)
```
Buscar: nobbk
```
**Resultado**:
```json
{
  "results": [],
  "alternative_suggestion": "notebook"
}
```

## 🔧 Como Funciona

### Pipeline de Busca

1. **Normalização** (`normalize.py`)
   - Converte para minúsculas
   - Remove acentos (café → cafe)
   - Remove espaços extras

2. **Correção Ortográfica** (`spellcheck.py`)
   - Compara cada palavra com vocabulário conhecido
   - Usa fuzzy matching (85% de similaridade)
   - Corrige erros de digitação

3. **Busca Semântica** (`semantic_search.py`)
   - Codifica a consulta em vetor usando modelo multilíngue
   - Busca no índice FAISS (k=5 resultados)
   - Filtra por score mínimo (0.5)
   - Retorna produtos mais relevantes

4. **Sugestão de Alternativas** (`suggest_alternatives.py`)
   - **Ativado apenas quando nenhum resultado é encontrado**
   - Usa modelo Llama 3.3 70B da Groq
   - Sugere consultas alternativas mais específicas
   - Fallback: retorna consulta original se API não configurada

## 🛠️ Scripts Auxiliares

### Recriar o Índice Vetorial

Se adicionar novos produtos ao catálogo:

```bash
python3 -m tools.indexer
```

Este script:
- Lê todos os produtos de `data/products.py`
- Gera embeddings vetoriais
- Cria o índice FAISS em `vectorstore/index.faiss`

### Recriar o Vocabulário

Para atualizar a base de correção ortográfica:

```bash
python3 -m tools.indexer
```

Este script:
- Extrai todas as palavras únicas dos produtos
- Gera frequências
- Salva em `vectorstore/grammar.json`

## 📊 Catálogo de Produtos

O sistema inclui **50+ produtos** em categorias:

- 📱 **Celulares**: Samsung, Motorola, Xiaomi
- 💻 **Informática**: Notebooks Dell, Lenovo, Acer
- 🖱️ **Periféricos**: Mouses, teclados, webcams
- 🎮 **Games**: Consoles, jogos, acessórios
- 📺 **Eletrônicos**: TVs, monitores, tablets
- 🎧 **Áudio**: Fones, caixas de som
- 🔌 **Acessórios**: Cabos, carregadores, hubs
- 🏠 **Casa Inteligente**: Lâmpadas, assistentes

## 🔑 Configuração de API Keys

### Groq API (Recomendado - Gratuito)

**Por que Groq?**
- ✅ Cota gratuita generosa
- ⚡ Extremamente rápido
- 🆓 Não requer cartão de crédito
- 🚀 Modelo Llama 3.3 70B de alta qualidade

**Como configurar:**
```bash
# Obtenha sua chave em: https://console.groq.com/keys
export GROQ_API_KEY='gsk_...'
```

### Variáveis de Ambiente Opcionais

```bash
# Para cache do HuggingFace (recomendado para produção)
export HF_TOKEN='seu_token_huggingface'
```

## 🧪 Testando o Sistema

### Teste 1: Busca Exata
```bash
echo "notebook" | python main.py
```

### Teste 2: Busca com Erro
```bash
echo "notbok barato" | python main.py
```

### Teste 3: Busca Semântica
```bash
echo "computador portátil" | python main.py
```

### Teste 4: Produto Inexistente
```bash
echo "nobbk" | python main.py
```

## 🔄 Atualizando o Catálogo

1. Edite `data/products.py` e adicione produtos:
```python
{
    "id": 99,
    "name": "Novo Produto",
    "category": "Categoria",
    "brand": "Marca",
    "description": "Descrição do produto"
}
```

2. Recrie os índices:
```bash
python3 -m tools.indexer
```

3. Teste:
```bash
python3 main.py
```
