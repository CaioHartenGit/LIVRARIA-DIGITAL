const API_URL = "http://127.0.0.1:8000";

const usuarioLogado = JSON.parse(localStorage.getItem("usuario_livraria"));
if (!usuarioLogado) {
    window.location.href = "index.html";
}

const params = new URLSearchParams(window.location.search);
const livroId = parseInt(params.get("livro_id"));
let paginaAtual = parseInt(params.get("pagina")) || 1;
let totalPaginas = 1;
let textoAtual = "";
let tamanhoFonteRem = 1.14;

const synth = window.speechSynthesis;
let falaAtual = null;

document.addEventListener("DOMContentLoaded", () => {
    if (!livroId) {
        window.location.href = "livros.html";
        return;
    }
    carregarPagina(paginaAtual);

    // Atalhos de teclado (Setas Esquerda e Direita)
    document.addEventListener("keydown", (e) => {
        if (e.key === "ArrowLeft") mudarPagina(-1);
        if (e.key === "ArrowRight") mudarPagina(1);
    });
});

window.addEventListener("beforeunload", () => {
    if (synth.speaking) {
        synth.cancel();
    }
});

async function carregarPagina(numeroPagina, iniciarAudioAutomatico = false) {
    pararAudiobook();

    const conteudoEl = document.getElementById("conteudo-pagina");
    conteudoEl.textContent = "Extraindo texto da página do PDF...";

    try {
        const resp = await fetch(`${API_URL}/livros/${livroId}/pagina/${numeroPagina}`);
        const dados = await resp.json();

        if (!resp.ok) {
            throw new Error(dados.detail || "Não foi possível carregar esta página");
        }

        paginaAtual = dados.pagina_atual;
        totalPaginas = dados.total_paginas;
        textoAtual = (dados.texto || "").trim();

        document.getElementById("titulo-livro").textContent = dados.titulo;
        document.getElementById("subtitulo-pagina").textContent = `Página ${paginaAtual} de ${totalPaginas}`;
        document.getElementById("indicador-pagina").textContent = `Página ${paginaAtual} de ${totalPaginas}`;

        conteudoEl.textContent = textoAtual.length > 0
            ? textoAtual
            : "[Esta página do PDF não possui texto selecionável ou contém apenas ilustrações.]";

        document.getElementById("btn-anterior").disabled = paginaAtual <= 1;
        document.getElementById("btn-proxima").disabled = paginaAtual >= totalPaginas;

        await salvarProgressoNoBanco(paginaAtual);

        if (iniciarAudioAutomatico && textoAtual.length > 0) {
            iniciarAudiobook();
        }
    } catch (erro) {
        conteudoEl.textContent = `Erro: ${erro.message}`;
    }
}

async function salvarProgressoNoBanco(pagina) {
    const porcentagem = totalPaginas > 0 ? Math.min(100, Math.round((pagina / totalPaginas) * 100)) : 0;
    const concluido = pagina === totalPaginas;

    document.getElementById("porcentagem-leitura").textContent = `${porcentagem}%`;
    document.getElementById("barra-progresso").style.width = `${porcentagem}%`;
    document.getElementById("status-conclusao").textContent = concluido ? "✅ Livro Concluído!" : "📖 Em leitura";
    document.getElementById("leitor-progresso-badge").innerHTML = `Salvo no banco: <strong>Pág. ${pagina}/${totalPaginas}</strong>`;

    try {
        await fetch(`${API_URL}/progresso/${usuarioLogado.id}/${livroId}/`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ pagina_atual: pagina })
        });
    } catch (e) {
        console.error("Erro ao sincronizar progresso:", e);
    }
}

function mudarPagina(direcao) {
    const novaPagina = paginaAtual + direcao;
    if (novaPagina >= 1 && novaPagina <= totalPaginas) {
        carregarPagina(novaPagina);
        window.scrollTo({ top: 0, behavior: "smooth" });
    }
}

// ==================== PERSONALIZAÇÃO DO LEITOR (KINDLE MODE) ====================

function mudarTemaPapel(tema) {
    const folha = document.getElementById("conteudo-pagina");
    folha.classList.remove("theme-sepia", "theme-light");

    if (tema === "sepia") folha.classList.add("theme-sepia");
    if (tema === "light") folha.classList.add("theme-light");

    ["dark", "sepia", "light"].forEach((t) => {
        document.getElementById(`tema-${t}`).classList.toggle("active", t === tema);
    });
}

function mudarFonte(tipo) {
    const folha = document.getElementById("conteudo-pagina");
    if (tipo === "serif") {
        folha.classList.add("font-serif");
    } else {
        folha.classList.remove("font-serif");
    }
    document.getElementById("fonte-sans").classList.toggle("active", tipo === "sans");
    document.getElementById("fonte-serif").classList.toggle("active", tipo === "serif");
}

function ajustarTamanhoFonte(delta) {
    tamanhoFonteRem = Math.min(1.6, Math.max(0.9, tamanhoFonteRem + delta));
    document.getElementById("conteudo-pagina").style.fontSize = `${tamanhoFonteRem.toFixed(2)}rem`;
}

// ==================== CONTROLES DO AUDIOBOOK STUDIO ====================

function definirAnimacaoEqualizador(ativo) {
    const eq = document.getElementById("audio-equalizer");
    if (eq) eq.classList.toggle("playing", ativo);
}

function iniciarAudiobook() {
    if (!textoAtual) {
        document.getElementById("status-audio").textContent = "Não há texto nesta página para narrar.";
        return;
    }

    synth.cancel();

    falaAtual = new SpeechSynthesisUtterance(textoAtual);
    falaAtual.lang = "pt-BR";
    falaAtual.rate = parseFloat(document.getElementById("velocidade-voz").value) || 1.0;

    const vozes = synth.getVoices();
    const vozPt = vozes.find((v) => v.lang.includes("pt-BR") || v.lang.includes("pt"));
    if (vozPt) {
        falaAtual.voice = vozPt;
    }

    falaAtual.onstart = () => {
        definirAnimacaoEqualizador(true);
        document.getElementById("status-audio").textContent = `🔊 Narrando a Página ${paginaAtual} em voz alta...`;
    };

    falaAtual.onend = () => {
        definirAnimacaoEqualizador(false);
        document.getElementById("status-audio").textContent = `✅ Leitura da Página ${paginaAtual} concluída.`;

        const autoAvancar = document.getElementById("auto-avancar");
        if (autoAvancar && autoAvancar.checked && paginaAtual < totalPaginas) {
            carregarPagina(paginaAtual + 1, true);
        }
    };

    falaAtual.onerror = () => {
        definirAnimacaoEqualizador(false);
        document.getElementById("status-audio").textContent = "Narração pausada ou interrompida.";
    };

    synth.speak(falaAtual);
}

function pausarOuRetomarAudio() {
    const btnPause = document.getElementById("btn-pause");
    const statusAudio = document.getElementById("status-audio");

    if (synth.speaking && !synth.paused) {
        synth.pause();
        definirAnimacaoEqualizador(false);
        btnPause.textContent = "▶️ Retomar";
        statusAudio.textContent = "⏸️ Audiobook pausado";
    } else if (synth.paused) {
        synth.resume();
        definirAnimacaoEqualizador(true);
        btnPause.textContent = "⏸️ Pausar";
        statusAudio.textContent = `🔊 Narrando a Página ${paginaAtual} em voz alta...`;
    }
}

function pararAudiobook() {
    if (synth.speaking || synth.paused) {
        synth.cancel();
    }
    definirAnimacaoEqualizador(false);
    const btnPause = document.getElementById("btn-pause");
    const statusAudio = document.getElementById("status-audio");
    if (btnPause) btnPause.textContent = "⏸️ Pausar";
    if (statusAudio) statusAudio.textContent = "Pronto para narrar esta página em Português";
}
