const API_URL = "https://luminabooks.onrender.com";

const usuarioLogado = JSON.parse(localStorage.getItem("usuario_livraria"));
if (!usuarioLogado) {
    window.location.href = "index.html";
}

let mapaProgresso = {};
let todosLivrosCache = [];
let filtroAtual = "todos";

document.addEventListener("DOMContentLoaded", () => {
    const userInfo = document.getElementById("user-info");
    userInfo.innerHTML = `👤 <strong>${usuarioLogado.nome}</strong> <span class="role-tag">${usuarioLogado.tipo_usuario}</span>`;

    // O botão de Upload de PDF fica liberado tanto para 'normal' quanto para 'admin'
    // A diferença é que o 'admin' visualiza o botão exclusivo de listar todos os usuários
    const btnAdminUsuarios = document.getElementById("btn-admin-usuarios");
    if (usuarioLogado.tipo_usuario === "admin" && btnAdminUsuarios) {
        btnAdminUsuarios.style.display = "inline-flex";
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
        // Sem progresso registrado ainda
    }
}

function atualizarPainelEstatisticas(livros) {
    const totalLivros = Array.isArray(livros) ? livros.length : 0;
    let emLeitura = 0;
    let concluidos = 0;
    let paginasLidas = 0;

    Object.values(mapaProgresso).forEach((prog) => {
        paginasLidas += prog.pagina_atual || 0;
        if (prog.concluido) {
            concluidos++;
        } else if (prog.pagina_atual > 0) {
            emLeitura++;
        }
    });

    document.getElementById("stat-total-livros").textContent = totalLivros;
    document.getElementById("stat-lendo").textContent = emLeitura;
    document.getElementById("stat-concluidos").textContent = concluidos;
    document.getElementById("stat-paginas").textContent = paginasLidas;
}

async function carregarAcervo() {
    document.getElementById("input-busca").value = "";
    await carregarProgressoUsuario();

    const grid = document.getElementById("books-grid");
    grid.innerHTML = "<p style='color: var(--text-muted);'>Sincronizando biblioteca...</p>";

    try {
        const resp = await fetch(`${API_URL}/livros/?usuario_id=${usuarioLogado.id}`);
        const dados = await resp.json();

        if (!resp.ok || !Array.isArray(dados)) {
            todosLivrosCache = [];
            atualizarPainelEstatisticas([]);
            grid.innerHTML = `<p style="color: var(--text-muted);">Nenhum livro cadastrado no acervo ainda.</p>`;
            return;
        }

        todosLivrosCache = dados;
        atualizarPainelEstatisticas(dados);
        aplicarFiltro(filtroAtual);
    } catch (erro) {
        grid.innerHTML = `<p style="color: var(--text-muted);">Nenhum livro disponível no momento.</p>`;
    }
}

function aplicarFiltro(tipo) {
    filtroAtual = tipo;
    ["todos", "lendo", "concluidos"].forEach((id) => {
        const btn = document.getElementById(`filtro-${id}`);
        if (btn) btn.classList.toggle("active", id === tipo);
    });

    let filtrados = todosLivrosCache;
    if (tipo === "lendo") {
        filtrados = todosLivrosCache.filter((l) => {
            const p = mapaProgresso[l.id];
            return p && p.pagina_atual > 0 && !p.concluido;
        });
    } else if (tipo === "concluidos") {
        filtrados = todosLivrosCache.filter((l) => {
            const p = mapaProgresso[l.id];
            return p && p.concluido;
        });
    }

    renderizarLivros(filtrados);
}

async function buscarLivros() {
    const termo = document.getElementById("input-busca").value.trim();
    if (!termo) {
        return carregarAcervo();
    }

    const grid = document.getElementById("books-grid");
    try {
        const resp = await fetch(`${API_URL}/livros/titulo/${encodeURIComponent(termo)}?usuario_id=${usuarioLogado.id}`);
        const dados = await resp.json();

        if (!resp.ok || !Array.isArray(dados)) {
            grid.innerHTML = `<p style="color: var(--text-muted);">Nenhum livro encontrado para "${termo}".</p>`;
            return;
        }

        renderizarLivros(dados);
    } catch (erro) {
        grid.innerHTML = `<p style="color: var(--text-muted);">Erro ao pesquisar livros.</p>`;
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

    if (!livros.length) {
        grid.innerHTML = `<p style="color: var(--text-muted);">Nenhum livro encontrado nesta categoria.</p>`;
        return;
    }

    livros.forEach((livro, index) => {
        const prog = mapaProgresso[livro.id];
        const paginaAtual = prog ? prog.pagina_atual : 0;
        const porcentagem = livro.total_paginas > 0
            ? Math.min(100, Math.round((paginaAtual / livro.total_paginas) * 100))
            : 0;

        const statusTexto = prog && prog.concluido
            ? "✅ Concluído"
            : prog && paginaAtual > 0
                ? `📖 Pág. ${paginaAtual} de ${livro.total_paginas}`
                : "✨ Novo para leitura";

        const temaCapa = `cover-theme-${(livro.id || index) % 5}`;

        const podeDeletar = usuarioLogado.tipo_usuario === "admin" || livro.usuario_id === usuarioLogado.id;
        const botaoDeletar = podeDeletar
            ? `<button class="btn btn-danger" onclick="deletarLivro(${livro.id})" title="Excluir obra">🗑️</button>`
            : "";

        const tagDonoAdmin = usuarioLogado.tipo_usuario === "admin" && livro.usuario_id
            ? ` <span style="font-size: 0.75rem; color: var(--primary-light);">• ${livro.usuario_id === usuarioLogado.id ? "Sua obra" : `Usuário #${livro.usuario_id}`}</span>`
            : "";

        const card = document.createElement("div");
        card.className = "book-card";
        card.innerHTML = `
            <div class="book-cover-banner ${temaCapa}">
                <span class="book-cover-badge">${livro.total_paginas} págs</span>
                <div class="book-cover-title-preview">${livro.titulo}</div>
            </div>
            <div class="book-card-body">
                <div>
                    <div class="book-title">${livro.titulo}</div>
                    <div class="book-author">por ${livro.autor}${tagDonoAdmin}</div>
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
                        🎧 Ler & Audiobook
                    </button>
                    <a href="${API_URL}/${livro.arquivo_path}" target="_blank" class="btn btn-outline" title="Abrir PDF original">
                        📄
                    </a>
                    ${botaoDeletar}
                </div>
            </div>
        `;
        grid.appendChild(card);
    });
}

async function abrirLeitor(livroId, paginaAtual) {
    const paginaInicial = paginaAtual > 0 ? paginaAtual : 1;

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
            // Progresso já iniciado
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
    formData.append("usuario_id", usuarioLogado.id);
    formData.append("arquivo", arquivo);

    btn.disabled = true;
    btn.textContent = "Processando PDF e contando páginas...";

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
        btn.textContent = "Enviar PDF e Cadastrar Obra";
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

// ==================== PAINEL EXCLUSIVO DE ADMIN: LISTAR USUÁRIOS ====================

async function abrirModalUsuariosAdmin() {
    const modal = document.getElementById("modal-usuarios-admin");
    const container = document.getElementById("lista-usuarios-container");
    modal.classList.add("open");
    container.innerHTML = "<p style='color: var(--text-muted);'>Consultando usuários no banco...</p>";

    try {
        const resp = await fetch(`${API_URL}/usuarios/admin/${usuarioLogado.id}`);
        const usuarios = await resp.json();

        if (!resp.ok || !Array.isArray(usuarios)) {
            throw new Error(usuarios.detail || "Acesso negado.");
        }

        container.innerHTML = "";
        usuarios.forEach((u) => {
            const item = document.createElement("div");
            item.style.cssText = "display: flex; align-items: center; justify-content: space-between; background: var(--bg-input); border: 1px solid var(--border-subtle); padding: 12px 16px; border-radius: 12px;";
            item.innerHTML = `
                <div>
                    <strong style="font-size: 0.95rem;">${u.nome}</strong>
                    <span class="role-tag">${u.tipo_usuario}</span>
                    <div style="font-size: 0.82rem; color: var(--text-muted); margin-top: 2px;">${u.email} (ID: #${u.id})</div>
                </div>
                ${u.id !== usuarioLogado.id ? `<button class="btn btn-danger" style="padding: 6px 12px; font-size: 0.8rem;" onclick="deletarUsuarioComoAdmin(${u.id})">Remover</button>` : `<span style="font-size: 0.78rem; color: var(--accent);">Você</span>`}
            `;
            container.appendChild(item);
        });
    } catch (erro) {
        container.innerHTML = `<p style="color: var(--danger);">${erro.message}</p>`;
    }
}

function fecharModalUsuariosAdmin() {
    document.getElementById("modal-usuarios-admin").classList.remove("open");
}

async function deletarUsuarioComoAdmin(idUsuario) {
    if (!confirm("Deseja realmente excluir este usuário?")) return;

    try {
        const resp = await fetch(`${API_URL}/usuarios/${usuarioLogado.id}?id_usuario=${idUsuario}`, {
            method: "DELETE"
        });
        if (resp.ok || resp.status === 204) {
            await abrirModalUsuariosAdmin();
        }
    } catch (e) {
        alert("Erro ao remover usuário.");
    }
}
