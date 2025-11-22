const API_BASE = "http://127.0.0.1:8000/api/";
const genresList = [
  "Ficção",
  "Romance",
  "Técnico",
  "História",
  "Sci-Fi",
  "Fantasia",
  "Biografia",
  "Terror",
];
let booksCache = [];

// --- INICIALIZAÇÃO ---
function init() {
  renderGenreCheckboxes();
  loadBooks();
  loadAuthors();
  loadLoans();
}

// --- RENDERIZAÇÃO DE UI AUXILIAR ---
function renderGenreCheckboxes() {
  const container = document.getElementById("genreOptions");
  container.innerHTML = genresList
    .map(
      (g) => `
            <label class="checkbox-label">
                <input type="checkbox" name="generos" value="${g}"> ${g}
            </label>
        `
    )
    .join("");
}

// --- NAVEGAÇÃO E ABAS ---
function switchTab(tabId) {
  // Reseta Abas
  document
    .querySelectorAll(".tab-btn")
    .forEach((b) => b.classList.remove("active"));
  document
    .querySelectorAll(".tab-content")
    .forEach((c) => c.classList.remove("active"));

  // Ativa Selecionada
  document
    .querySelector(`button[onclick="switchTab('${tabId}')"]`)
    .classList.add("active");
  document.getElementById(tabId).classList.add("active");

  // Recarrega dados relevantes
  if (tabId === "acervo") loadBooks();
  if (tabId === "emprestados" || tabId === "historico") loadLoans();
}

// --- VIEW DE DETALHES ---
function showDetail(id) {
  const book = booksCache.find((b) => b.id == id);
  if (!book) return;

  // Oculta Abas e Mostra Detalhes
  document.getElementById("tabsContainer").classList.add("hidden");
  document.getElementById("detailView").style.display = "block";

  // Popula Dados
  document.getElementById("detTitle").textContent = book.titulo;
  document.getElementById("detAuthor").textContent = book.autor_detalhes.nome;
  document.getElementById("detStock").textContent = book.estoque;
  document.getElementById("detPages").textContent = book.paginas;
  document.getElementById("detDate").textContent = new Date(
    book.data_publicacao
  ).toLocaleDateString("pt-BR");
  document.getElementById("detDesc").textContent = book.descricao;

  // Status com cor
  const statusEl = document.getElementById("detStatus");
  statusEl.textContent = book.status;
  statusEl.className = `badge ${
    book.status === "Disponível" ? "disp" : "alug"
  }`;

  // Imagem
  document.getElementById("detImg").src =
    book.capa_do_livro || "https://via.placeholder.com/300x450?text=Sem+Capa";

  // Gêneros
  document.getElementById("detGenres").innerHTML = book.genero
    .split(",")
    .map((g) => `<span class="tag-genre">${g}</span>`)
    .join("");
}

function closeDetails() {
  document.getElementById("detailView").style.display = "none";
  document.getElementById("tabsContainer").classList.remove("hidden");
}

// --- RENDERIZAR TABELA DO ACERVO ---
function renderAcervoTable(data) {
  const tbody = document.querySelector("#tableAcervo tbody");
  tbody.innerHTML = "";

  if (data.length === 0) {
    tbody.innerHTML =
      '<tr><td colspan="6" style="text-align:center; padding:20px">Nenhum livro encontrado.</td></tr>';
    return;
  }

  data.forEach((book) => {
    const tr = document.createElement("tr");
    const statusClass = book.status === "Disponível" ? "disp" : "alug";

    // IMPORTANTE: Checkbox tem stopPropagation para não abrir detalhes
    tr.innerHTML = `
                <td><input type="checkbox" class="book-check" value="${
                  book.id
                }" onclick="event.stopPropagation()"></td>
                <td class="clickable-row" onclick="showDetail(${book.id})">${
      book.titulo
    }</td>
                <td class="clickable-row" onclick="showDetail(${book.id})">${
      book.autor_detalhes.nome
    }</td>
                <td class="clickable-row" onclick="showDetail(${
                  book.id
                })">${book.genero.split(",").slice(0, 2).join(", ")}</td>
                <td class="clickable-row" onclick="showDetail(${
                  book.id
                })" style="text-align:center">${book.estoque}</td>
                <td class="clickable-row" onclick="showDetail(${
                  book.id
                })"><span class="badge ${statusClass}">${
      book.status
    }</span></td>
            `;
    tbody.appendChild(tr);
  });
}

// --- FILTRAGEM (BUSCA) ---
function filterBooks() {
  const term = document.getElementById("searchBook").value.toLowerCase();

  const filtered = booksCache.filter(
    (book) =>
      book.titulo.toLowerCase().includes(term) ||
      book.autor_detalhes.nome.toLowerCase().includes(term) ||
      book.genero.toLowerCase().includes(term)
  );

  renderAcervoTable(filtered);
}

// --- LÓGICA DE DADOS (CRUD) ---

// 1. Carregar Livros (Tabela Acervo)
async function loadBooks() {
  try {
    const res = await fetch(API_BASE + "livros/");
    booksCache = await res.json();

    // Renderiza tabela completa inicialmente
    renderAcervoTable(booksCache);

    // Popula selects
    populateSelects(booksCache);
  } catch (e) {
    console.error(e);
  }
}

// 2. Carregar Empréstimos (Tabelas Ativos e Histórico)
async function loadLoans() {
  try {
    const res = await fetch(API_BASE + "emprestimos/");
    const loans = await res.json();

    const ativos = loans.filter((l) => l.data_devolucao === null);
    const historico = loans.filter((l) => l.data_devolucao !== null);

    document.querySelector("#tableAtivos tbody").innerHTML = ativos
      .map(
        (l) => `
                <tr>
                    <td>${l.aluno_detalhes.nome} <br><small>${
          l.aluno_detalhes.cpf
        }</small></td>
                    <td>${l.livro_titulo}</td>
                    <td>${new Date(l.data_emprestimo).toLocaleDateString()}</td>
                    <td><button class="btn-warning" style="font-size:0.8rem; padding: 5px 10px;" onclick="quickReturn('${
                      l.aluno_detalhes.cpf
                    }', ${l.livro})">Devolver</button></td>
                </tr>
            `
      )
      .join("");

    document.querySelector("#tableHistorico tbody").innerHTML = historico
      .map(
        (l) => `
                <tr>
                    <td>${l.aluno_detalhes.nome}</td>
                    <td>${l.livro_titulo}</td>
                    <td>${new Date(l.data_emprestimo).toLocaleDateString()}</td>
                    <td><span class="badge dev">${new Date(
                      l.data_devolucao
                    ).toLocaleDateString()}</span></td>
                </tr>
            `
      )
      .join("");
  } catch (e) {
    console.error(e);
  }
}

// 3. Cadastrar Livro (Com FormData para Imagem e Gêneros)
document.getElementById("bookForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const formData = new FormData(e.target);

  // Coleta checkboxes de gênero manualmente para string separada por vírgula
  const genres = Array.from(
    document.querySelectorAll('input[name="generos"]:checked')
  )
    .map((cb) => cb.value)
    .join(",");
  formData.set("genero", genres); // Sobrescreve/Define no FormData

  try {
    // Nota: NÃO defina Content-Type header manualmente quando usar FormData, o browser faz isso.
    const res = await fetch(API_BASE + "livros/", {
      method: "POST",
      body: formData,
    });

    if (res.ok) {
      alert("Livro cadastrado!");
      closeModal("bookModal");
      e.target.reset();
      loadBooks();
    } else {
      alert("Erro ao cadastrar.");
    }
  } catch (e) {
    alert("Erro de conexão");
  }
});

// 4. Excluir Livros (Selecionados na Tabela)
async function deleteSelectedBooks() {
  const checked = Array.from(
    document.querySelectorAll(".book-check:checked")
  ).map((cb) => cb.value);
  if (checked.length === 0) {
    alert("Selecione ao menos um livro.");
    return;
  }

  if (!confirm(`Tem certeza que deseja excluir ${checked.length} livro(s)?`))
    return;

  for (let id of checked) {
    await fetch(`${API_BASE}livros/${id}/`, { method: "DELETE" });
  }
  alert("Livros excluídos.");
  document.getElementById("selectAll").checked = false;
  loadBooks();
}

// 5. Empréstimo e Devolução (Ações)
document
  .getElementById("loanForm")
  .addEventListener("submit", async (e) => handlePost(e, "emprestimos/"));
document
  .getElementById("returnForm")
  .addEventListener("submit", async (e) =>
    handlePost(e, "emprestimos/devolver/")
  );

async function handlePost(e, endpoint) {
  e.preventDefault();
  const data = Object.fromEntries(new FormData(e.target).entries());
  try {
    const res = await fetch(API_BASE + endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (res.ok) {
      alert("Operação realizada com sucesso!");
      e.target.closest(".modal-overlay").style.display = "none"; // Fecha modal
      e.target.reset();
      loadBooks();
      loadLoans();
    } else {
      const err = await res.json();
      alert("Erro: " + JSON.stringify(err));
    }
  } catch (e) {
    alert("Erro de conexão");
  }
}

async function quickReturn(cpf, livroId) {
  if (!confirm("Confirmar devolução imediata?")) return;
  try {
    const res = await fetch(API_BASE + "emprestimos/devolver/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ cpf: cpf, livro_id: livroId }),
    });
    if (res.ok) {
      alert("Devolvido!");
      loadBooks();
      loadLoans();
    } else {
      alert("Erro na devolução");
    }
  } catch (e) {
    alert("Erro de conexão");
  }
}

// --- UTILITÁRIOS ---
function populateSelects(books) {
  const opts = books
    .map((b) => `<option value="${b.id}">${b.titulo}</option>`)
    .join("");
  document.getElementById("returnBookSelect").innerHTML = opts;

  // Para empréstimo, apenas livros com estoque
  const avail = books.filter((b) => b.estoque > 0);
  document.getElementById("loanBookSelect").innerHTML = avail
    .map(
      (b) => `<option value="${b.id}">${b.titulo} (${b.estoque} disp.)</option>`
    )
    .join("");
}

async function loadAuthors() {
  const res = await fetch(API_BASE + "autores/");
  const authors = await res.json();
  document.getElementById("authorsList").innerHTML = authors
    .map((a) => `<option value="${a.nome}">`)
    .join("");
}

function toggleAll(source) {
  document
    .querySelectorAll(".book-check")
    .forEach((cb) => (cb.checked = source.checked));
}

window.openModal = (id) => (document.getElementById(id).style.display = "flex");
window.closeModal = (id) =>
  (document.getElementById(id).style.display = "none");
window.onclick = (e) => {
  if (e.target.classList.contains("modal-overlay"))
    e.target.style.display = "none";
};

// Iniciar
init();
