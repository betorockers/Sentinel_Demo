# ping_logic.py - Demo Version
import random
import time
import platform

def get_mac_address(ip):
    """Simula una MAC address para el modo demo."""
    # Generar una MAC aleatoria consistente para la misma IP
    random.seed(ip)
    mac = [random.randint(0x00, 0xff) for _ in range(6)]
    return ':'.join(map(lambda x: "%02X" % x, mac))

def ping_ip(ip, monitor, interval_sec): 
    """Simulación de ping para el modo demo (90% online, 10% offline)."""
    
    while True:
        # Simulación: 75% de probabilidad de estar conectado (más fallos para el video)
        success = random.random() < 0.75
        
        new_status = "Conectado" if success else "Desconectado"
        mac_address = "No disponible"
        latencia = None
        
        if success:
            mac_address = get_mac_address(ip)
            # Latencia aleatoria entre 10ms y 120ms
            latencia = round(random.uniform(10, 120), 2)
        
        # Verificar si el widget aún existe
        try:
            if not monitor.winfo_exists():
                break
        except:
            break
            
        monitor.update_status(new_status, mac_address, latencia) 
        
        # Esperar el intervalo
        time.sleep(interval_sec)
