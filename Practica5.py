# Practica 2 Deteccion de Localhost

from scapy.all import ARP, Ether, srp, sniff
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

"""
Escaneo de Red
"""
def escanear_red(ip_range="192.168.1.1/24"):
    print("Escaneando dispositivos...")

    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    paquete = ether / arp 

    resultado = srp(paquete, timeout=2, verbose=0)[0]

    dispositivos = []
    for enviado, recibido in resultado:
        dispositivos.append({
            "ip": recibido.psrc,
            "mac": recibido.hwsrc
        })
    return dispositivos


"""
Capturar Trafico
"""
trafico = []

def capturar_paquetes(packet):
    if packet.haslayer("IP"):
        trafico.append({
            "ip": packet["IP"].src,
            "longitud": len(packet),
            "protocolo": packet["IP"].proto
        })

def analizar_trafico(tiempo=10):
    global trafico
    trafico = []

    print("Capturando Trafico...")
    sniff(prn=capturar_paquetes, timeout=tiempo)

    df = pd.DataFrame(trafico)

    if df.empty:
        print("No se capturó tráfico, usando datos de prueba...")
        df = pd.DataFrame([
            {"ip": "192.168.1.10", "longitud": 200, "protocolo": 6},
            {"ip": "192.168.1.15", "longitud": 1500, "protocolo": 6},
            {"ip": "192.168.1.20", "longitud": 300, "protocolo": 17},
        ])

    return df


"""
IA
"""
def entrenar_modelo(df):
    if df.empty:
        return None, None, None

    df["etiqueta"] = df["longitud"].apply(lambda x: 1 if x > 1000 else 0)

    X = df[["longitud", "protocolo"]]
    y = df["etiqueta"]

    modelo = RandomForestClassifier()
    modelo.fit(X, y)

    return modelo, X, y


def predecir_trafico(modelo, X):
    if modelo is None:
        return []
    return modelo.predict(X)


"""
Main
"""
if __name__ == "__main__":


    dispositivos = escanear_red()
    print("\nDispositivos encontrados:")
    for d in dispositivos:
        print(d)

    df = analizar_trafico(10)
    print("\nDatos capturados:")
    print(df)

    modelo, X, y = entrenar_modelo(df)

    if modelo is not None:
        predicciones = predecir_trafico(modelo, X)
        df["prediccion"] = predicciones

        df["estado"] = df["prediccion"].apply(lambda x: "Anómalo" if x == 1 else "Normal")

        print("\nClasificación por IP:")
        print(df[["ip", "estado"]].drop_duplicates())

    else:
        print("No hay datos para entrenar el modelo.")