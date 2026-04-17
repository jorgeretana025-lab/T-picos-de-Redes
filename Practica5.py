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