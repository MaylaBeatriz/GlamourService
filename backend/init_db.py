import sqlite3 as sql

# Criar a conexão com o banco de dados (ou criar o banco se não existir)
con = sql.connect('db_siteGlamour.db')
cur = con.cursor()

# Apagar tabelas existentes
cur.execute("DROP TABLE IF EXISTS escala_funcionario")
cur.execute("DROP TABLE IF EXISTS escala")
cur.execute("DROP TABLE IF EXISTS eventos")
cur.execute("DROP TABLE IF EXISTS orcamento")
cur.execute("DROP TABLE IF EXISTS funcionario")
cur.execute("DROP TABLE IF EXISTS usuario")
cur.execute('DROP TABLE IF EXISTS historico_servico')
cur.execute('DROP TABLE IF EXISTS pagamento')
cur.execute('DROP TABLE IF EXISTS orcamento')
cur.execute('DROP TABLE IF EXISTS contrato')
cur.execute('DROP TABLE IF EXISTS eventos')
cur.execute('DROP TABLE IF EXISTS funcionario')
cur.execute('DROP TABLE IF EXISTS cliente')
cur.execute('DROP TABLE IF EXISTS usuario')

# Criar a tabela usuario com os campos
sql_usuario = '''CREATE TABLE usuario (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email VARCHAR(150) NOT NULL UNIQUE,
  senha VARCHAR(255) NOT NULL,
  role TEXT NOT NULL CHECK(role IN ('Administrador','Financeiro','Coordenador','Cliente','Funcionario')),
  criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
)'''
cur.execute(sql_usuario)

# Criar a tabela cliente com os campos
sql_cliente = '''CREATE TABLE cliente (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  id_usuario INT NOT NULL,
  nome_cliente VARCHAR(200) NOT NULL,
  email_cliente VARCHAR(150) NOT NULL,
  telefone_cliente VARCHAR(30) NOT NULL,
  FOREIGN KEY (id_usuario) REFERENCES usuario(id) ON DELETE CASCADE
)'''
cur.execute(sql_cliente)

# Criar a tabela funcionario com os campos
sql_funcionarios = '''CREATE TABLE funcionario (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  id_usuario INT NOT NULL,
  nome_funcionario VARCHAR(200) NOT NULL,
  telefone_funcionario VARCHAR(30) NOT NULL,
  email_funcionario VARCHAR(150) NOT NULL,
  especialidade TEXT CHECK(especialidade IN ('Garcom','Bartender')),
  FOREIGN KEY (id_usuario) REFERENCES usuario(id) ON DELETE CASCADE
)'''
cur.execute(sql_funcionarios)

# Criar a tabela eventos com os campos
sql_eventos = '''CREATE TABLE eventos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  titulo_evento TEXT NOT NULL,
  data_evento DATE NOT NULL,
  tipo_evento TEXT,
  num_convidados INTEGER,
  endereco_evento TEXT,
  nome_cliente TEXT,
  email_cliente TEXT,
  telefone_cliente TEXT
)'''
cur.execute(sql_eventos)

# Criar a tabela contrato com os campos
sql_contrato = '''CREATE TABLE contrato (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  id_cliente INT NOT NULL,
  data_inicio DATE NOT NULL,
  data_fim DATE NOT NULL,
  status TEXT DEFAULT 'Aberto' CHECK(status IN ('Aberto','Fechado')),
  FOREIGN KEY (id_cliente) REFERENCES cliente(id) ON DELETE CASCADE
)'''
cur.execute(sql_contrato)

# Criar a tabela orcamento com os campos
sql_orcamento = '''CREATE TABLE orcamento (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  id_contrato INT NOT NULL,
  nome_cliente VARCHAR(150) NOT NULL,
  email_cliente VARCHAR(150) NOT NULL,
  telefone_cliente VARCHAR(30) NOT NULL,
  data_evento DATE NOT NULL,
  hora_evento TIME NOT NULL,
  tipo_evento VARCHAR(100) NOT NULL,
  qtde_convidados INT NOT NULL,
  endereco_evento VARCHAR(255) NOT NULL,
  FOREIGN KEY (id_contrato) REFERENCES contrato(id) ON DELETE CASCADE
)'''
cur.execute(sql_orcamento)

# Criar a tabela pagamento com os campos
sql_pagamento = '''CREATE TABLE pagamento (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  id_orcamento INT NOT NULL,
  data_pagamento DATE,
  valor DECIMAL(10,2),
  metodo TEXT CHECK(metodo IN ('Boleto','Cartao','Transferencia')),
  status TEXT DEFAULT 'Pendente' CHECK(status IN ('Pendente','Confirmado','Estornado')),
  FOREIGN KEY (id_orcamento) REFERENCES orcamento(id) ON DELETE CASCADE
)'''
cur.execute(sql_pagamento)

# Criar a tabela escala com os campos
sql_escala = '''CREATE TABLE escala (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_evento INTEGER,
    data_turno DATE NOT NULL,
    inicio_turno TIME NOT NULL,
    fim_turno TIME NOT NULL,
    FOREIGN KEY (id_evento) REFERENCES eventos(id)
)'''
cur.execute(sql_escala)

# Criar a tabela escala_funcionario com os campos
sql_escala_funcionario = '''CREATE TABLE escala_funcionario (
  id_escala INT NOT NULL,
  id_funcionario INT NOT NULL,
  confirmado INTEGER DEFAULT 0,
  PRIMARY KEY (id_escala, id_funcionario),
  FOREIGN KEY (id_escala) REFERENCES escala(id) ON DELETE CASCADE,
  FOREIGN KEY (id_funcionario) REFERENCES funcionario(id) ON DELETE CASCADE
)'''
cur.execute(sql_escala_funcionario)

# Criar a tabela historico_servico com os campos
sql_historico_servico = '''CREATE TABLE historico_servico (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  id_funcionario INT NOT NULL,
  evento_id INT,
  descricao TEXT,
  data_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (id_funcionario) REFERENCES funcionario(id) ON DELETE CASCADE,
  FOREIGN KEY (evento_id) REFERENCES eventos(id) ON DELETE SET NULL
)'''
cur.execute(sql_historico_servico)

# Salvar as alterações e fechar a conexão
con.commit()
con.close()

print("Banco de dados e tabelas criados com sucesso.")