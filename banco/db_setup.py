import sqlite3

# Configuração do banco de dados
db_connection = sqlite3.connect('estoque.db')
db_cursor = db_connection.cursor()

# Tabelas
db_cursor.execute("""
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    categoria_id INTEGER,
    quantidade INTEGER NOT NULL,
    preco REAL NOT NULL,
    localizacao TEXT,
    FOREIGN KEY (categoria_id) REFERENCES categorias (id)
)
""")

db_cursor.execute("""
CREATE TABLE IF NOT EXISTS categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
)
""")

db_cursor.execute("""
CREATE TABLE IF NOT EXISTS movimentacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id INTEGER NOT NULL,
    tipo TEXT NOT NULL,
    quantidade INTEGER NOT NULL,
    data TEXT NOT NULL,
    FOREIGN KEY (produto_id) REFERENCES produtos (id)
)
""")

db_connection.commit()
