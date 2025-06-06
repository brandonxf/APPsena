from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import re
import captcha

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
    return redirect(url_for('acceso'))

@app.route('/acceso', methods=['GET', 'POST'])
def acceso():
    error_login = None
    error_registro = None
    if request.method == 'POST':
        form_type = request.form.get('form_type')
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']
        if form_type == 'login':
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute('SELECT contrasena FROM usuarios WHERE usuario = ?', (usuario,))
            resultado = c.fetchone()
            conn.close()
            if resultado and check_password_hash(resultado[0], contrasena):
                session['usuario'] = usuario
                return redirect(url_for('index'))
            else:
                error_login = 'Usuario o contraseña incorrectos'
        elif form_type == 'registro':
            # Validar que el usuario sea un correo electrónico
            if not re.match(r"[^@]+@[^@]+\.[^@]+", usuario):
                error_registro = 'Ingrese un correo electrónico válido'
            else:
                # ...registro...
                contrasena_hash = generate_password_hash(contrasena)
                try:
                    conn = sqlite3.connect('users.db')
                    c = conn.cursor()
                    c.execute('INSERT INTO usuarios (usuario, contrasena) VALUES (?, ?)', (usuario, contrasena_hash))
                    conn.commit()
                    conn.close()
                    return redirect(url_for('acceso'))
                except:
                    error_registro = 'El usuario ya existe'
    return render_template('acceso.html', error_login=error_login, error_registro=error_registro)

captcha_image = captcha.generate_captcha()
@app.route('/captcha')
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
