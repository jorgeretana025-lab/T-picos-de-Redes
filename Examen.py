"""
Examen Primer Parcial (Simulacion y Detencion de Trafico de Datos con IA)
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import time
import threading

from mpl_toolkits.mplot3d import Axes3D
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

"""
Dataset Simulado
"""
def generar_datos(n=300):
    np.random.seed(42)

    data = pd.DataFrame({
        "paquetes": np.random.randint(100, 5000, n),
        "tamano": np.random.randint(500, 10000, n),
        "tiempo": np.random.uniform(0.01, 2, n),
        "latencia": np.random.uniform(0.01, 0.3, n),
        "ancho_banda": np.random.randint(1000, 100000, n)
    })
    # Si la latencia y tamaño son mayores a 0.2 segundos y 8000 mbps se clasificara como 'anomalo'
    condiciones = [
        (data["latencia"] > 0.2),
        (data["tamano"] > 8000)
    ]

    opciones = ["anomalo", "anomalo"]
    # Si la latencia y el tamaño son menores a 0.2 seg y 8000 mbps seran clasificadas como 'normales'
    data["tipo"] = np.select(condiciones, opciones, default="normal")

    return data
"""
Machine Learning (IA)
"""
def entrenar_modelo(data):
    X = data[["paquetes", "tamano", "tiempo", "latencia", "ancho_banda"]]
    y = data["tipo"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    
    #El modelo de machine learning que se utilizara sera RandomForest
    modelo = RandomForestClassifier(n_estimators=100)
    modelo.fit(X_train, y_train)
    #La IA crea los datos y estos seran clasificados de acuerdo a su tamaño y latencia
    pred = modelo.predict(X_test)
    #Metricas
    print("\n --Metricas del Modelo-- ")
    print("Accuracy:", accuracy_score(y_test, pred))
    print("Matriz de confusion:\n", confusion_matrix(y_test, pred))

    return modelo

tiempo_real = []
trafico = []
clasificaciones = []
"""
Simulacion en Tiempo Real
"""
def simulacion(modelo):
    i = 0
    # El tiempo de simulacion sera hasta los 50 segundos
    for i in range(50):
        paquetes = random.randint(100, 5000)
        #El numero de paquetes que se utilizaran sera de entre 100 a 5000
        tamano = random.randint(500, 10000)
        #El tamaño de los datos que se utilizaran sera de entre 500 a 10000
        tiempo_tx = random.uniform(0.01, 2)
        #El tiempo de transmision sera de los 0.01 segundos a 2 segundos
        latencia = random.uniform(0.01, 0.3)
        #El tiempo de latencia sera de los 0.01 segundos a 0.3 segundos
        ancho = random.randint(1000, 100000)
        #La capacidad del ancho de banda sera de entre 1000 a 100000 mbps

        muestra = np.array([[paquetes, tamano, tiempo_tx, latencia, ancho]])
        pred = modelo.predict(muestra)[0]

        print(f"\nIteracion {i+1}")
        print(f"Paquetes: {paquetes}, Tamaño: {tamano}, Latencia: {latencia:.3f}")
        print(f"Clasificacion: {pred}")

        tiempo_real.append(i)
        trafico.append(paquetes)
        clasificaciones.append(1 if pred == "anomalo" else 0)

        i += 1
        # La cantidad que se usara para simular el retraso seran de 0.5 segundos
        time.sleep(0.5)
"""
Actualizacion de las Graficas 
"""
def graficas():
    plt.ion()
    # Matplotlib para la actualizacion en tiempo real
    fig = plt.figure()

    while True:
        fig.clf()
        # Grafica de trafico vs tiempo
        ax1 = fig.add_subplot(2, 1, 1)
        ax1.plot(tiempo_real, trafico)
        ax1.set_title("Trafico vs Tiempo")
        ax1.set_xlabel("Tiempo")
        ax1.set_ylabel("Paquetes")
        
        # Grafica de clasificacion de datos
        ax2 = fig.add_subplot(2, 1, 2, projection='3d')
        colores = ['red' if c == 1 else 'green' for c in clasificaciones]
        ax2.scatter(
            tiempo_real,
            trafico,
            clasificaciones,
            c=colores
        )

        ax2.set_title("Clasificacion ")
        ax2.set_xlabel("Tiempo")
        ax2.set_ylabel("Trafico")
        ax2.set_zlabel("Clasificacion (0=Normal, 1=Anomalo)")

        plt.tight_layout()
        plt.pause(0.1)
"""
Main
"""
if __name__ == "__main__":
    data = generar_datos(300)
    print(data.head())

    modelo = entrenar_modelo(data)

    hilo_simulacion = threading.Thread(target=simulacion, args=(modelo,))
    hilo_graficas = threading.Thread(target=graficas)

    hilo_simulacion.start()
    hilo_graficas.start()
