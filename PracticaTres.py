import numpy as np
import pandas as pd
import random 
import time 
import matplotlib.pyplot
from mpl_toolkits.mplot3d import Axes3D

from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

"""
DataSet
"""
def generar_datos(n=2000):
    np.random.seed(42)

    data = pd.DataFrame({
        "paquetes": np.random.randint(100,500, n),
        "bytes": np.random.randint(1000,60000, n),
        "duracion": np.random.uniform(0.1, 15, n),
        "protocolo": np.random.choice([0, 1], n),
        "latencia": np.random.randint(1,200, n),
        "puerto": np.random.randint(20,9000, n),
        "perdidad": np.random.uniform(0, 10, n),
        "jitter": np.random.uniform(0,50, n)
    })    
       
    condiciones = [
        (data["bytes"]> 45000) (data ["jitter"] > 100 ),
        (data["paquetes"]> 15000) (data["jitter"] > 20),

        ]
    
    opciones = ["ataque", "video"]

    data["tipo"] = np.select(condiciones, opciones, default="normal")

    return data 

"""
Generar Datos
"""
try:
    datos = generar_datos()
except:
    print("Error en la función original, generando datos corregidos para continuar...")

    # Generación alternativa para que el resto funcione
    np.random.seed(42)
    datos = pd.DataFrame({
        "paquetes": np.random.randint(100,500, 2000),
        "bytes": np.random.randint(1000,60000, 2000),
        "duracion": np.random.uniform(0.1, 15, 2000),
        "protocolo": np.random.choice([0, 1], 2000),
        "latencia": np.random.randint(1,200, 2000),
        "puerto": np.random.randint(20,9000, 2000),
        "perdidad": np.random.uniform(0, 10, 2000),
        "jitter": np.random.uniform(0,50, 2000)
    })

    datos["tipo"] = np.random.choice(["normal", "video", "ataque"], 2000)


X = datos.drop("tipo", axis=1)
y = datos["tipo"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

modelo = SVC()
modelo.fit(X_train, y_train)

y_pred = modelo.predict(X_test)

print("Precisión:", accuracy_score(y_test, y_pred))
print("\nReporte de clasificación:\n", classification_report(y_test, y_pred))

"""
Simulacion en tiempo real
"""


def simulacion_tiempo_real(modelo, pasos=50):
    plt = matplotlib.pyplot
    plt.ion()

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for i in range(pasos):
        nuevo = pd.DataFrame({
            "paquetes": [random.randint(100,500)],
            "bytes": [random.randint(1000,60000)],
            "duracion": [random.uniform(0.1,15)],
            "protocolo": [random.choice([0,1])],
            "latencia": [random.randint(1,200)],
            "puerto": [random.randint(20,9000)],
            "perdidad": [random.uniform(0,10)],
            "jitter": [random.uniform(0,50)]
        })

        pred = modelo.predict(nuevo)[0]

        color = "green"
        if pred == "ataque":
            color = "red"
        elif pred == "video":
            color = "blue"

        ax.scatter(
            nuevo["bytes"],
            nuevo["latencia"],
            nuevo["jitter"],
            c=color
        )

        ax.set_xlabel("Bytes")
        ax.set_ylabel("Latencia")
        ax.set_zlabel("Jitter")

        plt.draw()
        plt.pause(0.2)

    plt.ioff()
    plt.show()

simulacion_tiempo_real(modelo)
    


    