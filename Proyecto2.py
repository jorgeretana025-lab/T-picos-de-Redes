""""""
Sistemas de trafico de datos con IA

""""""
import numpy as np
import pandas as pd
import random
import time
import matplotlib.pyplot as pit
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

"""
Generar Datset
"""

def generar_datos (n=1000):
    np.random.seed(42)

    data=pd.DataFrame({
        "paquetes": np.random
        "bytes": np.random.randint(1000, 6000, n),
        "duracion": np.random.uniforme(0.1,15, n),
        "protocolo": np.random.choice([0,1], 1),
    })

    condiciones = [
     (data["bytes"] > 45000),
     (data["paquetes"]  < 2000),
   ]

   opciones = ["ataque", "video"]

   data["tipo"] = np.select(condiciones, opciones, default="normal")

   return data 