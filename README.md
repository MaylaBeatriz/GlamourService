# Glamour Service

Sistema web para gerenciar uma empresa de garçons e bartenders para eventos. Ele organiza clientes, funcionários, eventos, orçamentos e escalas de trabalho, com uma área institucional para o público e uma área administrativa para a equipe.

Projeto desenvolvido em equipe no programa **Transforme-se 2025**, da Serasa Experian em parceria com a Gerando Falcões.

## Funcionalidades

- Página inicial institucional e página de contato
- Formulário de pedido de orçamento
- Área do cliente
- Área administrativa com cadastro, edição e exclusão (CRUD) de:
  - funcionários (garçons e bartenders)
  - eventos
  - orçamentos
  - escalas de trabalho, com seleção dos funcionários de cada turno
- Listagem de clientes

## Tecnologias

- **Backend:** Python e Flask
- **Banco de dados:** SQLite
- **Frontend:** HTML, CSS e JavaScript (templates Jinja2)

## Banco de dados

Banco relacional em SQLite, criado pelo script `backend/init_db.py`. Principais tabelas:

| Tabela | O que guarda |
|---|---|
| `usuario` | login e perfil de acesso (Administrador, Financeiro, Coordenador, Cliente, Funcionário) |
| `cliente` | dados dos clientes, ligados a um usuário |
| `funcionario` | garçons e bartenders, ligados a um usuário |
| `eventos` | eventos com data, tipo, número de convidados e endereço |
| `contrato` | contratos dos clientes, com status aberto ou fechado |
| `orcamento` | pedidos de orçamento ligados a um contrato |
| `pagamento` | pagamentos de cada orçamento (boleto, cartão ou transferência) |
| `escala` | turnos de trabalho de cada evento |
| `escala_funcionario` | quais funcionários trabalham em cada turno |

As relações usam chaves estrangeiras com exclusão em cascata, e os campos com valores fixos (perfil, especialidade, status, forma de pagamento) são validados com `CHECK`.

## Estrutura

```
GlamourService/
├── backend/
│   ├── app.py          # rotas e regras do sistema (Flask)
│   ├── database.py     # conexão com o SQLite
│   ├── init_db.py      # cria as tabelas do banco
│   ├── seed_db.py      # popula o banco com dados de exemplo
│   └── db_siteGlamour.db
└── frontend/
    ├── templates/      # páginas HTML
    └── static/         # CSS, JavaScript e imagens
```

## Como executar

Pré-requisito: Python 3 instalado.

```bash
cd backend

# criar e ativar o ambiente virtual
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/macOS

# instalar o Flask
pip install flask

# (opcional) recriar o banco do zero e popular com dados de exemplo
python init_db.py
python seed_db.py

# rodar o servidor
python app.py
```

Depois acesse `http://127.0.0.1:5000` no navegador. Para parar o servidor, use `Ctrl + C`.

O repositório já inclui o banco `db_siteGlamour.db` populado, então os passos de recriar o banco são opcionais. Rode os comandos de dentro da pasta `backend`, porque o caminho do banco é relativo a ela.

## Autoras

- **Mayla Rocha** – modelagem básica do banco de dados
- **Yslla Gonçalves**
- **Irlane Silva Santos**
