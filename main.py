# main.py - Demo Version
from monitor import App

if __name__ == "__main__":
    # Lista de IPs para la demostración
    ips_to_monitor = [        
        {"ip": "192.168.1.10", "label": "Servidor Web Principal"},
        {"ip": "192.168.1.25", "label": "Base de Datos Producción"},
        {"ip": "192.168.1.50", "label": "Firewall Perimetral"},
        {"ip": "192.168.1.100", "label": "Switch Core Distribución"},        
        {"ip": "172.16.0.10", "label": "Servidor de Aplicaciones"},
        {"ip": "172.16.0.20", "label": "Almacenamiento NAS"},
        {"ip": "10.0.0.1", "label": "Router Gateway"},
        {"ip": "10.0.0.5", "label": "Controlador de Dominio"},
        {"ip": "10.0.0.15", "label": "Servidor de Correo"},
        {"ip": "10.0.0.50", "label": "Backup Server"}
    ]
    
    print("Iniciando Monitor de IP's DemoVersion v2.0 [MODO DEMO]...")
    app = App(ips_to_monitor)
    app.mainloop()
