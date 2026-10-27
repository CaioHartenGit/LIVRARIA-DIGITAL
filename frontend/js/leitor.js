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

const synth = window.speechSynthesis;
let falaAtual = null;

document.addEventListener("DOMContentLoaded", () => {
    if (!livroId) {
        window.location.href = "livros.html";
        return;
    }
    carregarPagina(paginaAtual);
});

window.addEventListener("beforeunload", () => {
    if (synth.speaking) {
        synth.cancel();
    }
});

async function carregarPagina(numeroPagina) {
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
        document.getElementById("indicador-pagina").textContent = `Página ${paginaAtual} / ${totalPaginas}`;

        conteudoEl.textContent = textoAtual.length > 0
            ? textoAtual
            : "[Esta página do PDF não possui texto selecionável ou contém apenas imagens.]";

        // Atualiza os botões de paginação
        document.getElementById("btn-anterior").disabled = paginaAtual <= 1;
        document.getElementById("btn-proxima").disabled = paginaAtual >= totalPaginas;

        // Salva o progresso automaticamente no PostgreSQL
        await salvarProgressoNoBanco(paginaAtual);
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
    document.getElementById("leitor-progresso-badge").innerHTML = `Progresso salvo: <strong>Pág. ${pagina}</strong>`;

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
    }
}

// ==================== CONTROLES DO AUDIOBOOK (TTS) ====================

function iniciarAudiobook() {
    if (!textoAtual) {
        document.getElementById("status-audio").textContent = "Não há texto nesta página para ler.";
        return;
    }

    synth.cancel();

    falaAtual = new SpeechSynthesisUtterance(textoAtual);
    falaAtual.lang = "pt-BR";
    falaAtual.rate = parseFloat(document.getElementById("velocidade-voz").value) || 1.0;

    // Tenta selecionar uma voz em Português se disponível no sistema
    const vozes = synth.getVoices();
    const vozPt = vozes.find((v) => v.lang.includes("pt-BR") || v.lang.includes("pt"));
    if (vozPt) {
        falaAtual.voice = vozPt;
    }

    falaAtual.onstart = () => {
        document.getElementById("status-audio").textContent = `🔊 Lendo a Página ${paginaAtual} em voz alta...`;
    };

    falaAtual.onend = () => {
        document.getElementById("status-audio").textContent = `✅ Leitura da Página ${paginaAtual} finalizada.`;
    };

    falaAtual.onerror = () => {
        document.getElementById("status-audio").textContent = "Leitura interrompida.";
    };

    synth.speak(falaAtual);
}

function pausarOuRetomarAudio() {
    const btnPause = document.getElementById("btn-pause");
    const statusAudio = document.getElementById("status-audio");

    if (synth.speaking && !synth.paused) {
        synth.pause();
        btnPause.textContent = "▶️ Retomar";
        statusAudio.textContent = "⏸️ Audiobook pausado";
    } else if (synth.paused) {
        synth.resume();
        btnPause.textContent = "⏸️ Pausar";
        statusAudio.textContent = `🔊 Lendo a Página ${paginaAtual} em voz alta...`;
    }
}

function pararAudiobook() {
    if (synth.speaking || synth.paused) {
        synth.cancel();
    }
    const btnPause = document.getElementById("btn-pause");
    const statusAudio = document.getElementById("status-audio");
    if (btnPause) btnPause.textContent = "⏸️ Pausar";
    if (statusAudio) statusAudio.textContent = "Pronto para ler a página em voz alta";
}
