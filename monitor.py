# monitor.py - Demo Version
import customtkinter
import tkinter as tk
import threading
from ping_logic import ping_ip 
import time
import subprocess
import platform
import json 
import pygame 
from plyer import notification
import datetime
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from metrics_manager import MetricasHistoricas
import numpy as np
from PIL import Image
import os

class ToastNotification(customtkinter.CTkToplevel):
    def __init__(self, master, title, message, color="green", duration=5000):
        super().__init__(master)
        
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        
        bg_color = "#1A1A1A"
        border_color = color if color != "green" else "#51cf66"
        if color == "red": border_color = "#ff6b6b"
        
        self.configure(fg_color=bg_color)
        
        width = 350
        height = 100
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        x = screen_width - width - 20
        y = screen_height - height - 60
        
        self.geometry(f"{width}x{height}+{x}+{y}")
        
        self.main_frame = customtkinter.CTkFrame(self, corner_radius=10, border_width=2, border_color=border_color, fg_color=bg_color)
        self.main_frame.pack(fill="both", expand=True)
        
        icon = "🛡️" if color == "green" else "⚠️"
        self.title_label = customtkinter.CTkLabel(self.main_frame, text=f"{icon} {title}", font=("Arial", 14, "bold"), text_color="#FFFFFF")
        self.title_label.pack(pady=(10, 0), padx=15, anchor="w")
        
        self.message_label = customtkinter.CTkLabel(self.main_frame, text=message, font=("Arial", 12), text_color="#CCCCCC", wraplength=300, justify="left")
        self.message_label.pack(pady=(5, 10), padx=15, anchor="w")
        
        self.progress = customtkinter.CTkProgressBar(self.main_frame, height=4, progress_color=border_color)
        self.progress.pack(fill="x", padx=15, pady=(0, 10))
        self.progress.set(1)
        
        self.after(duration, self.destroy)

class IPMonitor(customtkinter.CTkFrame):
    def __init__(self, master, ip, label, desconexiones_count=0, mac="Buscando MAC...", disconnection_timestamp=None): 
        super().__init__(master, corner_radius=10, fg_color="#2B2B2B",
                         border_width=2, border_color="#555555")

        self.ip = ip
        self.label = label
        self.status = "Verificando..."
        self.previous_status = None 
        self.desconexiones_count = desconexiones_count 
        self.mac = mac
        self.disconnection_timestamp = disconnection_timestamp 

        self.grid_columnconfigure(0, weight=1)

        self.label_name = customtkinter.CTkLabel(self, text=self.label, font=("Arial", 14, "bold"), text_color="#FFFFFF")
        self.label_name.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.ip_label = customtkinter.CTkLabel(self, text=self.ip, font=("Arial", 11), text_color="#AAAAAA")
        self.ip_label.grid(row=1, column=0, padx=10, pady=(0, 2), sticky="ew")

        self.mac_label = customtkinter.CTkLabel(self, text=self.mac, font=("Arial", 10, "italic"), text_color="#888888") 
        self.mac_label.grid(row=2, column=0, padx=10, pady=(0, 5), sticky="ew")

        self.status_icon_label = customtkinter.CTkLabel(self, text="⏳", font=("Arial", 24), text_color="#555555")
        self.status_icon_label.grid(row=3, column=0, padx=10, pady=(5, 0), sticky="ew")

        self.status_text_label = customtkinter.CTkLabel(self, text="Iniciando...", font=("Arial", 12, "bold"), text_color="#555555")
        self.status_text_label.grid(row=4, column=0, padx=10, pady=(0, 10), sticky="ew")

    def update_status(self, new_status, mac_address, latencia=None): 
        try:
            if self.winfo_exists():
                self.after(0, self._update_status_ui, new_status, mac_address, latencia)
        except:
            pass

    def _update_status_ui(self, new_status, mac_address, latencia=None):
        self.previous_status = self.status 
        self.status = new_status
        self.mac = mac_address
        
        try:
            app = self.winfo_toplevel()
            
            if hasattr(app, 'metricas'):
                app.metricas.agregar_medicion(self.ip, latencia, new_status)
        except Exception as e:
            print(f"Error al guardar métrica: {e}")
            
        self.mac_label.configure(text=self.mac)
        self.update_visuals()
        self.check_for_alert() 

    def update_visuals(self):
        if self.status == "Conectado":
            self.configure(border_color="green")
            self.status_icon_label.configure(text="👍", text_color="green")
            self.status_text_label.configure(text="Conectado", text_color="green")
            self.mac_label.configure(text_color="#AAAAAA") 
        elif self.status == "Desconectado":
            self.configure(border_color="red")
            self.status_icon_label.configure(text="👎", text_color="red")
            self.status_text_label.configure(text="Desconectado", text_color="red")
            self.mac_label.configure(text="MAC Desconocida", text_color="#777777")
        else:
            self.configure(border_color="#555555")
            self.status_icon_label.configure(text="⏳", text_color="gray")
            self.status_text_label.configure(text=self.status, text_color="gray")
            self.mac_label.configure(text_color="#777777") 
            
    def check_for_alert(self):
        if self.previous_status is not None and self.previous_status != self.status:
            if self.status == "Desconectado":
                self.disconnection_timestamp = datetime.datetime.now()
                self.send_alert(f"¡Alerta! {self.label} está desconectado.", "red", "alerta.mp3")
                self.desconexiones_count += 1
            elif self.status == "Conectado":
                self.disconnection_timestamp = None 
                self.send_alert(f"¡Recuperado! {self.label} está en línea de nuevo.", "green", "recuperado.mp3")

    def send_alert(self, message, color, sound_file): 
        try:
            app = self.winfo_toplevel()
            
            title = "Sentinel: Cambio de Estado"
            ToastNotification(app, title, message, color=color)
        except Exception as e:
            print(f"Error al mostrar Toast: {e}")

        try:
            sound_path = f"assets/sounds/{sound_file}"
            if os.path.exists(sound_path):
                sound = pygame.mixer.Sound(sound_path) 
                sound.play()
        except Exception as e:
            print(f"Error al reproducir el sonido: {e}")

class App(customtkinter.CTk):
    def __init__(self, equipos_a_monitorear):
        super().__init__()
        
        self.geometry("1366x768") 
        
        try:
            pygame.mixer.init()
        except pygame.error as e:
            print(f"Error al inicializar el mezclador de Pygame: {e}")
        
        self.title("Monitor de IP's DemoVersion v2.0 | Powered by @Betograf_inc & Omar Toledo")

        self.grid_rowconfigure(0, weight=1) 
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        
        self.equipos_a_monitorear = equipos_a_monitorear
        self.ping_interval = 2 # Intervalo ultra rápido para el video
        
        self.tabview = customtkinter.CTkTabview(self)
        self.tabview.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")

        self.tab_monitoreo = self.tabview.add("Monitoreo Activo")
        self.tab_historial = self.tabview.add("Historial de Eventos")

        self.monitor_frame = customtkinter.CTkScrollableFrame(self.tab_monitoreo)
        self.monitor_frame.pack(fill='both', expand=True, padx=5, pady=5)

        self.historial_frame = customtkinter.CTkScrollableFrame(self.tab_historial)
        self.historial_frame.pack(fill='both', expand=True, padx=5, pady=5)

        self.button_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=0)
        self.button_frame.grid_columnconfigure(2, weight=1)

        self.refresh_button = customtkinter.CTkButton(self.button_frame, text="Recargar", font=("Arial", 14, "bold"),
                                                       command=self.create_monitors)
        self.refresh_button.grid(row=0, column=1, padx=10, pady=5)

        self.footer_frame = customtkinter.CTkFrame(self, height=40, corner_radius=0)
        self.footer_frame.grid(row=2, column=0, sticky="ew")

        self.footer_frame.grid_columnconfigure(0, weight=1)
        self.footer_frame.grid_columnconfigure(1, weight=1)
        self.footer_frame.grid_columnconfigure(2, weight=1)
        
        self.clock_label = customtkinter.CTkLabel(self.footer_frame, text="", font=("Arial", 12, "bold"), text_color="#00d9ff")
        self.clock_label.grid(row=0, column=0, padx=20, pady=2, sticky="w")
        
        leyenda_label = customtkinter.CTkLabel(self.footer_frame, text="DEMOSTRACIÓN PORTFOLIO - Monitor de Red", font=("Arial", 12, "bold"), text_color="#FFFFFF")
        leyenda_label.grid(row=0, column=1, padx=10, pady=2, sticky="ew")

        nombre_label = customtkinter.CTkLabel(self.footer_frame, text="Desarrollado por Omar Toledo | betograf.cl", font=("Arial", 12, "italic"), text_color="#999999")
        nombre_label.grid(row=0, column=2, padx=10, pady=2, sticky="e")
        
        self.update_clock()

        self.sidebar_frame = customtkinter.CTkFrame(self, width=200, corner_radius=0, border_width=0)
        self.sidebar_frame.grid(row=0, column=1, rowspan=3, sticky="nsew")
        
        try:
            logo_path = 'assets/img/logoBlancoGraf.png'
            if os.path.exists(logo_path):
                pil_image = Image.open(logo_path)
                orig_w, orig_h = pil_image.size
                ratio = min(75/orig_w, 75/orig_h)
                new_w = int(orig_w * ratio)
                new_h = int(orig_h * ratio)
                self.logo_image = customtkinter.CTkImage(light_image=pil_image, dark_image=pil_image, size=(new_w, new_h))
                self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, image=self.logo_image, text="")
                self.logo_label.grid(row=0, column=0, padx=10, pady=10)
        except Exception as e:
            print(f"Error al cargar el logo: {e}")

        self.sidebar_title = customtkinter.CTkLabel(self.sidebar_frame, text="Panel de Control", font=("Arial", 16, "bold"))
        self.sidebar_title.grid(row=1, column=0, padx=10, pady=(0, 5))
        
        self.demo_badge = customtkinter.CTkLabel(self.sidebar_frame, text="MODO SIMULACIÓN", font=("Arial", 10, "bold"), text_color="#ff9f43", fg_color="#3d2b1f", corner_radius=5)
        self.demo_badge.grid(row=2, column=0, padx=10, pady=(0, 5))

        self.sidebar_frame.grid_rowconfigure(14, weight=1) 
        
        self.interval_label = customtkinter.CTkLabel(self.sidebar_frame, text="Intervalo Ping (Seg):", font=("Arial", 12))
        self.interval_label.grid(row=3, column=0, padx=10, pady=(5, 0), sticky="w")
        
        self.ping_interval_entry = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="ej. 5", justify='center')
        self.ping_interval_entry.grid(row=4, column=0, padx=10, pady=2, sticky="ew")
        self.ping_interval_entry.insert(0, str(self.ping_interval))
        
        self.ip_label = customtkinter.CTkLabel(self.sidebar_frame, text="Dirección IP:", font=("Arial", 12))
        self.ip_label.grid(row=5, column=0, padx=10, pady=(5, 0), sticky="w")
        self.ip_entry = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="ej. 192.168.1.1")
        self.ip_entry.grid(row=6, column=0, padx=10, pady=2, sticky="ew")

        self.etiqueta_label = customtkinter.CTkLabel(self.sidebar_frame, text="Etiqueta:", font=("Arial", 12))
        self.etiqueta_label.grid(row=7, column=0, padx=10, pady=(5, 0), sticky="w")
        self.etiqueta_entry = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="ej. Servidor")
        self.etiqueta_entry.grid(row=8, column=0, padx=10, pady=2, sticky="ew")

        self.add_button = customtkinter.CTkButton(self.sidebar_frame, text="Agregar Equipo", command=self.agregar_equipo)
        self.add_button.grid(row=9, column=0, padx=10, pady=5)
        
        self.remove_button = customtkinter.CTkButton(self.sidebar_frame, text="Eliminar Equipo", command=self.remover_equipo, fg_color="#c0392b", hover_color="#e74c3c")
        self.remove_button.grid(row=10, column=0, padx=10, pady=5)

        self.save_button = customtkinter.CTkButton(self.sidebar_frame, text="Guardar Config", command=self.guardar_equipos)
        self.save_button.grid(row=11, column=0, padx=10, pady=5)
        
        self.report_button = customtkinter.CTkButton(self.sidebar_frame, text="Generar Reporte", command=self.generar_reporte)
        self.report_button.grid(row=12, column=0, padx=10, pady=5)
        
        self.monitors = {}
        self.create_monitors()
        self.after(500, self.inicializar_historial)

    def update_clock(self):
        ahora = datetime.datetime.now().strftime("%H:%M:%S")
        fecha = datetime.datetime.now().strftime("%d/%m/%Y")
        self.clock_label.configure(text=f"{fecha} | {ahora}")
        self.after(1000, self.update_clock)

    def create_monitors(self):
        try:
            val = self.ping_interval_entry.get()
            if val:
                self.ping_interval = max(1, int(val))
        except: pass

        for widget in self.monitor_frame.winfo_children(): widget.destroy()
        self.monitors = {}
        row, col = 0, 0
        max_cols = 4 

        for i in range(max_cols): self.monitor_frame.grid_columnconfigure(i, weight=1, pad=10)

        for equipo in self.equipos_a_monitorear:
            monitor = IPMonitor(self.monitor_frame, equipo["ip"], equipo["label"])
            monitor.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            self.monitors[equipo["ip"]] = monitor
            threading.Thread(target=ping_ip, args=(equipo["ip"], monitor, self.ping_interval), daemon=True).start()
            col += 1
            if col >= max_cols: col = 0; row += 1

    def agregar_equipo(self):
        ip, etiqueta = self.ip_entry.get(), self.etiqueta_entry.get()
        if ip and etiqueta:
            # Verificar si ya existe
            if any(e["ip"] == ip for e in self.equipos_a_monitorear):
                ToastNotification(self, "Error", f"La IP {ip} ya está en la lista", color="red")
                return

            self.equipos_a_monitorear.append({"ip": ip, "label": etiqueta})
            self.create_monitors()
            self.ip_entry.delete(0, 'end'); self.etiqueta_entry.delete(0, 'end')
            ToastNotification(self, "Éxito", f"Equipo {etiqueta} agregado correctamente", color="green")
        else:
            ToastNotification(self, "Campos Incompletos", "Por favor, completa IP y Etiqueta", color="red")

    def remover_equipo(self):
        ip = self.ip_entry.get()
        if ip:
            original_count = len(self.equipos_a_monitorear)
            self.equipos_a_monitorear = [e for e in self.equipos_a_monitorear if e["ip"] != ip]
            
            if len(self.equipos_a_monitorear) < original_count:
                self.create_monitors()
                ToastNotification(self, "Éxito", f"Equipo con IP {ip} eliminado", color="green")
                self.ip_entry.delete(0, 'end')
            else:
                ToastNotification(self, "No encontrado", f"No se encontró la IP {ip}", color="red")
        else:
            ToastNotification(self, "Campo Vacío", "Ingresa la IP para eliminar", color="red")

    def guardar_equipos(self):
        try:
            data = {"intervalo_ping": self.ping_interval, "equipos": self.equipos_a_monitorear}
            with open("equipos_demo.json", "w") as f: json.dump(data, f, indent=4)
            if hasattr(self, 'metricas'): self.metricas.guardar_en_disco()
        except Exception as e: print(f"Error: {e}")

    def generar_reporte(self):
        filename = f"reporte_demo_{datetime.datetime.now().strftime('%H%M%S')}.txt"
        with open(filename, "w") as f:
            f.write("--- REPORTE SENTINEL DEMO ---\n")
            for ip, m in self.monitors.items():
                f.write(f"{m.label} ({ip}): {m.status}\n")

    def inicializar_historial(self):
        self.metricas = MetricasHistoricas(archivo_datos="metricas_historial.json")
        titulo = customtkinter.CTkLabel(self.historial_frame, text="📊 Análisis de Red (Simulado)", font=("Arial", 20, "bold"))
        titulo.pack(pady=(10, 20))
        
        self.graficos_frame = customtkinter.CTkFrame(self.historial_frame, fg_color="transparent")
        self.graficos_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Latencia
        f_lat = customtkinter.CTkFrame(self.graficos_frame, fg_color="#2B2B2B")
        f_lat.pack(fill='both', expand=True, pady=5)
        customtkinter.CTkLabel(f_lat, text="📈 Latencia en Tiempo Real", font=("Arial", 16, "bold")).pack(pady=2)
        self.fig_latencia = Figure(figsize=(8, 3), facecolor='#2B2B2B', dpi=100)
        self.ax_latencia = self.fig_latencia.add_subplot(111)
        self.ax_latencia.set_facecolor('#2B2B2B')
        self.ax_latencia.tick_params(colors='white', labelsize=8)
        self.canvas_latencia = FigureCanvasTkAgg(self.fig_latencia, f_lat)
        self.canvas_latencia.get_tk_widget().pack(fill='both', expand=True, padx=5, pady=5)
        
        # Gauges
        self.frame_gauges = customtkinter.CTkFrame(self.graficos_frame, fg_color="transparent")
        self.frame_gauges.pack(fill='x', pady=5)
        customtkinter.CTkLabel(self.frame_gauges, text="🎯 Disponibilidad (Uptime)", font=("Arial", 16, "bold")).pack(pady=2)
        self.gauges_container = customtkinter.CTkFrame(self.frame_gauges, fg_color="transparent")
        self.gauges_container.pack(fill='x', expand=True)

        # Heatmap
        f_hm = customtkinter.CTkFrame(self.graficos_frame, fg_color="#2B2B2B")
        f_hm.pack(fill='both', expand=True, pady=5)
        customtkinter.CTkLabel(f_hm, text="🗓️ Mapa de Calor de Disponibilidad", font=("Arial", 16, "bold")).pack(pady=2)
        self.fig_heatmap = Figure(figsize=(8, 2.5), facecolor='#2B2B2B', dpi=100)
        self.ax_heatmap = self.fig_heatmap.add_subplot(111)
        self.ax_heatmap.set_facecolor('#2B2B2B')
        self.canvas_heatmap = FigureCanvasTkAgg(self.fig_heatmap, f_hm)
        self.canvas_heatmap.get_tk_widget().pack(fill='both', expand=True, padx=5, pady=5)
        
        self.btn_actualizar = customtkinter.CTkButton(self.historial_frame, text="🔄 Actualizar Análisis", command=self.actualizar_graficos)
        self.btn_actualizar.pack(pady=10)
        self.after(500, self.actualizar_graficos)

    def actualizar_graficos(self):
        self.ax_latencia.clear()
        self.ax_latencia.set_facecolor('#2B2B2B')
        self.ax_latencia.grid(True, alpha=0.1)
        colores = ['#00d9ff', '#ff6b6b', '#51cf66', '#ffd43b', '#ff6b9d']
        for i, equipo in enumerate(self.equipos_a_monitorear):
            datos = self.metricas.obtener_datos(equipo['ip'], periodo_horas=24)
            if datos and datos['latencias']:
                y = list(datos['latencias'])[-50:]
                self.ax_latencia.plot(range(len(y)), y, label=equipo['label'], color=colores[i % len(colores)], linewidth=2)
        if self.ax_latencia.get_legend_handles_labels()[1]:
            self.ax_latencia.legend(facecolor='#3B3B3B', labelcolor='white', fontsize=8)
        self.canvas_latencia.draw()
        
        # Heatmap
        self.ax_heatmap.clear()
        hm_data, hm_labels = [], []
        for equipo in self.equipos_a_monitorear:
            hm_labels.append(equipo['label'][:15])
            datos = self.metricas.obtener_datos(equipo['ip'], periodo_horas=24)
            if datos and datos['estados']:
                bloques = np.array_split(datos['estados'], 24)
                hm_data.append([sum(b)/len(b) if len(b)>0 else 0 for b in bloques])
            else: hm_data.append([0]*24)
        if hm_data:
            self.ax_heatmap.imshow(hm_data, cmap='RdYlGn', aspect='auto', vmin=0, vmax=1)
            self.ax_heatmap.set_yticks(range(len(hm_labels)))
            self.ax_heatmap.set_yticklabels(hm_labels, color='white', fontsize=8)
        self.canvas_heatmap.draw()

        # Gauges
        for w in self.gauges_container.winfo_children(): w.destroy()
        for i in range(5): self.gauges_container.grid_columnconfigure(i, weight=1)
        for i, equipo in enumerate(self.equipos_a_monitorear):
            uptime = self.metricas.calcular_uptime(equipo['ip'])
            f = customtkinter.CTkFrame(self.gauges_container, fg_color="#2B2B2B")
            f.grid(row=i//5, column=i%5, padx=5, pady=5, sticky="nsew")
            c = tk.Canvas(f, width=100, height=60, bg="#2B2B2B", highlightthickness=0)
            c.pack()
            color = '#51cf66' if uptime >= 98 else '#ffd43b' if uptime >= 90 else '#ff6b6b'
            c.create_arc(5, 5, 95, 95, start=0, extent=180, outline="#444", width=6, style="arc")
            c.create_arc(5, 5, 95, 95, start=180, extent=-(uptime/100)*180, outline=color, width=6, style="arc")
            c.create_text(50, 45, text=f"{uptime:.1f}%", fill="white", font=("Arial", 10, "bold"))
            customtkinter.CTkLabel(f, text=equipo['label'][:12], font=("Arial", 9), text_color="#AAA").pack()
        
        self.after(5000, self.actualizar_graficos)

if __name__ == "__main__":
    app = App([{"ip": "1.1.1.1", "label": "Cloudflare"}])
    app.mainloop()
