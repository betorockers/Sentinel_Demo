# metrics_manager.py - Demo Version
from collections import deque
from datetime import datetime, timedelta
import json
import os
import random

class MetricasHistoricas:
    """Almacena métricas de cada equipo para gráficos"""
    
    def __init__(self, max_puntos=1440, archivo_datos="metricas_historial.json"):
        self.max_puntos = max_puntos
        self.archivo_datos = archivo_datos
        self.datos = {}  # {ip: {'timestamps': [], 'latencias': [], 'estados': []}}
        
        if not os.path.exists(self.archivo_datos):
            self.pre_poblar_datos_demo()
        else:
            self.cargar_desde_disco()
    
    def pre_poblar_datos_demo(self):
        """Genera datos ficticios para que los gráficos no empiecen vacíos en la demo."""
        ips_demo = ["192.168.1.10", "192.168.1.25", "192.168.1.50", "192.168.1.100", "172.16.0.10"]
        ahora = datetime.now()
        
        for ip in ips_demo:
            self.datos[ip] = {
                'timestamps': deque(maxlen=self.max_puntos),
                'latencias': deque(maxlen=self.max_puntos),
                'estados': deque(maxlen=self.max_puntos)
            }
            # Generar 100 puntos de datos hacia atrás
            for i in range(100, 0, -1):
                ts = ahora - timedelta(minutes=i*5)
                success = random.random() < 0.95
                self.datos[ip]['timestamps'].append(ts)
                self.datos[ip]['latencias'].append(random.uniform(5, 40) if success else 0)
                self.datos[ip]['estados'].append(1 if success else 0)
        
        self.guardar_en_disco()

    def guardar_en_disco(self):
        try:
            datos_serializables = {}
            for ip, metricas in self.datos.items():
                datos_serializables[ip] = {
                    'timestamps': [ts.isoformat() for ts in list(metricas['timestamps'])],
                    'latencias': list(metricas['latencias']),
                    'estados': list(metricas['estados'])
                }
            with open(self.archivo_datos, "w") as f:
                json.dump(datos_serializables, f)
        except Exception as e:
            print(f"Error al guardar métricas: {e}")

    def cargar_desde_disco(self):
        if not os.path.exists(self.archivo_datos):
            return
        try:
            with open(self.archivo_datos, "r") as f:
                datos_cargados = json.load(f)
            for ip, metricas in datos_cargados.items():
                self.datos[ip] = {
                    'timestamps': deque([datetime.fromisoformat(ts) for ts in metricas['timestamps']], maxlen=self.max_puntos),
                    'latencias': deque(metricas['latencias'], maxlen=self.max_puntos),
                    'estados': deque(metricas['estados'], maxlen=self.max_puntos)
                }
        except Exception as e:
            print(f"Error al cargar métricas: {e}")

    def agregar_medicion(self, ip, latencia, estado):
        if ip not in self.datos:
            self.datos[ip] = {
                'timestamps': deque(maxlen=self.max_puntos),
                'latencias': deque(maxlen=self.max_puntos),
                'estados': deque(maxlen=self.max_puntos)
            }
        timestamp = datetime.now()
        self.datos[ip]['timestamps'].append(timestamp)
        self.datos[ip]['latencias'].append(latencia if latencia is not None else 0)
        self.datos[ip]['estados'].append(1 if estado == "Conectado" else 0)
    
    def obtener_datos(self, ip, periodo_horas=24):
        if ip not in self.datos:
            return None
        limite_tiempo = datetime.now() - timedelta(hours=periodo_horas)
        datos = self.datos[ip]
        timestamps = list(datos['timestamps'])
        latencias = list(datos['latencias'])
        estados = list(datos['estados'])
        indices = [i for i, ts in enumerate(timestamps) if ts >= limite_tiempo]
        return {
            'timestamps': [timestamps[i] for i in indices],
            'latencias': [latencias[i] for i in indices],
            'estados': [estados[i] for i in indices]
        }
    
    def calcular_uptime(self, ip, dias=30):
        if ip not in self.datos or len(self.datos[ip]['estados']) == 0:
            return 100.0
        estados = list(self.datos[ip]['estados'])
        total = len(estados)
        conectados = sum(estados)
        return (conectados / total * 100) if total > 0 else 100.0
