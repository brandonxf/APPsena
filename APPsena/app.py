from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'clave-secreta'

# Crear tabla si no existe
def crear_tabla():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE,
            contrasena TEXT
        )
    ''')
    conn.commit()
    conn.close()

crear_tabla()

@app.route('/')
def index():
    if 'usuario' in session:
        return f'Hola, {session["usuario"]}! <a href="/logout">Cerrar sesión</a>'
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('SELECT contrasena FROM usuarios WHERE usuario = ?', (usuario,))
        resultado = c.fetchone()
        conn.close()
        if resultado and check_password_hash(resultado[0], contrasena):
            session['usuario'] = usuario
            return redirect(url_for('index'))
        else:
            return 'Usuario o contraseña incorrectos'
    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = generate_password_hash(request.form['contrasena'])
        try:
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute('INSERT INTO usuarios (usuario, contrasena) VALUES (?, ?)', (usuario, contrasena))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except:
            return 'El usuario ya existe'
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
