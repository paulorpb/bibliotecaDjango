const API_BASE = "http://127.0.0.1:8000/api/";
let booksData = [];

const genres = ["Ficção", "Romance", "Técnico", "História", "Sci-Fi"];

function init() {
  loadBooks();
  loadAuthors();
  renderGenreCheckboxes();
}

// --- MANIPULAÇÃO DA DOM AUXILIAR ---
function renderGenreCheckboxes() {
  document.getElementById("genreOptions").innerHTML = genres
    .map(
      (g) => `
            <label><input type="checkbox" value="${g}" name="generos"> ${g}</label>
        `
    )
    .join("");
}

window.openModal = (id) => (document.getElementById(id).style.display = "flex");
window.closeModal = (id) =>
  (document.getElementById(id).style.display = "none");
window.toggleAll = (source) => {
  document
    .querySelectorAll(".book-check")
    .forEach((cb) => (cb.checked = source.checked));
};

// --- API CALLS ---

// 1. Load Books (Com Checkboxes)
async function loadBooks() {
  const res = await fetch(API_BASE + "livros/");
  booksData = await res.json();
  renderTable(booksData);

  // Popula select do Empréstimo apenas com livros disponíveis
  const available = booksData.filter((b) => b.estoque > 0);
  document.getElementById("loanBookSelect").innerHTML = available
    .map(
      (b) => `<option value="${b.id}">${b.titulo} (${b.estoque} disp.)</option>`
    )
    .join("");
}

function renderTable(data) {
  const tbody = document.getElementById("bookTableBody");
  tbody.innerHTML = "";
  data.forEach((book) => {
    const tr = document.createElement("tr");
    const statusClass =
      book.status === "Disponível" ? "status-disponivel" : "status-alugado";

    // Checkbox na primeira célula
    // Click no TR abre detalhes, Click no Checkbox seleciona (stopPropagation)
    tr.innerHTML = `
                <td><input type="checkbox" class="book-check" value="${book.id}" onclick="event.stopPropagation()"></td>
                <td onclick="showDetail(${book.id})">${book.titulo}</td>
                <td onclick="showDetail(${book.id})">${book.autor_detalhes.nome}</td>
                <td onclick="showDetail(${book.id})">${book.genero}</td>
                <td onclick="showDetail(${book.id})" style="text-align:center">${book.estoque}</td>
                <td onclick="showDetail(${book.id})"><span class="status-badge ${statusClass}">${book.status}</span></td>
            `;
    tbody.appendChild(tr);
  });
}

// 2. Excluir Livros (Múltiplos)
async function deleteSelectedBooks() {
  const checked = Array.from(
    document.querySelectorAll(".book-check:checked")
  ).map((cb) => cb.value);

  if (checked.length === 0) {
    alert("Selecione pelo menos um livro na tabela para excluir.");
    return;
  }

  if (!confirm(`Tem certeza que deseja excluir ${checked.length} livro(s)?`))
    return;

  // Delete em loop (Para simplicidade, em prod seria um endpoint bulk)
  for (let id of checked) {
    await fetch(`${API_BASE}livros/${id}/`, { method: "DELETE" });
  }

  loadBooks();
  alert("Livros excluídos com sucesso!");
  document.getElementById("selectAll").checked = false;
}

// 3. Criar Empréstimo
document.getElementById("loanForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const formData = new FormData(e.target);
  const data = Object.fromEntries(formData.entries());

  // Validar se dados do aluno foram preenchidos (Exemplo simples)
  if (data.aluno_nome === "" && data.aluno_curso === "") {
    // Nota: O Backend aceita buscar só pelo CPF, mas o UX ideal pediria confirmação
    // Deixaremos passar, assumindo que o aluno já existe se o usuário não preencheu o resto
  }

  try {
    const res = await fetch(API_BASE + "emprestimos/", {
      // Note a mudança de rota
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    if (res.ok) {
      alert("Empréstimo registrado com sucesso!");
      closeModal("loanModal");
      e.target.reset();
      loadBooks(); // Atualiza estoque na tabela
    } else {
      const err = await res.json();
      alert("Erro: " + JSON.stringify(err));
    }
  } catch (error) {
    alert("Erro de conexão");
  }
});

// 4. Cadastro de Livro (Mantido do anterior, simplificado aqui)
async function loadAuthors() {
  /* ... Mesma lógica ... */
  const res = await fetch(API_BASE + "autores/");
  const authors = await res.json();
  document.getElementById("authorsList").innerHTML = authors
    .map((a) => `<option value="${a.nome}">`)
    .join("");
}

document.getElementById("bookForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const formData = new FormData(e.target);
  const checkedGenres = Array.from(
    document.querySelectorAll('input[name="generos"]:checked')
  )
    .map((cb) => cb.value)
    .join(",");
  formData.append("genero", checkedGenres);

  await fetch(API_BASE + "livros/", { method: "POST", body: formData });
  closeModal("bookModal");
  e.target.reset();
  loadBooks();
});

// Detalhes (SPA logic)
function showDetail(id) {
  const book = booksData.find((b) => b.id == id);
  document.getElementById("homeView").classList.add("hidden");
  document.getElementById("detailView").style.display = "block";
  document.getElementById("detTitle").textContent = book.titulo;
  document.getElementById("detAuthor").textContent = book.autor_detalhes.nome;
  document.getElementById("detStock").textContent = book.estoque;
  document.getElementById("detStatus").textContent = book.status;
  document.getElementById("detStatus").style.color =
    book.status === "Disponível" ? "green" : "red";
  document.getElementById("detDesc").textContent = book.descricao;
  document.getElementById("detImg").src =
    book.capa_do_livro || "https://via.placeholder.com/300x450";
}

function showHome() {
  document.getElementById("detailView").style.display = "none";
  document.getElementById("homeView").classList.remove("hidden");
}

function filterBooks() {
  const term = document.getElementById("searchInput").value.toLowerCase();
  const filtered = booksData.filter((b) =>
    b.titulo.toLowerCase().includes(term)
  );
  renderTable(filtered);
}

init();
