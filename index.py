from flask import Flask, render_template, request, redirect, flash, url_for, send_file
from modelo.modelo import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/login')
def login():
    return render_template('loginEstudiante.html')


@app.route('/proyectos_disponibles')
def proyectos_disponibles():
    return render_template('proyectos_disponibles.html')


@app.route('/guardar_datos', methods=['POST'])
def guardar_datos():
    nombre_completo = request.form['nombreCompleto']
    correo_electronico = request.form['correoElectronico']
    contrasena = request.form['contrasena']
    area_conocimiento = request.form['areaConocimiento']
    disciplina = request.form['disciplina']
    subdisciplina = request.form['subdisciplina']

    # Puedes guardar los datos en una base de datos aquí, o realizar cualquier otra acción necesaria
    vector_doctores = llamaModelo([area_conocimiento, disciplina, subdisciplina])
    # Luego, renderiza una nueva plantilla con los datos guardados
    return render_template('doctores.html', doctores=vector_doctores)



app.run(host='0.0.0.0', port=81)
