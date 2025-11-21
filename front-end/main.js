const API_URL = "http://127.0.0.1:8000/api/livros/";

// 1. Função para Listar Livros (READ)
async function loadBooks() {
  const container = document.getElementById("bookContainer");
  container.innerHTML = "<p>Carregando...</p>";

  try {
    const response = await fetch(API_URL);
    const books = await response.json();

    container.innerHTML = "";

    if (books.length === 0) {
      container.innerHTML = "<p>Nenhum livro cadastrado.</p>";
      return;
    }

    books.forEach((book) => {
      const div = document.createElement("div");
      div.className = "book-item";
      // Imagem placeholder se não houver URL
      const imgUrl =
        book.capa_do_livro ||
        "https://via.placeholder.com/300x200?text=Sem+Capa";

      div.innerHTML = `
                    <img src="${imgUrl}" class="book-img" alt="Capa">
                    <div class="book-info">
                        <div class="book-title">${book.titulo}</div>
                        <div class="book-meta">Gênero: <span class="badge">${
                          book.genero
                        }</span></div>
                        <div class="book-meta">Estoque: ${
                          book.estoque
                        } un.</div>
                        <div class="book-meta" style="font-size: 0.8rem; color: #888; margin-top: 5px;">
                            ${book.descricao.substring(0, 60)}...
                        </div>
                        <button class="delete-btn" onclick="deleteBook(${
                          book.id
                        })">Excluir</button>
                    </div>
                `;
      container.appendChild(div);
    });
  } catch (error) {
    console.error("Erro:", error);
    container.innerHTML =
      '<p style="color:red">Erro ao conectar com a API.</p>';
  }
}

// 2. Função para Criar Livro (CREATE)
document.getElementById("bookForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const data = {
    titulo: document.getElementById("titulo").value,
    autor: parseInt(document.getElementById("autor").value),
    genero: document.getElementById("genero").value,
    estoque: parseInt(document.getElementById("estoque").value),
    paginas: parseInt(document.getElementById("paginas").value),
    data_publicacao: document.getElementById("dataPublicacao").value,
    capa_do_livro: document.getElementById("capa").value,
    descricao: document.getElementById("descricao").value,
  };

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    if (response.ok) {
      alert("Livro cadastrado com sucesso!");
      document.getElementById("bookForm").reset();
      loadBooks();
    } else {
      const err = await response.json();
      alert("Erro ao cadastrar: " + JSON.stringify(err));
    }
  } catch (error) {
    alert("Erro de conexão");
  }
});

// 3. Função para Deletar Livro (DELETE)
async function deleteBook(id) {
  if (!confirm("Tem certeza que deseja excluir este livro?")) return;

  try {
    const response = await fetch(`${API_URL}${id}/`, {
      method: "DELETE",
    });
    if (response.ok) {
      loadBooks();
    } else {
      alert("Erro ao excluir");
    }
  } catch (error) {
    alert("Erro de conexão");
  }
}

// Carregar ao iniciar
loadBooks();
