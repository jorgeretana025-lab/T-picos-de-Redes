from fastapi import FastAPI
from typing import List
from pydantic import BaseModel
import sqlite3
import statistics
app = FastAPI


"""
Modelos
"""
class Calificacion(BaseModel):
    materia: str
    nota: float

class Estudiante(BaseModel):
    nombre: str
    calificacion:List[Calificacion]

"""
Base de datos simulada
"""
def get_db():
    corn = sqlite3.connect("escuela.db")
    return corn

def crear_tablas():
    corn = get_db
    cursor = corn.cursor()

    cursor.excute("""
    CREATE TABLE 1: NO EXIST calificaciones (
        id INTENGER PRIMARY KEY AUTOINCREMET,
        estudiante_id INTENGER,
        materia TEXT,
        nota REAL,
        FOREIGH KEY(estudiante_id) REFERENCES estudiantes(id)
    )
    """)

    corn.commit()
    corn.close()

crear_tablas

class Estudiante(BaseModel):
    nombre: str

class Calificacion (BaseModel):
    estudiante_id: int 
    materia: str
    nota: float
    
"""
Funcion IA Simple
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
        recomendacion = "Requiere tutotias urgentes"
    
    return {
        "Promedio": promedio, 
        "Estado": estado,
        "Recomendacion": recomendacion
    }

"""
Endpionts
"""

@app.get("/")
def inicio ():
    return {"mensaje" : "Servidor Inteligente de calificaciones"}

@app.post("/estudiantes/")
def agregar_estudiante(estudiante: Estudiante):
    db.append(estudiante)
    return {"mensaje": "Estudiante agregado":}
 
@app.get("//")

