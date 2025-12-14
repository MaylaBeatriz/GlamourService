import sqlite3
import random
from datetime import date, time, timedelta

def conectar():
    return sqlite3.connect('db_siteGlamour.db')

def seed_data():
    con = conectar()
    cur = con.cursor()

    # --- Inserir 5 Usuários e Funcionários ---
    funcionarios = []
    for i in range(5):
        email = f'funcionario{i+1}@example.com'
        # Inserir usuário primeiro
        cur.execute("INSERT INTO usuario (email, senha, role) VALUES (?, ?, ?)", (email, 'senha123', 'Funcionario'))
        id_usuario = cur.lastrowid
        
        # Inserir funcionário
        nome = f'Funcionario {i+1}'
        telefone = f'99999-000{i+1}'
        especialidade = random.choice(['Garcom', 'Bartender'])
        cur.execute("INSERT INTO funcionario (id_usuario, nome_funcionario, telefone_funcionario, email_funcionario, especialidade) VALUES (?, ?, ?, ?, ?)",
                    (id_usuario, nome, telefone, email, especialidade))
        funcionarios.append(cur.lastrowid)

    # --- Inserir 5 Eventos ---
    eventos = []
    for i in range(5):
        titulo = f'Evento de Teste {i+1}'
        data_evento = (date.today() + timedelta(days=i*10)).isoformat()
        tipo = random.choice(['Casamento', 'Aniversário', 'Corporativo'])
        convidados = random.randint(50, 200)
        endereco = f'Rua Exemplo {i+1}, N 123'
        cliente = f'Cliente {i+1}'
        email_cliente = f'cliente{i+1}@teste.com'
        telefone_cliente = f'88888-000{i+1}'
        cur.execute("INSERT INTO eventos (titulo_evento, data_evento, tipo_evento, num_convidados, endereco_evento, nome_cliente, email_cliente, telefone_cliente) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (titulo, data_evento, tipo, convidados, endereco, cliente, email_cliente, telefone_cliente))
        eventos.append(cur.lastrowid)

    # --- Inserir 5 Orçamentos (associados a contratos fakes) ---
    # Primeiro, criar usuários e clientes para os contratos
    clientes_contrato = []
    for i in range(5):
        cur.execute("INSERT INTO usuario (email, senha, role) VALUES (?, ?, ?)", (f'clientect{i+1}@example.com', 'senha123', 'Cliente'))
        id_usuario_cliente = cur.lastrowid
        cur.execute("INSERT INTO cliente (id_usuario, nome_cliente, email_cliente, telefone_cliente) VALUES (?, ?, ?, ?)", (id_usuario_cliente, f'Cliente Contrato {i+1}', f'clientect{i+1}@example.com', f'77777-000{i+1}'))
        clientes_contrato.append(cur.lastrowid)

    # Criar contratos fakes
    contratos = []
    for cliente_id in clientes_contrato:
        cur.execute("INSERT INTO contrato (id_cliente, data_inicio, data_fim, status) VALUES (?, ?, ?, ?)", (cliente_id, date.today().isoformat(), (date.today() + timedelta(days=30)).isoformat(), 'Aberto'))
        contratos.append(cur.lastrowid)

    for i in range(5):
        data_orc = (date.today() + timedelta(days=i*5)).isoformat()
        hora_orc = time(hour=19, minute=0).strftime('%H:%M:%S')
        cur.execute("INSERT INTO orcamento (id_contrato, nome_cliente, email_cliente, telefone_cliente, data_evento, hora_evento, tipo_evento, qtde_convidados, endereco_evento) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (random.choice(contratos), f'Cliente Orcamento {i+1}', f'clienteorc{i+1}@teste.com', f'66666-000{i+1}', data_orc, hora_orc, 'Festa', random.randint(30, 100), f'Endereco Orcamento {i+1}'))

    # --- Inserir 5 Escalas ---
    for i in range(5):
        id_evento = random.choice(eventos)
        data_turno = (date.today() + timedelta(days=i*2)).isoformat()
        inicio_turno = time(hour=18, minute=0).strftime('%H:%M:%S')
        fim_turno = time(hour=23, minute=0).strftime('%H:%M:%S')
        cur.execute("INSERT INTO escala (id_evento, data_turno, inicio_turno, fim_turno) VALUES (?, ?, ?, ?)",
                    (id_evento, data_turno, inicio_turno, fim_turno))
        id_escala = cur.lastrowid
        # Associar um funcionário aleatório à escala
        id_funcionario = random.choice(funcionarios)
        cur.execute("INSERT INTO escala_funcionario (id_escala, id_funcionario) VALUES (?, ?)", (id_escala, id_funcionario))

    con.commit()
    con.close()
    print("Banco de dados populado com 5 registros de exemplo para cada tabela.")

if __name__ == '__main__':
    seed_data()
