const API_URL = "http://127.0.0.1:8000";

function mostrarAlerta(mensagem, tipo = "error") {
    const alertBox = document.getElementById("alert-box");
    alertBox.textContent = mensagem;
    alertBox.className = `alert-box ${tipo === "success" ? "alert-success" : "alert-error"}`;
    alertBox.style.display = "block";
}

function esconderAlerta() {
    const alertBox = document.getElementById("alert-box");
    if (alertBox) alertBox.style.display = "none";
}

function alternarAba(aba) {
    esconderAlerta();
    const formLogin = document.getElementById("form-login");
    const formCadastro = document.getElementById("form-cadastro");
    const tabLogin = document.getElementById("tab-login");
    const tabCadastro = document.getElementById("tab-cadastro");

    if (aba === "login") {
        formLogin.style.display = "block";
        formCadastro.style.display = "none";
        tabLogin.classList.add("active");
        tabCadastro.classList.remove("active");
    } else {
        formLogin.style.display = "none";
        formCadastro.style.display = "block";
        tabCadastro.classList.add("active");
        tabLogin.classList.remove("active");
    }
}

async function realizarLogin(event) {
    event.preventDefault();
    esconderAlerta();

    const email = document.getElementById("login-email").value.trim();
    const senha = document.getElementById("login-senha").value;

    try {
        const resposta = await fetch(`${API_URL}/usuarios/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, senha })
        });

        const dados = await resposta.json();

        if (!resposta.ok) {
            throw new Error(dados.detail || "Falha ao realizar login");
        }

        localStorage.setItem("usuario_livraria", JSON.stringify(dados));
        window.location.href = "livros.html";
    } catch (erro) {
        mostrarAlerta(erro.message, "error");
    }
}

async function realizarCadastro(event) {
    event.preventDefault();
    esconderAlerta();

    const nome = document.getElementById("cad-nome").value.trim();
    const email = document.getElementById("cad-email").value.trim();
    const senha = document.getElementById("cad-senha").value;

    try {
        const resposta = await fetch(`${API_URL}/usuarios/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ nome, email, senha })
        });

        const dados = await resposta.json();

        if (!resposta.ok) {
            throw new Error(dados.detail || "Erro ao cadastrar usuário");
        }

        mostrarAlerta("Conta criada com sucesso! Faça login para entrar.", "success");
        setTimeout(() => alternarAba("login"), 1200);
    } catch (erro) {
        mostrarAlerta(erro.message, "error");
    }
}
