# 📚 Biblioteca Universitária - Sistema de Gestão (Full Stack)

Sistema moderno para gerenciamento de acervo bibliotecário. O projeto integra uma API REST robusta em **Django Rest Framework** com um Frontend **SPA (Single Page Application)** responsivo, focado em experiência do usuário e automação de processos.

## 📂 Estrutura de Diretórios

├── biblioteca_config/      # Settings e URLConf principal
├── core/                   # Aplicação Django
│   ├── models.py           # Regras de Negócio (Property @status)
│   ├── serializers.py      # Serialização e validação
│   └── views.py            # ViewSets
├── media/                  # Uploads de imagens (GitIgnore recomendado)
├── index.html              # Frontend SPA
├── popular_banco.py        # Script de Seed/Povoamento
└── manage.py               # Utilitário CLI

## 🚀 Funcionalidades

### Backend (API)
* **Gestão Inteligente de Autores:** Cadastro automático de autores ("Upsert") via nome durante a criação do livro, eliminando a necessidade de gerenciar IDs manualmente.
* **Status Dinâmico:** O campo `status` ("Disponível" ou "Emprestado") é calculado automaticamente com base na quantidade de itens disponíveis em estoque, sem redundância no banco de dados.
* **Upload de Capas:** Suporte completo para upload e armazenamento de imagens via `ImageField`.
* **CRUD Completo:** Endpoints para Livros, Autores e Pedidos.
* **Povoamento Automático:** Script dedicado para popular o banco com 100 livros reais para testes imediatos.

### Frontend (Interface)
* **Dashboard SPA:** Navegação fluida entre listagem e detalhes sem recarregamento.
* **Visualização de Status:** Badges coloridas indicando disponibilidade imediata na listagem.
* **Nomenclatura Amigável:** Exibição de "Disponíveis" ao invés de "Estoque" técnico.
* **Filtros e Ordenação:** Busca em tempo real e ordenação por título, autor ou disponibilidade.
* **Modais Interativos:** Formulários de cadastro e pedidos em modais sobrepostos.
* **Autocomplete:** Sugestão de autores existentes no banco durante o cadastro.

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python 3, Django 5, Django Rest Framework (DRF), Pillow.
* **Banco de Dados:** SQLite 3 (Padrão, portável).
* **Frontend:** HTML5 Semântico, CSS3 (Grid/Flexbox, Glassmorphism), JavaScript Vanilla (ES6+).

## ⚙️ Pré-requisitos

* Python 3.8+
* Pip (Gerenciador de pacotes)

## 📦 Guia de Instalação

### 1. Clone e Prepare o Ambiente
```bash
git clone [https://github.com/seu-usuario/biblioteca-universitaria.git](https://github.com/seu-usuario/biblioteca-universitaria.git)
cd biblioteca-universitaria

# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 2. Instale as Dependências
```bash
pip install django djangorestframework django-cors-headers Pillow
```

### 3. Migração do Banco de Dados
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. (Opcional) Povoar com Dados de Teste
Gere 100 livros automaticamente (Clássicos, Best-sellers, Técnicos) executando o script na raiz do projeto:

```bash
python popular_banco.py
```

### 5. Execute o Servidor
```bash
python manage.py runserver
```

Acesse a aplicação em: `http://127.0.0.1:8000/` (Abra o arquivo `index.html` no navegador se não estiver servindo o estático via Django Templates).

## 🔗 Documentação da API
Endpoints Principais

| **Método** | **Endpoint** |	**Descrição** |
| ---------- | ------------ | ------------- |
|  GET  | `/api/livros/ ` | Lista todos os livros com campo status calculado.      |
|  POST | `/api/livros/`  |	Cria livro (Multipart/Form-data para imagem).          |
|  GET  |	`/api/autores/ `|	Lista autores (usado no autocomplete).                 |
|  POST | `/api/pedidos/` |	Registra um pedido de livro.                           |

Exemplo de Objeto Livro (JSON):

{
    "id": 1,
    "titulo": "Dom Casmurro",
    "autor_detalhes": { "id": 5, "nome": "Machado de Assis" },
    "estoque": 3,
    "status": "Disponível",  // Campo calculado (Read-Only)
    "capa_do_livro": "[http://127.0.0.1:8000/media/capas/dom_casmurro.jpg](http://127.0.0.1:8000/media/capas/dom_casmurro.jpg)",
    "genero": "Romance,Clássico"
}
