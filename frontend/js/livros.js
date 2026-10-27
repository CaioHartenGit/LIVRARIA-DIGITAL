const API_URL = "http://127.0.0.1:8000";

const usuarioLogado = JSON.parse(localStorage.getItem("usuario_livraria"));
if (!usuarioLogado) {
    window.location.href = "index.html";
}

let mapaProgresso = {};

document.addEventListener("DOMContentLoaded", () => {
    const userInfo = document.getElementById("user-info");
    userInfo.innerHTML = `Olá, <strong>${usuarioLogado.nome}</strong> <span class="role-tag">${usuarioLogado.tipo_usuario}</span>`;

    // Se não for admin, oculta o botão de cadastrar livro (ou exibe apenas para admin)
    const btnNovoLivro = document.getElementById("btn-novo-livro");
    if (usuarioLogado.tipo_usuario !== "admin") {
        btnNovoLivro.style.display = "none";
    }

    carregarAcervo();
});

function sair() {
    localStorage.removeItem("usuario_livraria");
    window.location.href = "index.html";
}

async function carregarProgressoUsuario() {
    mapaProgresso = {};
    try {
        const resp = await fetch(`${API_URL}/progresso/${usuarioLogado.id}/`);
        if (resp.ok) {
            const lista = await resp.json();
            lista.forEach((item) => {
                mapaProgresso[item.livro_id] = item;
            });
        }
    } catch (e) {
        // Usuário ainda não possui progresso registrado
    }
}

async function carregarAcervo() {
    document.getElementById("input-busca").value = "";
    await carregarProgressoUsuario();

    const grid = document.getElementById("books-grid");
    grid.innerHTML = "<p style='color: var(--text-muted);'>Carregando livros...</p>";

    try {
        const resp = await fetch(`${API_URL}/livros/`);
        const dados = await resp.json();

        if (!resp.ok || !Array.isArray(dados)) {
            grid.innerHTML = `<p style="color: var(--text-muted);">Nenhum livro cadastrado ainda.</p>`;
            return;
        }

        renderizarLivros(dados);
    } catch (erro) {
        grid.innerHTML = `<p style="color: var(--text-muted);">Nenhum livro cadastrado no momento.</p>`;
    }
}

async function buscarLivros() {
    const termo = document.getElementById("input-busca").value.trim();
    if (!termo) {
        return carregarAcervo();
    }

    const grid = document.getElementById("books-grid");
    try {
        const resp = await fetch(`${API_URL}/livros/titulo/${encodeURIComponent(termo)}`);
        const dados = await resp.json();

        if (!resp.ok) {
            grid.innerHTML = `<p style="color: var(--text-muted);">Nenhum livro encontrado com "${termo}".</p>`;
            return;
        }

        renderizarLivros(dados);
    } catch (erro) {
        grid.innerHTML = `<p style="color: var(--text-muted);">Erro ao buscar livros.</p>`;
    }
}

function filtrarPorTecla(event) {
    if (event.key === "Enter") {
        buscarLivros();
    }
}

function renderizarLivros(livros) {
    const grid = document.getElementById("books-grid");
    grid.innerHTML = "";

    livros.forEach((livro) => {
        const prog = mapaProgresso[livro.id];
        const paginaAtual = prog ? prog.pagina_atual : 0;
        const porcentagem = livro.total_paginas > 0
            ? Math.min(100, Math.round((paginaAtual / livro.total_paginas) * 100))
            : 0;
        const statusTexto = prog && prog.concluido
            ? "✅ Concluído"
            : prog
                ? `Lendo: pág. ${paginaAtual} de ${livro.total_paginas}`
                : `Não iniciado (${livro.total_paginas} págs)`;

        const botaoDeletar = usuarioLogado.tipo_usuario === "admin"
            ? `<button class="btn btn-danger" onclick="deletarLivro(${livro.id})" title="Excluir livro">🗑️</button>`
            : "";

        const card = document.createElement("div");
        card.className = "book-card";
        card.innerHTML = `
            <div>
                <div class="book-icon">📖</div>
                <div class="book-title">${livro.titulo}</div>
                <div class="book-author">por ${livro.autor}</div>
                <div class="progress-container">
                    <div class="book-meta">
                        <span>${statusTexto}</span>
                        <strong>${porcentagem}%</strong>
                    </div>
                    <div class="progress-bar-bg">
                        <div class="progress-bar-fill" style="width: ${porcentagem}%"></div>
                    </div>
                </div>
            </div>
            <div class="book-actions">
                <button class="btn btn-primary btn-full" onclick="abrirLeitor(${livro.id}, ${paginaAtual})">
                    🎧 Ler / Audiobook
                </button>
                ${botaoDeletar}
            </div>
        `;
        grid.appendChild(card);
    });
}

async function abrirLeitor(livroId, paginaAtual) {
    let paginaInicial = paginaAtual > 0 ? paginaAtual : 1;

    // Se o usuário ainda não tinha progresso para este livro, cria na página 1
    if (!mapaProgresso[livroId]) {
        try {
            await fetch(`${API_URL}/progresso/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    usuario_id: usuarioLogado.id,
                    livro_id: livroId,
                    pagina_atual: 1
                })
            });
        } catch (e) {
            // Ignora caso já exista
        }
    }

    window.location.href = `leitor.html?livro_id=${livroId}&pagina=${paginaInicial}`;
}

function abrirModalUpload() {
    document.getElementById("modal-upload").classList.add("open");
}

function fecharModalUpload() {
    document.getElementById("modal-upload").classList.remove("open");
    document.getElementById("form-upload").reset();
    document.getElementById("modal-alerta").style.display = "none";
}

async function enviarNovoLivro(event) {
    event.preventDefault();
    const alerta = document.getElementById("modal-alerta");
    const btn = document.getElementById("btn-submit-upload");

    const titulo = document.getElementById("livro-titulo").value.trim();
    const autor = document.getElementById("livro-autor").value.trim();
    const arquivo = document.getElementById("livro-arquivo").files[0];

    const formData = new FormData();
    formData.append("titulo", titulo);
    formData.append("autor", autor);
    formData.append("arquivo", arquivo);

    btn.disabled = true;
    btn.textContent = "Enviando e contando páginas...";

    try {
        const resp = await fetch(`${API_URL}/livros/`, {
            method: "POST",
            body: formData
        });

        const dados = await resp.json();

        if (!resp.ok) {
            throw new Error(dados.detail || "Erro ao cadastrar livro");
        }

        fecharModalUpload();
        await carregarAcervo();
    } catch (erro) {
        alerta.textContent = erro.message;
        alerta.className = "alert-box alert-error";
        alerta.style.display = "block";
    } finally {
        btn.disabled = false;
        btn.textContent = "Enviar PDF e Cadastrar";
    }
}

async function deletarLivro(id) {
    if (!confirm("Deseja realmente excluir este livro do acervo?")) return;

    try {
        const resp = await fetch(`${API_URL}/livros/${id}`, {
            method: "DELETE"
        });
        if (resp.ok) {
            await carregarAcervo();
        }
    } catch (erro) {
        alert("Erro ao excluir livro");
    }
}
