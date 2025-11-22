# 📚 Sistema de Gestão de Biblioteca Universitária (SGBU)

Uma solução **Full Stack** completa para gerenciamento de acervos acadêmicos. O sistema combina uma API RESTful robusta construída com **Django** e uma interface Frontend **SPA (Single Page Application)** moderna, focado em agilidade, controle de dados e experiência do usuário.

## 📂 Estrutura de Diretórios
```
├── biblioteca_config/      # Configurações do Django (Settings, URLConf)
├── core/                   # App Principal
│   ├── models.py           # Modelos (Livro, Aluno, Emprestimo, Autor)
│   ├── serializers.py      # Serialização e Validação de Dados
│   └── views.py            # Lógica de Negócio (ViewSets)
├── media/capas/            # Diretório de armazenamento de uploads
├── index.html              # Frontend Unificado (SPA)
├── popular_banco.py        # Script de Seed/Povoamento de Dados
└── manage.py
```

## 🚀 Funcionalidades do Sistema

### 🖥️ Interface & Experiência do Usuário (Frontend)
* **Navegação em Abas:** Organização lógica em três painéis:
    1.  **Acervo:** Gestão completa dos livros.
    2.  **Emprestados:** Monitoramento em tempo real de livros com alunos.
    3.  **Histórico:** Log permanente de todas as movimentações (entradas e saídas).
* **Busca em Tempo Real:** Barra de pesquisa inteligente que filtra livros por **Título**, **Autor** ou **Gênero** instantaneamente, sem recarregar a página.
* **Visualização de Detalhes:** Clique em qualquer livro para ver uma ficha técnica completa, incluindo a **Capa do Livro**, sinopse, estoque e metadados.
* **Gestão de Imagens:** Suporte para upload e visualização de capas de livros (`.jpg`, `.png`).

### ⚙️ Regras de Negócio (Backend)
* **Fluxo de Empréstimo:**
    * Validação automática de estoque.
    * Identificação flexível de alunos por **CPF** ou **Nome**.
    * Baixa automática no estoque ao emprestar.
* **Fluxo de Devolução:**
    * Restaurar o estoque automaticamente.
    * O registro não é excluído, mas arquivado com a data de devolução preenchida (Histórico).
* **Gestão de Entidades:**
    * **Livros:** CRUD completo com exclusão em massa (Bulk Delete) via checkboxes.
    * **Autores:** Cadastro inteligente ("Upsert") — se o autor já existe, o sistema vincula; se não, cria um novo.
    * **Alunos:** Base de dados completa com CPF, Nome, Curso e Turma.
* **Status Dinâmico:** O sistema calcula automaticamente se um livro está "Disponível" (Verde) ou "Alugado" (Vermelho) com base no estoque atual.

## 🛠️ Tecnologias Utilizadas

### Backend
* **Linguagem:** Python 3.10+
* **Framework:** Django 5
* **API:** Django Rest Framework (DRF)
* **Banco de Dados:** SQLite 3
* **Processamento de Imagem:** Pillow

### Frontend
* **Estrutura:** HTML5 Semântico
* **Estilo:** CSS3 (Flexbox, Grid, Glassmorphism UI)
* **Lógica:** JavaScript (ES6+, Fetch API, FormData)

## 📦 Guia de Instalação

### 1. Clone o Repositório
```bash
git clone [https://github.com/paulorpb/bibliotecaDjango.git](https://github.com/paulorpb/bibliotecaDjango.git)
cd bibliotecaDjango
```

### 2. Configure o Ambiente Virtual 

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux/Mac
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as Dependências
```bash
pip install django djangorestframework django-cors-headers Pillow
```

### 4. Prepare o Banco de Dados
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. (Opcional) Popule com Dados de Teste
Gere automaticamente 100 Livros e 100 Alunos fictícios para testar todas as funcionalidades imediatamente:

```bash
python popular_banco.py
```

### 6. Execute o Projeto
```bash
python manage.py runserver
```

Acesse a aplicação em: `http://127.0.0.1:8000/` (Abra o arquivo `index.html` no navegador se não estiver servindo o estático via Django Templates).

## 📖 Manual de Uso Rápido
**Gerenciar Livros**
- **Cadastrar:** Clique em "Novo Livro". Preencha os dados e anexe uma imagem de capa. O autor será buscado ou criado automaticamente.
- **Excluir:** Na tabela do Acervo, selecione as caixas de seleção (checkbox) à esquerda dos livros desejados e clique em "Excluir Selecionados".
- **Detalhes:** Clique sobre o texto de qualquer linha da tabela para abrir a visualização detalhada.

**Realizar Empréstimo**
1. Na aba **Acervo**, clique em "Emprestar".
2. Escolha um livro disponível na lista.
3. Digite o **CPF** (ou Nome) do aluno.
4. Confirme. O livro sairá do estoque e aparecerá na aba Emprestados.

**Realizar Devolução**
1. Vá até a aba **Emprestados**.
2. Localize o empréstimo e clique no botão "Devolver" na linha correspondente.
3. Confirme a ação. O livro voltará ao estoque e o registro moverá para a aba Histórico.

## 🔗 Endpoints da API
A aplicação expõe uma API RESTful completa em `/api/`.

| **Método** | **Endpoint** |	**Descrição** |
| ---------- | ------------ | ------------- |
|  GET  | `/api/livros/ ` | Lista livros com status e URLs de imagem.    |
|  POST | `/api/livros/`  |	Cria livro (Multipart Form Data).          |
|  GET  |	`/api/alunos/ `|	Lista alunos cadastrados.                |
|  POST | `/api/emprestimos/` |	Registra saída de livro.                           |
|  POST | `/api/emprestimos/devolver` |	Ação personalizada para dar baixa em empréstimos. |
