# 🛡️ Sentinel Master Prompt: Portfolio Demo Edition

Este documento es el "ADN" del proyecto **Anvic Network Sentinel v2.0**. Úsalo para recrear el proyecto en una nueva carpeta o para dárselo a otro asistente de IA.

---

## 📝 Descripción del Proyecto
Un monitor de red profesional con estética tipo Grafana, diseñado para el portfolio de **Omar Toledo**. Permite monitorear IPs en tiempo real, visualizar latencia histórica y disponibilidad mediante mapas de calor y gauges visuales.

## 🛠️ Tech Stack
- **Lenguaje**: Python 3.11+
- **UI**: `customtkinter` (Tema Dark)
- **Gráficos**: `matplotlib` con backend `TkAgg`
- **Lógica**: `threading`, `subprocess` (ping), `pygame` (sonidos)
- **Datos**: `numpy` y persistencia en `JSON`

## 📂 Estructura de Archivos
1.  [main.py](file:///d:/respaldo_de_todo_anvic/entrenamiento/Proyectos/ProyectoMonitoreoMod_V2/main.py): Punto de entrada. Inicializa la lista de equipos y lanza la App.
2.  [monitor.py](file:///d:/respaldo_de_todo_anvic/entrenamiento/Proyectos/ProyectoMonitoreoMod_V2/monitor.py): El corazón de la UI. Contiene las pestañas de Monitoreo y Historial.
3.  [ping_logic.py](file:///d:/respaldo_de_todo_anvic/entrenamiento/Proyectos/ProyectoMonitoreoMod_V2/ping_logic.py): Lógica de red (con soporte para simulación aleatoria).
4.  [metrics_manager.py](file:///d:/respaldo_de_todo_anvic/entrenamiento/Proyectos/ProyectoMonitoreoMod_V2/metrics_manager.py): Clase para procesar y guardar datos históricos.
5.  `assets/`:
    - `img/logoAnvic.png` (Logo 75x75)
    - `sounds/alerta.mp3`, [recuperado.mp3](file:///d:/respaldo_de_todo_anvic/entrenamiento/Proyectos/ProyectoMonitoreoMod_V2/assets/recuperado.mp3)

## 🚀 Funcionalidades Clave (ADN Lógico)
- **Gauges de Disponibilidad**: Semicírculos dibujados con `tkinter.Canvas` que muestran el % de uptime.
- **Heatmap de 24h**: Matriz de 24 bloques por equipo usando `imshow` de Matplotlib.
- **Modo Demo**: Generación de estados aleatorios (90% online / 10% offline) para demostraciones dinámicas en video.
- **Footer Dinámico**: Reloj en tiempo real y créditos del desarrollador.
- **Sidebar Compacto**: Panel de control sin separadores para máxima visibilidad.

## 💡 Instrucciones para la Recreación
1.  **Entorno**: Crear un `venv` e instalar `customtkinter`, `matplotlib`, `numpy`, `pygame`, `plyer`, `pillow`.
2.  **Modo Simulación**: En [ping_logic.py](file:///d:/respaldo_de_todo_anvic/entrenamiento/Proyectos/ProyectoMonitoreoMod_V2/ping_logic.py), implementar un flag `demo_mode=True` que use `random.random()` para simular caídas.
3.  **Diseño**: Usar colores `#00d9ff` (Cian), `#51cf66` (Verde), `#ff6b6b` (Rojo) y `#2B2B2B` (Fondo).
4.  **Optimización**: Asegurar que los pings corran en hilos separados (`threading`) para no bloquear la interfaz.

---
**Desarrollado por Omar Toledo | Sentinel v2.0 Portfolio Edition**
