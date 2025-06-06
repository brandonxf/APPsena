import sqlite3

# Conectar o crear base de datos
conn = sqlite3.connect('usuarios.db')
cursor = conn.cursor()

# Crear tabla de usuarios
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')

# Insertar un usuario de prueba
cursor.execute('''
INSERT OR IGNORE INTO usuarios (username, password)
VALUES (?, ?)
''', ('admin', '1234'))

conn.commit()
conn.close()

print("Base de datos y usuario creados correctamente.")
