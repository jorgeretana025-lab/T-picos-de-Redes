from fastapi import FastAPI
from typing import List
from pydantic import BaseModel
import statistics
import sqlite3

app = FastAPI()

"""
Modelos
"""
class Calificacion(BaseModel):
    materia: str
    nota: float

class Estudiante(BaseModel):
    nombre: str
    calificacion: List[Calificacion]

"""
Base de datos simulada (datos iniciales)
"""
db = [
    Estudiante(
        nombre="Jorge",
        calificacion=[
            Calificacion(materia="Historia", nota=9),
            Calificacion(materia="Geografia", nota=10),
            Calificacion(materia="Ciencias", nota=8)
        ]
    ),
    Estudiante(
        nombre="Armando",
        calificacion=[
            Calificacion(materia="Historia", nota=6),
            Calificacion(materia="Geografia", nota=7),
            Calificacion(materia="Ciencias", nota=8)
        ]
    )
]

"""
SQLite
"""
def get_db():
    return sqlite3.connect("base_de_datos.db")

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS estudiantes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS calificaciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        estudiante_id INTEGER,
        materia TEXT,
        nota REAL,
        FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id)
    )
    ''')

    conn.commit()
    conn.close()

"""
Insertar datos iniciales SOLO si está vacío
"""
def insertar_datos_iniciales():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM estudiantes")
    if cursor.fetchone()[0] == 0:
        for estudiante in db:
            cursor.execute(
                "INSERT INTO estudiantes (nombre) VALUES (?)",
                (estudiante.nombre,)
            )
            estudiante_id = cursor.lastrowid

            for calificacion in estudiante.calificacion:
                cursor.execute(
                    "INSERT INTO calificaciones (estudiante_id, materia, nota) VALUES (?, ?, ?)",
                    (estudiante_id, calificacion.materia, calificacion.nota)
                )

    conn.commit()
    conn.close()

init_db()
insertar_datos_iniciales()

"""
Funcion de IA simple
"""
def evaluar_desempeno(notas):
    promedio = statistics.mean(notas)

    if promedio >= 9:
        estado = "Excelente"
        recomendacion = "Puedes participar en proyecto"
    elif promedio >= 7:
        estado = "Regular"
        recomendacion = "Necesitas reforzar algunos temas"
    else:
        estado = "En riesgo"
        recomendacion = "Requiere tutorias urgentes"

    return {
        "promedio": promedio,
        "estado": estado,
        "recomendacion": recomendacion
    }

"""
Endpoints
"""
@app.get("/")
def inicio():
    return {"mensaje": "Servidor Inteligente de calificacion"}

@app.post("/estudiantes/")
def agregar_estudiantes(estudiante: Estudiante):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO estudiantes (nombre) VALUES (?)",
        (estudiante.nombre,)
    )
    estudiante_id = cursor.lastrowid

    for calificacion in estudiante.calificacion:
        cursor.execute(
            "INSERT INTO calificaciones (estudiante_id, materia, nota) VALUES (?, ?, ?)",
            (estudiante_id, calificacion.materia, calificacion.nota)
        )

    conn.commit()
    conn.close()

    return {"mensaje": "Estudiante agregado"}

@app.get("/estudiantes/")
def obtener_estudiantes():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
    SELECT estudiantes.nombre, calificaciones.materia, calificaciones.nota
    FROM estudiantes
    JOIN calificaciones ON estudiantes.id = calificaciones.estudiante_id
    ''')

    rows = cursor.fetchall()
    conn.close()

    return [
        {"nombre": r[0], "materia": r[1], "nota": r[2]}
        for r in rows
    ]