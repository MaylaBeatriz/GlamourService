from flask import Flask, render_template, request, redirect, url_for, jsonify
from database import conectar

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')


# ------------------------- ROTAS DE PÁGINAS -------------------------------- #

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/contato")
def contato():
    return render_template("contato.html")

@app.route("/form_orcamento")
def form_orcamento():
    return render_template("form_orcamento.html")

@app.route("/areadocliente")
def areadocliente():
    return render_template("areadocliente.html")

@app.route("/administrativo")
def administrativo():
    return render_template("administrativo.html")

@app.route("/cliente")
def cliente():
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT id, nome_cliente, email_cliente, telefone_cliente FROM cliente")
    clientes = cur.fetchall()
    con.close()
    return render_template("cliente.html", clientes=clientes)

@app.route("/evento")
def evento():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT * FROM eventos")
    eventos = cur.fetchall()
    conn.close()
    return render_template("evento.html", eventos=eventos)

@app.route("/fornecedor")
def fornecedor():
    return render_template("fornecedor.html")

@app.route("/orcamento")
def orcamento():
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT * FROM orcamento")
    orcamentos = cur.fetchall()
    con.close()
    return render_template("orcamento.html", orcamentos=orcamentos)

@app.route("/login_cliente")
def login_cliente():
    return render_template("login_cliente.html")

@app.route("/funcionario")
def funcionario():
    # Carregar a lista de funcionários do banco para exibição
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT id, nome_funcionario, email_funcionario, telefone_funcionario, especialidade FROM funcionario")
    funcionarios = cur.fetchall()
    con.close()

    return render_template("funcionario.html", funcionarios=funcionarios)

@app.route("/escala")
def escala():
    con = conectar()
    cur = con.cursor()
    cur.execute("""
        SELECT escala.id, evento.titulo_evento, escala.data_turno, escala.inicio_turno, escala.fim_turno
        FROM escala JOIN eventos as evento ON escala.id_evento = evento.id
    """)
    escalas = cur.fetchall()

    cur.execute("SELECT id, nome_funcionario FROM funcionario")
    funcionarios = cur.fetchall()

    cur.execute("SELECT id, titulo_evento FROM eventos")
    eventos = cur.fetchall()

    con.close()
    return render_template("escala.html", escalas=escalas, funcionarios=funcionarios, eventos=eventos)


# -------------------------- ROTAS DE AÇÕES CRUD ---------------------------- #

# Criar funcionário
@app.route("/add_funcionario", methods=["POST"])
def add_funcionario():
    dados = request.get_json()
    nome = dados.get("nome")
    email = dados.get("email")
    telefone = dados.get("telefone")
    especialidade = dados.get("especialidade")

    con = conectar()
    cur = con.cursor()
    # O id_usuario está fixo como 1, idealmente viria de um sistema de login
    cur.execute("""
        INSERT INTO funcionario (id_usuario, nome_funcionario, telefone_funcionario, email_funcionario, especialidade)
        VALUES (1, ?, ?, ?, ?)""", (nome, telefone, email, especialidade))
    con.commit()
    id_funcionario = cur.lastrowid
    cur.execute("SELECT * FROM funcionario WHERE id = ?", (id_funcionario,))
    novo_funcionario = cur.fetchone()
    con.close()

    return jsonify({'status': 'success', 'funcionario': novo_funcionario}), 201

# Atualizar funcionário
@app.route("/update_funcionario/<int:id>", methods=["POST"])
def update_funcionario(id):
    nome = request.form.get("nome")
    email = request.form.get("email")
    telefone = request.form.get("telefone")
    especialidade = request.form.get("especialidade")

    con = conectar()
    cur = con.cursor()
    cur.execute("""
        UPDATE funcionario
        SET nome_funcionario = ?, email_funcionario = ?, telefone_funcionario = ?, especialidade = ?
        WHERE id = ?
    """, (nome, email, telefone, especialidade, id))
    con.commit()

    cur.execute("SELECT * FROM funcionario WHERE id = ?", (id,))
    funcionario_atualizado = cur.fetchone()

    con.close()

    return jsonify({'status': 'success', 'funcionario': funcionario_atualizado}), 200

# Deletar funcionário
@app.route("/delete_funcionario/<int:id>", methods=["POST"])
def delete_funcionario(id):
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM funcionario WHERE id = ?", (id,))
    con.commit()
    con.close()
    return redirect(url_for("funcionario"))

# Deletar orçamento
@app.route("/delete_orcamento/<int:id>", methods=["POST"])
def delete_orcamento(id):
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM orcamento WHERE id = ?", (id,))
    con.commit()
    con.close()
    return redirect(url_for("orcamento"))


# Criar orçamento
@app.route("/add_orcamento", methods=["POST"])
def add_orcamento():
    dados = request.get_json()
    nome_cliente = dados.get("nome_cliente")
    email_cliente = dados.get("email_cliente")
    telefone_cliente = dados.get("telefone_cliente")
    data_evento = dados.get("data_evento")
    hora_evento = dados.get("hora_evento")
    tipo_evento = dados.get("tipo_evento")
    qtde_convidados = dados.get("qtde_convidados")
    endereco_evento = dados.get("endereco_evento")

    con = conectar()
    cur = con.cursor()
    cur.execute("""
        INSERT INTO orcamento (id_contrato, nome_cliente, email_cliente, telefone_cliente, data_evento, hora_evento, tipo_evento, qtde_convidados, endereco_evento)
        VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?)""", 
        (nome_cliente, email_cliente, telefone_cliente, data_evento, hora_evento, tipo_evento, qtde_convidados, endereco_evento)
    ) # id_contrato temporário
    con.commit()
    id_orcamento = cur.lastrowid
    con.close()

    return jsonify({'status': 'success', 'id': id_orcamento}), 201


# Criar escala
@app.route("/add_escala", methods=["POST"])
def add_escala():
    dados = request.get_json()
    id_evento = dados.get("id_evento")
    data_turno = dados.get("data_turno")
    inicio_turno = dados.get("inicio_turno")
    fim_turno = dados.get("fim_turno")
    funcionarios_ids = dados.get("funcionarios")

    con = conectar()
    cur = con.cursor()

    cur.execute("INSERT INTO escala(id_evento, data_turno, inicio_turno, fim_turno) VALUES (?, ?, ?, ?)", (id_evento, data_turno, inicio_turno, fim_turno))
    id_escala = cur.lastrowid

    if funcionarios_ids:
        for f_id in funcionarios_ids:
            cur.execute("INSERT INTO escala_funcionario(id_escala, id_funcionario) VALUES (?, ?)", (id_escala, f_id))
    
    con.commit()

    cur.execute("""
        SELECT escala.id, evento.titulo_evento, escala.data_turno, escala.inicio_turno, escala.fim_turno
        FROM escala JOIN eventos as evento ON escala.id_evento = evento.id
        WHERE escala.id = ?
    """, (id_escala,))
    nova_escala = cur.fetchone()

    con.close()

    return jsonify({'status': 'success', 'escala': nova_escala}), 201

# Deletar escala
@app.route("/delete_escala/<int:id>", methods=["POST"])
def delete_escala(id):
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM escala WHERE id = ?", (id,))
    con.commit()
    con.close()
    return redirect(url_for("escala"))

# Atualizar escala
@app.route("/update_escala/<int:id>", methods=["POST"])
def update_escala(id):
    dados = request.get_json()
    id_evento = dados.get("id_evento")
    data_turno = dados.get("data_turno")
    inicio_turno = dados.get("inicio_turno")
    fim_turno = dados.get("fim_turno")

    con = conectar()
    cur = con.cursor()
    cur.execute("""
        UPDATE escala
        SET id_evento = ?, data_turno = ?, inicio_turno = ?, fim_turno = ?
        WHERE id = ?
    """, (id_evento, data_turno, inicio_turno, fim_turno, id))
    con.commit()

    cur.execute("""
        SELECT escala.id, evento.titulo_evento, escala.data_turno, escala.inicio_turno, escala.fim_turno
        FROM escala JOIN eventos as evento ON escala.id_evento = evento.id
        WHERE escala.id = ?
    """, (id,))
    escala_atualizada = cur.fetchone()

    con.close()

    return jsonify({'status': 'success', 'escala': escala_atualizada})


# Criar evento
@app.route('/add_evento', methods=['POST'])
def add_evento():
    dados = request.get_json()
    conn = conectar()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO eventos (titulo_evento, data_evento, tipo_evento, num_convidados, endereco_evento, nome_cliente, email_cliente, telefone_cliente) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (dados['titulo_evento'], dados['data_evento'], dados['tipo_evento'], dados['num_convidados'], dados['endereco_evento'], dados['nome_cliente'], dados['email_cliente'], dados['telefone_cliente']))
    conn.commit()
    id_evento = cur.lastrowid
    cur.execute("SELECT * FROM eventos WHERE id = ?", (id_evento,))
    novo_evento = cur.fetchone()
    conn.close()
    return jsonify({'status': 'success', 'evento': novo_evento}), 201

# Atualizar evento
@app.route('/update_evento/<int:id>', methods=['POST'])
def update_evento(id):
    dados = request.get_json()
    conn = conectar()
    cur = conn.cursor()
    cur.execute(
        """UPDATE eventos SET 
           titulo_evento = ?, data_evento = ?, tipo_evento = ?, num_convidados = ?, 
           endereco_evento = ?, nome_cliente = ?, email_cliente = ?, telefone_cliente = ?
           WHERE id = ?""",
        (dados['titulo_evento'], dados['data_evento'], dados['tipo_evento'], dados['num_convidados'], 
         dados['endereco_evento'], dados['nome_cliente'], dados['email_cliente'], dados['telefone_cliente'], id)
    )
    conn.commit()

    cur.execute("SELECT * FROM eventos WHERE id = ?", (id,))
    evento_atualizado = cur.fetchone()

    conn.close()
    return jsonify({'status': 'success', 'evento': evento_atualizado}), 200

# Deletar evento
@app.route('/delete_evento/<int:id>', methods=['POST'])
def delete_evento(id):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("DELETE FROM eventos WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('evento'))


# ----------------------- RODAR SERVIDOR ----------------------- #
if __name__ == "__main__":
    app.run(debug=True)
