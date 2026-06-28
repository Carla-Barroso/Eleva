// URL base do seu servidor Flask
const API_URL = 'https://cahdiel.pythonanywhere.com/api';

document.addEventListener('DOMContentLoaded', () => {

    // 1. LÓGICA DE LOGIN (Acessar Conta)
    const formLogin = document.getElementById('form-login');
    if (formLogin) {
        formLogin.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const loginInput = document.getElementById('login-email').value;
            const passwordInput = document.getElementById('login-password').value;

            try {
                const response = await fetch(`${API_URL}/login`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ login: loginInput, senha: passwordInput })
                });

                const data = await response.json();

                if (data.sucesso) {
                    // Salva os dados no navegador para usar nas telas
                    localStorage.setItem('usuarioNome', data.usuario.nome);
                    localStorage.setItem('usuarioTipo', data.usuario.tipo);

                    // Redireciona para o painel correto com base no tipo de usuário
                    if (data.usuario.tipo === 'cliente') {
                        window.location.href = 'painel-cliente.html';
                    } else if (data.usuario.tipo === 'profissional') {
                        window.location.href = 'painel-profissional.html';
                    } else if (data.usuario.tipo === 'instituicao') {
                        window.location.href = 'painel-instituicao.html';
                    }
                } else {
                    alert('Erro no login: ' + data.mensagem);
                }
            } catch (error) {
                console.error('Erro na requisição:', error);
                alert('Erro de conexão com o servidor.');
            }
        });
    }

    // 2. LÓGICA DE CADASTRO (Novo Cliente)
    const formRegister = document.getElementById('form-register');
    if (formRegister) {
        formRegister.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const nome = document.getElementById('reg-nome').value;
            const email = document.getElementById('reg-email').value;
            const senha = document.getElementById('reg-password').value;
            const tipo = document.getElementById('reg-tipo').value;

            try {
                const response = await fetch(`${API_URL}/cadastro`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ nome, email, senha, tipo })
                });

                const data = await response.json();

                if (data.sucesso) {
                    alert('Cadastro realizado! Faça login para continuar.');
                    // Muda visualmente para a aba de login
                    document.getElementById('tab-login').click();
                } else {
                    alert('Erro: ' + data.mensagem);
                }
            } catch (error) {
                console.error('Erro:', error);
            }
        });
    }

    // 3. LÓGICA DE ATIVAÇÃO DA CONTA (Profissional)
    const formActivate = document.getElementById('form-activate');
    if (formActivate) {
        formActivate.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const idAtivacao = document.getElementById('act-id').value;
            const senha = document.getElementById('act-password').value;
            const senhaConfirm = document.getElementById('act-password-confirm').value;

            if (senha !== senhaConfirm) {
                alert('As senhas não coincidem!');
                return;
            }

            try {
                const response = await fetch(`${API_URL}/ativar`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ id_ativacao: idAtivacao, senha: senha })
                });

                const data = await response.json();

                if (data.sucesso) {
                    alert('Conta ativada com sucesso! Redirecionando...');
                    // Após ativar, já joga ele pro painel do profissional
                    localStorage.setItem('usuarioTipo', 'profissional');
                    window.location.href = 'painel-profissional.html';
                } else {
                    alert('Erro na ativação: ' + data.mensagem);
                }
            } catch (error) {
                console.error('Erro:', error);
            }
        });
    }
});