import sqlite3
import random
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)

# ADICIONE ESTA LINHA EXATAMENTE ASSIM:
DB_FILE = '/home/cahdiel/eleva/database.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # 1. Tabela de Usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE,
            senha_hash TEXT,
            tipo TEXT NOT NULL,
            id_ativacao TEXT UNIQUE,
            status_conta TEXT DEFAULT 'Ativo',
            foto TEXT
        )
    ''')

    # 2. Tabela de Solicitações (Atualizada com codigo_verificacao, nota e comentario)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS solicitacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            profissional_nome TEXT NOT NULL,
            nome_cliente TEXT NOT NULL,
            whatsapp TEXT NOT NULL,
            data_servico TEXT NOT NULL,
            endereco TEXT NOT NULL,
            detalhes TEXT NOT NULL,
            status TEXT DEFAULT 'Pendente',
            codigo_verificacao TEXT,
            nota INTEGER,
            comentario TEXT,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 3. Tabela de Profissionais (Atualizada dinamicamente com status)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS profissionais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT, profissao TEXT, categoria TEXT, regiao TEXT,
            instituicao TEXT, foto TEXT, nota REAL, avaliacoes_qtd INTEGER,
            servicos_qtd INTEGER, sobre_mim TEXT, habilidades TEXT,
            preco_inicial TEXT, preco_diaria TEXT, preco_orcamento TEXT,
            review_recente TEXT, review_autor TEXT, taxa_comparecimento TEXT,
            taxa_resposta TEXT, clientes_recorrentes TEXT,
            status TEXT DEFAULT 'Ativo'
        )
    ''')

    # 4. Tabela de Mensagens
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mensagens (
            id INTEGER PRIMARY KEY AUTOINCREMENT, sala TEXT, remetente TEXT,
            texto TEXT, data_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()

    # Carga Inicial de Dados de Teste
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        senha_padrao = generate_password_hash('123456')

        cursor.execute("INSERT INTO usuarios (nome, email, senha_hash, tipo) VALUES (?, ?, ?, ?)",
                       ('Carlos Eduardo', 'cliente@eleva.com', senha_padrao, 'cliente'))

        instituicoes = [
            ('Instituto Horizonte', 'horizonte@eleva.com', senha_padrao, 'instituicao'),
            ('Projeto Caminhos', 'caminhos@eleva.com', senha_padrao, 'instituicao'),
            ('Rede Novo Ofício', 'novooficio@eleva.com', senha_padrao, 'instituicao')
        ]
        cursor.executemany("INSERT INTO usuarios (nome, email, senha_hash, tipo) VALUES (?, ?, ?, ?)", instituicoes)

        dados_profissionais = [
            ("João Silva", "Eletricista", "Manutenção e Reparos", "Taguatinga, DF", "Instituto Horizonte", 4.9, 42, 120, "Especialista em instalações residenciais e manutenção de redes elétricas preventivas.", "Instalação Elétrica, Quadros de Força, Troca de Fiação", "80,00", "220,00", "ELEVA-PRO-01"),
            ("Marcos Paulo", "Encanador", "Manutenção e Reparos", "Ceilândia, DF", "Projeto Caminhos", 4.7, 18, 54, "Atuo com caça-vazamentos, reparos hidráulicos e limpeza de colunas prediais.", "Caça-Vazamentos, Reparos de Válvulas, Tubulação PVC", "90,00", "250,00", "ELEVA-PRO-02"),
            ("Ricardo Vieira", "Montador de Móveis", "Manutenção e Reparos", "Samambaia, DF", "Instituto Horizonte", 4.8, 29, 88, "Montagem e desmontagem de móveis planejados ou convencionais com rapidez.", "Móveis Planejados, Adaptações de Marcenaria, Reparos", "70,00", "200,00", "ELEVA-PRO-03"),
            ("Gabriel Mota", "Técnico de Refrigeração", "Manutenção e Reparos", "Plano Piloto, DF", "Instituto Horizonte", 5.0, 15, 40, "Instalação e higienização de aparelhos de ar condicionado de todas as marcas.", "Ar Condicionado, Carga de Gás, Limpeza Química", "120,00", "300,00", "ELEVA-PRO-04"),
            ("Ana Júlia", "Pintora Residencial", "Obras e Reformas", "Guará, DF", "Projeto Caminhos", 4.9, 31, 95, "Pintura decorativa, aplicação de texturas e acabamento fino para interiores.", "Texturas, Pintura Acrílica, Tratamento de Paredes", "85,00", "240,00", "ELEVA-PRO-05"),
            ("Roberto Alves", "Pedreiro de Acabamento", "Obras e Reformas", "Sobradinho, DF", "Projeto Caminhos", 4.6, 22, 70, "Especializado no assentamento de porcelanatos, revestimentos e reformas em geral.", "Porcelanato, Alvenaria, Contra-piso", "100,00", "280,00", "ELEVA-PRO-06"),
            ("Fernando Costa", "Marceneiro", "Obras e Reformas", "Gama, DF", "Rede Novo Ofício", 4.8, 19, 50, "Restauração de móveis de madeira maciça e fabricação de pequenas peças sob medida.", "Restauração, Acabamento em Verniz, Cortes Precisos", "110,00", "260,00", "ELEVA-PRO-07"),
            ("Juliano Prates", "Serralheiro", "Obras e Reformas", "Santa Maria, DF", "Projeto Caminhos", 4.5, 14, 38, "Fabricação e reparo de portões, grades, corrimãos e estruturas metálicas leves.", "Solda Elétrica, Estruturas Metálicas, Portões", "95,00", "270,00", "ELEVA-PRO-08"),
            ("Maria Santos", "Diarista Profissional", "Limpeza", "Águas Claras, DF", "Rede Novo Ofício", 5.0, 55, 160, "Limpeza residencial detalhada com foco em organização e otimização do tempo.", "Limpeza Fina, Organização de Armários, Higienização", "130,00", "130,00", "ELEVA-PRO-09"),
            ("Patricia Gomes", "Especialista Pós-Obra", "Limpeza", "Plano Piloto, DF", "Instituto Horizonte", 4.7, 24, 65, "Remoção técnica de resíduos de tinta, gesso e cimento para entrega de obras limpas.", "Limpeza Pós-Obra, Remoção de Resíduos, Vidraças", "150,00", "350,00", "ELEVA-PRO-10"),
            ("Sandra Ribeiro", "Passadeira", "Limpeza", "Cruzeiro, DF", "Rede Novo Ofício", 4.9, 40, 110, "Passadoria de roupas sociais, delicadas e enxovais com agilidade e cuidado.", "Ferro a Vapor, Roupas Sociais, Organização", "80,00", "160,00", "ELEVA-PRO-11"),
            ("Elaine Costa", "Personal Organizer", "Limpeza", "Sudoeste, DF", "Rede Novo Ofício", 4.8, 17, 45, "Consultoria de organização inteligente para closets, cozinhas e home office.", "Otimização de Espaço, Triagem, Organização Funcional", "140,00", "290,00", "ELEVA-PRO-12"),
            ("Carlos Souza", "Técnico de Informática", "Tecnologia", "Ceilândia, DF", "Instituto Horizonte", 4.9, 33, 102, "Formatação, remoção de vírus, montagem de computadores e configuração de redes.", "Formatação, Instalação de Redes, Hardware", "75,00", "200,00", "ELEVA-PRO-13"),
            ("Amanda Duarte", "Instrutora Digital / Suporte", "Tecnologia", "Taguatinga, DF", "Instituto Horizonte", 4.6, 12, 28, "Treinamento para uso de smartphones, computadores e ferramentas de trabalho para idosos.", "Inclusão Digital, Configuração de Apps, Segurança", "60,00", "180,00", "ELEVA-PRO-14"),
            ("Bruno Mendes", "Instalador de Câmeras/CFTV", "Tecnologia", "Recanto das Emas, DF", "Projeto Caminhos", 4.8, 20, 61, "Configuração de sistemas de segurança residencial, câmeras Wi-Fi e alarmes.", "CFTV, Câmeras IP, Configuração de DVR", "90,00", "240,00", "ELEVA-PRO-15")
        ]

        for p in dados_profissionais:
            cursor.execute('''
                INSERT INTO profissionais (nome, profissao, categoria, regiao, instituicao, nota, avaliacoes_qtd, servicos_qtd, sobre_mim, habilidades, preco_inicial, preco_diaria, preco_orcamento, review_recente, review_autor, taxa_comparecimento, taxa_resposta, clientes_recorrentes, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Combinado via Chat', 'Excelente prestação de serviço, recomendo a todos do sistema.', 'Cliente Satisfeito', '100%', '96%', '8', 'Ativo')
            ''', (p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11]))

            email_fake = f"pro{p[12].split('-')[-1].lower()}@eleva.com"
            cursor.execute('''
                INSERT INTO usuarios (nome, email, senha_hash, tipo, id_ativacao, status_conta)
                VALUES (?, ?, ?, 'profissional', ?, 'Ativo')
            ''', (p[0], email_fake, senha_padrao, p[12]))

    conn.commit()
    conn.close()

# --- ROTAS DE AUTENTICAÇÃO ---

@app.route('/api/cadastro', methods=['POST'])
def cadastro():
    data = request.json
    senha_hash = generate_password_hash(data['senha'])

    tipo_usuario = data.get('tipo', 'cliente')

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO usuarios (nome, email, senha_hash, tipo, status_conta) VALUES (?, ?, ?, ?, ?)',
                       (data['nome'], data['email'], senha_hash, tipo_usuario, 'Ativo'))
        conn.commit()
        return jsonify({"sucesso": True, "mensagem": "Cadastro realizado com sucesso!"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"sucesso": False, "mensagem": "Este e-mail já está cadastrado."}), 400
    except Exception as e:
        return jsonify({"sucesso": False, "mensagem": f"Erro interno: {str(e)}"}), 500
    finally:
        conn.close()


@app.route('/api/login', methods=['POST'])
def login():
    data = request.json

    identificador = data.get('email', data.get('login'))
    senha = data.get('senha')

    if not identificador or not senha:
        return jsonify({"sucesso": False, "mensagem": "Preencha todos os campos."}), 400

    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE email = ? OR id_ativacao = ?", (identificador, identificador))
    usuario = cursor.fetchone()
    conn.close()

    if usuario and check_password_hash(usuario['senha_hash'], senha):
        return jsonify({
            "sucesso": True,
            "mensagem": "Login realizado com sucesso!",
            "usuario": {
                "id": usuario['id'],
                "nome": usuario['nome'],
                "email": usuario['email'],
                "tipo": usuario['tipo'],
                "id_ativacao": usuario['id_ativacao']
            }
        }), 200
    else:
        return jsonify({"sucesso": False, "mensagem": "E-mail/ID ou senha incorretos."}), 401


@app.route('/api/ativar', methods=['POST'])
def ativar_conta():
    data = request.json
    id_ativacao = data.get('id_ativacao')
    nova_senha = data.get('senha')

    if not id_ativacao or not nova_senha:
        return jsonify({"sucesso": False, "mensagem": "Preencha todos os campos."}), 400

    senha_hash = generate_password_hash(nova_senha)

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM usuarios WHERE id_ativacao = ?", (id_ativacao,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({"sucesso": False, "mensagem": "ID de ativação não encontrado."}), 404

    cursor.execute('''
        UPDATE usuarios
        SET senha_hash = ?, status_conta = 'Ativo'
        WHERE id_ativacao = ?
    ''', (senha_hash, id_ativacao))

    conn.commit()
    conn.close()

    return jsonify({"sucesso": True, "mensagem": "Conta ativada e senha atualizada com sucesso!"}), 200


@app.route('/api/profissionais', methods=['POST'])
def criar_profissional():
    data = request.json

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT COUNT(*) FROM profissionais")
        total_profissionais = cursor.fetchone()[0] + 1

        id_ativacao = f"ELEVA-PRO-{str(total_profissionais).zfill(2)}"
        email_fake = f"pro{total_profissionais}@eleva.com"
        senha_padrao = generate_password_hash("123456")

        cursor.execute('''
            INSERT INTO profissionais (
                nome, profissao, categoria, regiao, instituicao, nota,
                avaliacoes_qtd, servicos_qtd, sobre_mim, habilidades,
                preco_inicial, preco_diaria, preco_orcamento, review_recente,
                review_autor, taxa_comparecimento, taxa_resposta, clientes_recorrentes, status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('nome'),
            data.get('profissao'),
            data.get('categoria', 'Geral'),
            data.get('regiao', 'Não informado'),
            data.get('instituicao'),
            0, 0, 0,
            data.get('sobre_mim', 'Profissional cadastrado recentemente.'),
            data.get('habilidades', 'Não informado'),
            data.get('preco_inicial', '80,00'),
            data.get('preco_diaria', '200,00'),
            'Combinado via Chat',
            'Novo profissional na plataforma.',
            'Sistema Eleva',
            '100%', '100%', '0', 'Ativo'
        ))

        cursor.execute('''
            INSERT INTO usuarios (nome, email, senha_hash, tipo, id_ativacao, status_conta)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (data.get('nome'), email_fake, senha_padrao, 'profissional', id_ativacao, 'Ativo'))



        conn.commit()

        return jsonify({
            "sucesso": True,
            "mensagem": "Profissional criado com sucesso!",
            "login": id_ativacao,
            "senha_padrao": "123456"
        }), 201

    except Exception as e:
        return jsonify({"sucesso": False, "erro": str(e)}), 400
    finally:
        conn.close()


# ==========================================
# NOVAS ROTAS DE GERENCIAMENTO INSTITUCIONAL
# ==========================================

@app.route('/api/instituicoes/profissionais/<nome_instituicao>', methods=['GET'])
def listar_profissionais_instituicao(nome_instituicao):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM profissionais WHERE instituicao = ? ORDER BY id DESC', (nome_instituicao,))
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])


@app.route('/api/profissionais/<int:prof_id>', methods=['PUT'])
def atualizar_profissional(prof_id):
    data = request.json
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT nome FROM profissionais WHERE id = ?', (prof_id,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            return jsonify({"sucesso": False, "mensagem": "Profissional não encontrado."}), 404
        nome_antigo = row[0]

        cursor.execute('''
            UPDATE profissionais
            SET nome = ?, profissao = ?, categoria = ?, regiao = ?, sobre_mim = ?,
                habilidades = ?, preco_inicial = ?, preco_diaria = ?, status = ?
            WHERE id = ?
        ''', (
            data.get('nome'),
            data.get('profissao'),
            data.get('categoria'),
            data.get('regiao'),
            data.get('sobre_mim'),
            data.get('habilidades'),
            data.get('preco_inicial'),
            data.get('preco_diaria'),
            data.get('status', 'Ativo'),
            prof_id
        ))

        cursor.execute('''
            UPDATE usuarios
            SET nome = ?
            WHERE nome = ? AND tipo = 'profissional'
        ''', (data.get('nome'), nome_antigo))

        conn.commit()
        return jsonify({"sucesso": True, "mensagem": "Profissional atualizado com sucesso!"}), 200
    except Exception as e:
        return jsonify({"sucesso": False, "mensagem": f"Erro ao atualizar: {str(e)}"}), 500
    finally:
        conn.close()


@app.route('/api/profissionais/<int:prof_id>', methods=['DELETE'])
def deletar_profissional(prof_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT nome FROM profissionais WHERE id = ?', (prof_id,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            return jsonify({"sucesso": False, "mensagem": "Profissional não encontrado."}), 404
        nome_profissional = row[0]

        cursor.execute('DELETE FROM profissionais WHERE id = ?', (prof_id,))
        cursor.execute('DELETE FROM usuarios WHERE nome = ? AND tipo = "profissional"', (nome_profissional,))

        conn.commit()
        return jsonify({"sucesso": True, "mensagem": "Profissional excluído definitivamente com sucesso!"}), 200
    except Exception as e:
        return jsonify({"sucesso": False, "mensagem": f"Erro ao excluir: {str(e)}"}), 500
    finally:
        conn.close()


# ==========================================
# ROTAS PADRÕES DO SISTEMA (PRESERVADAS)
# ==========================================

@app.route('/api/chat', methods=['POST'])
def enviar_mensagem():
    data = request.json
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO mensagens (sala, remetente, texto) VALUES (?, ?, ?)',
                   (data['sala'], data['remetente'], data['texto']))
    conn.commit()
    conn.close()
    return jsonify({"sucesso": True}), 201

@app.route('/api/chat/<sala>', methods=['GET'])
def ler_mensagens(sala):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM mensagens WHERE sala = ? ORDER BY id ASC', (sala,))
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/api/profissionais', methods=['GET'])
def listar_profissionais():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    # Retorna apenas profissionais ativos na tela de busca principal
    cursor.execute("SELECT * FROM profissionais WHERE status = 'Ativo' ORDER BY nota DESC")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/api/profissionais/<int:prof_id>', methods=['GET'])
def obtener_profissional(prof_id):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM profissionais WHERE id = ?', (prof_id,))
    row = cursor.fetchone()
    conn.close()
    return jsonify(dict(row)), 200 if row else 404

@app.route('/api/instituicoes', methods=['GET'])
def listar_instituicoes():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT nome, email FROM usuarios WHERE tipo = 'instituicao' ORDER BY nome ASC")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/api/solicitacoes', methods=['POST'])
def nova_solicitacao():
    data = request.json
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM solicitacoes WHERE profissional_nome=? AND nome_cliente=? AND status='Pendente'",
                   (data['profissional_nome'], data['nome_cliente']))
    if not cursor.fetchone():
        cursor.execute('''INSERT INTO solicitacoes (profissional_nome, nome_cliente, whatsapp, data_servico, endereco, detalhes, status)
                          VALUES (?, ?, 'Chat', 'A definir', 'A definir', 'Negociação iniciada', 'Pendente')''',
                       (data['profissional_nome'], data['nome_cliente']))
        conn.commit()
    conn.close()
    return jsonify({"sucesso": True}), 201

@app.route('/api/solicitacoes/<profissional_nome>', methods=['GET'])
def ver_solicitacoes(profissional_nome):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM solicitacoes WHERE profissional_nome = ? ORDER BY id DESC", (profissional_nome,))
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/api/pagar', methods=['POST'])
def confirmar_pagamento():
    data = request.json
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    token_servico = str(random.randint(1000, 9999))

    cursor.execute('''
        UPDATE solicitacoes
        SET status = 'Pago (Retido)', detalhes = ?, codigo_verificacao = ?
        WHERE profissional_nome = ? AND nome_cliente = ? AND status = 'Pendente'
    ''', (f"Valor retido: R$ {data['valor']}", token_servico, data['profissional_nome'], data['nome_cliente']))
    conn.commit()
    conn.close()
    return jsonify({"sucesso": True, "token": token_servico}), 200

@app.route('/api/servico/iniciar', methods=['POST'])
def iniciar_servico():
    data = request.json
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id FROM solicitacoes
        WHERE id = ? AND codigo_verificacao = ? AND status = 'Pago (Retido)'
    ''', (data['solicitacao_id'], data['codigo']))

    if cursor.fetchone():
        cursor.execute("UPDATE solicitacoes SET status = 'Em Andamento' WHERE id = ?", (data['solicitacao_id'],))
        conn.commit()
        conn.close()
        return jsonify({"sucesso": True, "mensagem": "Serviço iniciado com sucesso!"}), 200
    else:
        conn.close()
        return jsonify({"sucesso": False, "mensagem": "Código de verificação incorreto!"}), 400

@app.route('/api/servico/concluir', methods=['POST'])
def concluir_servico():
    data = request.json
    nota = data.get('nota', 5)
    comentario = data.get('comentario', '')

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE solicitacoes
        SET status = 'Concluído', nota = ?, comentario = ?
        WHERE id = ?
    ''', (nota, comentario, data['solicitacao_id']))

    conn.commit()
    conn.close()
    return jsonify({"sucesso": True, "mensagem": "Serviço finalizado e avaliado com sucesso!"}), 200

@app.route('/api/ganhos/<profissional_nome>', methods=['GET'])
def ver_ganhos(profissional_nome):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT status, detalhes FROM solicitacoes WHERE profissional_nome = ?", (profissional_nome,))
    rows = cursor.fetchall()
    conn.close()

    saldo_retido = 0.0
    saldo_disponivel = 0.0

    for row in rows:
        if 'Valor retido: R$ ' in row['detalhes']:
            try:
                valor_str = row['detalhes'].split('R$ ')[1].replace(',', '.')
                valor_base_profissional = float(valor_str)

                if row['status'] == 'Pago (Retido)':
                    saldo_retido += valor_base_profissional
                elif row['status'] == 'Concluído':
                    saldo_disponivel += valor_base_profissional
            except:
                pass

    return jsonify({
        "saldo_retido": saldo_retido,
        "taxa_ong_retida": saldo_retido * 0.10,
        "saldo_disponivel": saldo_disponivel,
        "taxa_ong_disponivel": saldo_disponivel * 0.10
    })

@app.route('/api/solicitacoes/cliente/<nome_cliente>', methods=['GET'])
def ver_solicitacoes_cliente(nome_cliente):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM solicitacoes WHERE nome_cliente = ? ORDER BY id DESC", (nome_cliente,))
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/api/usuarios/foto', methods=['POST'])
def salvar_foto():
    data = request.json
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE usuarios SET foto = ? WHERE nome = ?", (data.get('foto'), data.get('nome')))
        cursor.execute("UPDATE profissionais SET foto = ? WHERE nome = ?", (data.get('foto'), data.get('nome')))  
        conn.commit()
        return jsonify({"sucesso": True}), 200
    except Exception as e:
        return jsonify({"sucesso": False}), 500
    finally:
        conn.close()

@app.route('/api/usuarios/foto/<nome>', methods=['GET'])
def carregar_foto(nome):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT foto FROM usuarios WHERE nome = ?", (nome,))
    resultado = cursor.fetchone()
    conn.close()

    if resultado and resultado[0]:
        return jsonify({"sucesso": True, "foto": resultado[0]}), 200
    return jsonify({"sucesso": False, "foto": None}), 404

@app.route('/api/usuarios/deletar', methods=['DELETE'])
def deletar_conta():
    data = request.json
    nome_usuario = data.get('nome')

    if not nome_usuario:
        return jsonify({"sucesso": False, "mensagem": "Nome do usuário não fornecido."}), 400

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM usuarios WHERE nome = ?", (nome_usuario,))
        cursor.execute("DELETE FROM solicitacoes WHERE nome_cliente = ?", (nome_usuario,))
        conn.commit()
        return jsonify({"sucesso": True, "mensagem": "Conta apagada com sucesso."}), 200
    except Exception as e:
        return jsonify({"sucesso": False, "mensagem": f"Erro interno: {str(e)}"}), 500
    finally:
        conn.close()
init_db()
if __name__ == '__main__':

    app.run(debug=True, port=5000)
