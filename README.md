# Glamour Service

Projeto desenvolvido para gerenciamento de eventos com garçons e bartenders.  
O sistema permite organizar clientes, funcionários, eventos, escalas e orçamentos.

## Funcionalidades do Sistema
- Página inicial institucional
- Página de contato
- Área do cliente (visualização de orçamentos e contratos)
- Área administrativa
- CRUD de clientes, funcionários, eventos e orçamentos
- Escalas com seleção de funcionários e horários
- Controle financeiro básico

## Tecnologias Utilizadas
- HTML
- CSS
- JavaScript
- MySQL

## Como Executar
1. Abra o arquivo **index.html** no navegador.
2. Para uso com banco de dados futuramente, será necessária integração com backend.

## Autores
- Yslla Gonçalves  
- Mayla Rocha  
- Irlane  

---

© Glamour Service

### Windows (PowerShell)

```powershell

# 1- instalar o Python
# 2 - Instalar o  VS Code

python -m venv .venv # 3 - criar ambiente virtual

.venv/scripts/activate # 4 - Ativar ambiente virtual

pip install flask # 5 - Instalar o Flask

python db_smarteventos.py   # 6 - cria/zera o banco db_smarteventos.db

python app.py       # 7 - Rodar o software - inicia o servidor

# Obs: Para parar o servidor CTRL + C