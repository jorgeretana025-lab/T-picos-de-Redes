from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sqlite3
import statistics

app = FastAPI(title="Servidor Inteligente de Calificacion")

"""
Base de Datos (SQLite)
"""

def get_db():
    conn = sqlite3.connect("umb.db")
    return conn

def crear_tablas():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS estudiantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS calificaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            estudiante_id INTEGER,
            materia TEXT,
            nota REAL,
            FOREIGN KEY(estudiante_id) REFERENCES estudiantes(id)
        )
    """)
    
    conn.commit()
    conn.close()

crear_tablas()

"""
Modelos
"""

class Estudiante(BaseModel):
    nombre: str

class Calificacion(BaseModel):
    estudiante_id: int
    materia: str
    nota: float

"""
IA Simple
"""
def evaluar_desempeno(notas):
    if len(notas) == 0:
        return {"error": "Sin calificaciones"}
    
    promedio = statistics.mean(notas)

    if promedio >= 9:
        estado = "Excelente"
        recomendacion = "Puede participar en proyectos"

    elif promedio >= 7:
        estado = "Regular"
        recomendacion = "Debe reforzar algunos temas"

    else:
        estado = "En riesgo" 
        recomendacion = "Requiere tutorias"
        
    return {
        "promedio": round(promedio, 2),
        "estado": estado,
        "recomendacion": recomendacion
    }

"""
Endpoints
"""

@app.post("/estudiantes")
def agregar_estudiante(est: Estudiante):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO estudiantes (nombre) VALUES (?)", (est.nombre,))
    conn.commit()
    conn.close()

    return {"mensaje": "Estudiante agregado"}

@app.get("/estudiantes")
def ver_estudiantes():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM estudiantes")
    data = cursor.fetchall()
    conn.close()

    return {"estudiantes": data}

@app.post("/calificaciones")
def agregar_calificacion(cal: Calificacion):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO calificaciones (estudiante_id, materia, nota)
        VALUES (?, ?, ?)
    """, (cal.estudiante_id, cal.materia, cal.nota))

    conn.commit()
    conn.close()

    return {"mensaje": "Calificación agregada"}

@app.get("/calificaciones/{estudiante_id}")
def ver_calificaciones(estudiante_id: int):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT materia, nota FROM calificaciones
        WHERE estudiante_id = ?
    """, (estudiante_id,))

    data = cursor.fetchall()
    conn.close()

    return {"calificaciones": data}

@app.get("/evaluar/{estudiante_id}")
def evaluar_estudiante(estudiante_id: int):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT nota FROM calificaciones
        WHERE estudiante_id = ?
    """, (estudiante_id,))

    notas = [row[0] for row in cursor.fetchall()]
    conn.close()

    if not notas:
        raise HTTPException(status_code=404, detail="Estudiante sin calificaciones")

    resultado = evaluar_desempeno(notas)
    return resultado

