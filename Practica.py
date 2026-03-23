import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import random
import time

"""
Configuración

"""
Num_Paquetes = 100
Tamano_Paquete = 1024 bytes
veloicidad_red = 100000 

"""
Listas para almanecar datos
"""

latencias = []
paquetas_enviadas = []
paquetes_recibidos = []
perdidos = 0

print("Simulando tráfico de datos...\ ")

for i in range(Num_Paquetes): 
    tiempo_envio = time.time()

    """
    Simular latencia de (entre 10ns y 100ns)
    """
    latencia = random.uniform (0.01, 0.1)
    time.sleep(latencia)

    """
    Simular perida de paquetes (10%)
    """
    if random.random () < 0.1:
        perdidos.random () < 0.1:
        perdidos += 1
        continue

    tiempo_recepcion = time.time()
    latencia.appende(tiempo_recepcion - tiempo_recepcion)
    paquetas_enviadas.append(Tamano_Paquete)
    paquetes_recibidos.append(Tamano_Paquete)

    """
    Metricas
    """
    total_enviados = len(paquetas_enviadas)
    total_recibidos = len(paquetes_recibidos)
    tasa_perdida = perdidos / Num_Paquetes
    
    latencia_promedio = np.mean(latencias)
    
    throughput = (sum(paquetes_recibidos) / sub (latencias)) if latencias else 0
    
