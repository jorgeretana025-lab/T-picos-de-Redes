import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import time

"""
Configuracion

"""
Num_paquetes = 100
Tamano_paquete = 1024 #bytes
velocidad_red = 100000 #bytes por segundo

"""
Listas para almacenar datos

"""
latencias = []
paquetes_envidas = []
paquetes_recibidos = []
perdidos = 0

print("Simulando tráfico de datos . . .\n")

for i in range(Num_paquetes):
    tiempo_envio = time.time()

    """
    Simular latencia (entre 10ns y 100ns)

    """
    latencia = random.uniform(0.01,0.1)
    time.sleep(latencia)

    """
    Simular perdidas de paquetes (10%)
    """
    if random.random () < 0.1:
        perdidos += 1
        continue

    tiempo_recepcion = time.time()
    latencias.append(tiempo_recepcion - tiempo_envio)
    paquetes_envidas.append(Tamano_paquete)
    paquetes_recibidos.append(Tamano_paquete)

    """
    Metricas
    """
total_enviados = len(paquetes_envidas)
total_recibidos = len(paquetes_recibidos)
tasa_perdida = perdidos / Num_paquetes

latencia_promedio = np.mean(latencias)
# Througtput (bytes/segundo)
throughput = (sum(paquetes_recibidos)/sum (latencias)) if latencias else 0

"""
Configutación de Resultados
"""

print("Paquetes envidas: {total_enviados}")
print("Paquetes recibidos: {total_recibidos}")
print("Paquetes perdidos: {perdidos}")
print("Tasa de perdidad: {tasa_perdida:.2f}")
print("Tasa de perdidad: {latencia_promedio:.2f}")
print("Througtput: {Througtput:.2f} bytes/s ")

"""
Grafica de latencias
"""

plt.plot(latencias)
plt.title("Latencia por paquete")
plt.xlabel("paquetes")
plt.ylabel("Latencia(s)")
plt.grid()
plt.show()
