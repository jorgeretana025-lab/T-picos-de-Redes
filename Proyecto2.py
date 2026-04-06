"""
Sistemas de Trafico de Datos con IA

"""

import numpy as np
import pandas as pd
import random
import time
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


"""
Generar DatSet
"""

def generar_datos(n=1000):
    np.random.seed(42)

    data = pd.DataFrame({
        "paquetes": np.random.randint(1000,5000,n),
        "bytes": np.random.randint(1000, 60000, n),
        "duracion":np.random.uniform(0.1,15, n),
        "protocolo": np.random.choice([0,1],n),
    })


    condiciones = [
        (data["bytes"]>45000),
        (data["paquetes"]<2000),


    ]  

    opciones =["ataque","video"]

    data["tipo"] = np.select(condiciones, opciones, default="normal")

    return data

"""
Entrenamiento del Modelo

"""


def entrenar_modelo(data):
    x = data[["paquetes","bytes","duracion","protocolo"]]
    y = data["tipo"]

    x_train, x_test, y_train, y_test = train_test_split(
        x,y,test_size=0.2, random_state=42
    )

    modelo = RandomForestClassifier(n_estimators=100)
    modelo.fit(x_train,y_train)


    prediciones = modelo.predict(x_test)

    print("\n evaluacion del modelo:")
    print("accuracy:", accuracy_score(y_test, prediciones))
    print("\nReporte:\n ", classification_report(y_test, prediciones))

    return modelo

"""
Simulacion en Tiempo Real
"""

def simulacion_tiempo_real(modelo,iteraciones=10):
    print("\n iniciando simulacion en tiempo real ...\n")

    for i in range (iteraciones):
        paquetes = random.randint(100, 5000)
        bytes_ = np.random.randint(1000, 60000)
        duracion = random.uniform(0.1,15)
        protocolo = np.random.choice([0,1])
         
        muestra = np.array([paquetes, bytes_, duracion, protocolo])
        pred = modelo.predict(muestra)[0]

        print(f"ilteracion {i+1}")
        print(f"paquetes: {paquetes}, bytes: {bytes_}, duracion: {duracion:.2f}, protocolo:")
        print("clasificacion: {pred}")
        print("." * 50)

        time.sleep

"""
Graficas
"""
def graficas(data):
    plt.figure()
    plt.hist(data["bytes"])
    plt.title("distribucion de bytes")
    plt.xlabel("bytes")
    plt.ylabel("frecuencia")
    plt.grid()
    plt.show()

    plt.figure()
    plt.hist(data["paquetes"])
    plt.title("distribucion de paquetes")
    plt.xlabel("paquetes")
    plt.ylabel("frecuencia")
    plt.grid()
    plt.show()

    plt.figure()
    data["tipo"].value_counts().plot(kind = 'bar')
    plt.title("tipos de trafico")
    plt.xlabel("tipo")
    plt.ylabel("cantidad")
    plt.grid()
    plt.show()


"""
Main
"""
if __name__ == "__main__":
   data = generar_datos(1000)
   print("dataset generado: ")
   print(data.head())

   modelo = entrenar_modelo(data)

   graficas(data)

   simulacion_tiempo_real(modelo, iteraciones=10)