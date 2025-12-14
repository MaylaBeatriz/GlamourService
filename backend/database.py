import sqlite3

DATABASE = 'db_siteGlamour.db'

def conectar():
    con = sqlite3.connect(DATABASE, check_same_thread=False)
    con.row_factory = sqlite3.Row
    return con
