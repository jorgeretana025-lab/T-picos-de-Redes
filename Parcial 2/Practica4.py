"""
Practica 4 (Simple con IA para detectar dispositivo en tu red)
"""
import os
import numpy as np
from sklearn.tree import DecisionTreeClassifier

#Simulacion de datos

"""
Caracteristicas: [Tiempo_respuesta_ms]
"""
X = np.array ([[10,], [20], [30], [200], [300], [400]])
y = np.array ([1, 1, 1, 0, 0, 0,])

"""
Modelo de IA
"""

modelo = DecisionTreeClassifier()
modelo.fit(x,y)

"""
Escaneo de Red
"""
red = "192.168.1."

for i in range (1, 20):
    ip = red + str(i)

    """
    Ping Window
    """
    respuesta = os.popen(f"ping -n -w 100 {ip}").read()

    if "tiempo" in respuesta:

        try:
            tiempo = int(respuesta.split("tiempo=") [1].split ("ns") [0])

        except:
            tiempo = 300

    else:
        tiempo = 400

    """
    Prediccion IA
    """

    prediccion = modelo.predict([[tiempo]]) [0]

    if prediccion == 1:
        print(f"Dispositivo Activa IA:  {ip} - {tiempo} ms")
    
    else:
        print(f"Dispositivo Inactivo (IA): {ip}")