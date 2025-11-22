const API_BASE = "http://127.0.0.1:8000/api/";
let booksCache = [];

// --- NAVEGAÇÃO (TABS) ---
function switchTab(tabId) {
  // UI Tabs
  document
    .querySelectorAll(".tab-btn")
    .forEach((b) => b.classList.remove("active"));
  document
    .querySelectorAll(".tab-content")
    .forEach((c) => c.classList.remove("active"));

  // Ativar atual
  document
    .querySelector(`button[onclick="switchTab('${tabId}')"]`)
    .classList.add("active");
  document.getElementById(tabId).classList.add("active");

  // Recarregar dados específicos
  if (tabId === "acervo") loadBooks();
  if (tabId === "emprestados") loadLoans();
  if (tabId === "historico") loadLoans();
}

// --- CARREGAMENTO DE DADOS ---

async function loadBooks() {
  const res = await fetch(API_BASE + "livros/");
  booksCache = await res.json();

  // Popula Tabela Acervo
  const tbody = document.querySelector("#tableAcervo tbody");
  tbody.innerHTML = booksCache
    .map(
      (b) => `
            <tr>
                <td>${b.titulo}</td>
                <td>${b.autor_detalhes.nome}</td>
                <td>${b.estoque}</td>
                <td><span class="badge ${
                  b.status === "Disponível" ? "disp" : "alug"
                }">${b.status}</span></td>
            </tr>
        `
    )
    .join("");

  // Popula Selects (Empréstimo e Devolução)
  const options = booksCache
    .map((b) => `<option value="${b.id}">${b.titulo}</option>`)
    .join("");
  document.getElementById("loanBookSelect").innerHTML = options;
  document.getElementById("returnBookSelect").innerHTML = options;
}

async function loadLoans() {
  const res = await fetch(API_BASE + "emprestimos/");
  const loans = await res.json();

  // Filtrar Ativos vs Histórico
  const ativos = loans.filter((l) => l.data_devolucao === null);
  const historico = loans.filter((l) => l.data_devolucao !== null);

  // Renderizar Ativos
  document.querySelector("#tableAtivos tbody").innerHTML = ativos
    .map(
      (l) => `
            <tr>
                <td>${l.aluno_detalhes.nome} <small>(${
        l.aluno_detalhes.cpf
      })</small></td>
                <td>${l.livro_titulo}</td>
                <td>${new Date(l.data_emprestimo).toLocaleDateString()}</td>
                <td><button class="btn-warning" style="padding:5px 10px; font-size:0.8rem" onclick="quickReturn('${
                  l.aluno_detalhes.cpf
                }', ${l.livro})">Devolver</button></td>
            </tr>
        `
    )
    .join("");

  // Renderizar Histórico
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
}

// --- ACTIONS (POST) ---

// 1. Emprestar
document.getElementById("loanForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const formData = new FormData(e.target);
  const data = Object.fromEntries(formData.entries());

  if (!data.aluno_cpf && !data.aluno_nome) {
    alert("Preencha CPF ou Nome!");
    return;
  }

  try {
    const res = await fetch(API_BASE + "emprestimos/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    if (res.ok) {
      alert("Empréstimo realizado!");
      closeModal("loanModal");
      e.target.reset();
      switchTab("emprestados"); // Vai para a aba de emprestados
    } else {
      const err = await res.json();
      alert("Erro: " + JSON.stringify(err)); // Provavelmente "Aluno não encontrado"
    }
  } catch (e) {
    alert("Erro de conexão");
  }
});

// 2. Devolver (Formulário)
document.getElementById("returnForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const formData = new FormData(e.target);
  const data = Object.fromEntries(formData.entries());
  await executeReturn(data);
});

// Devolver (Atalho botão tabela)
async function quickReturn(cpf, livroId) {
  if (!confirm("Confirmar devolução rápida?")) return;
  await executeReturn({ cpf: cpf, livro_id: livroId });
}

async function executeReturn(data) {
  try {
    const res = await fetch(API_BASE + "emprestimos/devolver/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    if (res.ok) {
      alert("Livro devolvido com sucesso!");
      closeModal("returnModal");
      document.getElementById("returnForm").reset();
      loadLoans(); // Atualiza tabelas
    } else {
      const err = await res.json();
      alert("Erro: " + (err.erro || JSON.stringify(err)));
    }
  } catch (e) {
    alert("Erro de conexão");
  }
}

// 3. Cadastrar Livro (Mantido simples)
document.getElementById("bookForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  // ... (Mesma lógica anterior para criar livro) ...
  const formData = new FormData(e.target);
  await fetch(API_BASE + "livros/", { method: "POST", body: formData });
  closeModal("bookModal");
  loadBooks();
});

// Filtro de Acervo
function filterBooks() {
  const term = document.getElementById("searchBook").value.toLowerCase();
  const rows = document.querySelectorAll("#tableAcervo tbody tr");
  rows.forEach((row) => {
    const txt = row.innerText.toLowerCase();
    row.style.display = txt.includes(term) ? "" : "none";
  });
}

// Utilitários Modal
window.openModal = (id) => (document.getElementById(id).style.display = "flex");
window.closeModal = (id) =>
  (document.getElementById(id).style.display = "none");

// Iniciar na aba Acervo
loadBooks();
