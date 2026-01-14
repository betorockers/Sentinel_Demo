# 🛡️ Sentinel v2.0: Instructivo Maestro de Recreación (Portfolio Demo)

Este documento contiene todas las especificaciones técnicas y lógicas necesarias para recrear el proyecto **Anvic Network Sentinel v2.0** desde cero en un nuevo entorno de trabajo.

---

## 1. Estructura del Proyecto
El proyecto debe seguir esta jerarquía de archivos:
- `main.py`: Punto de entrada y configuración de equipos.
- `monitor.py`: Interfaz gráfica principal (CustomTkinter + Matplotlib).
- `ping_logic.py`: Lógica de red y simulación (Threading).
- `metrics_manager.py`: Gestión de base de datos JSON y cálculos de uptime.
- `assets/`:
    - `img/logoAnvic.png` (Logo corporativo).
    - `sounds/alerta.mp3`, `recuperado.mp3` (Alertas sonoras).

## 2. Especificaciones Técnicas de la UI (monitor.py)
- **Tema**: Dark Mode (`customtkinter.set_appearance_mode("dark")`).
- **Pestañas**: Usar `CTkTabview` con dos pestañas: "Monitoreo Activo" e "Historial de Eventos".
- **Sidebar (Panel de Control)**:
    - Sin líneas de separación.
    - Márgenes compactos (`pady=2` o `pady=5`).
    - Botones: Agregar, Eliminar, Guardar, Cargar, Generar Reporte.
- **Footer**:
    - Reloj digital en tiempo real (`HH:MM:SS`).
    - Créditos: "Desarrollado por Omar Toledo".
- **Gauges (Semicírculos)**: Dibujados con `tk.Canvas`, mostrando % de uptime con colores dinámicos (Verde/Amarillo/Rojo).
- **Heatmap**: Matriz de 24 bloques (horas) usando `matplotlib.pyplot.imshow` con el mapa de color `RdYlGn`.

## 3. Lógica de Negocio y Datos
- **Métricas**: Guardar timestamps, latencia y estado (1=Online, 0=Offline) en un archivo `metricas_historial.json`.
- **Threading**: Cada IP debe tener su propio hilo de ejecución para el ping, evitando que la UI se congele.
- **Cálculo de Uptime**: Promediar los estados (1s y 0s) de los últimos 30 días.

## 4. Modo Demo (Portfolio Edition)
Para la versión de portfolio, el archivo `ping_logic.py` debe incluir un flag `demo_mode=True`:
- **Simulación**: Usar `random.random()` para generar un 90% de estados "Conectado" y un 10% de "Desconectado".
- **Latencia**: Generar valores aleatorios entre 10ms y 120ms para que los gráficos tengan movimiento dinámico en el video.

## 5. Dependencias (requirements.txt)
```text
customtkinter
matplotlib
numpy
pygame
plyer
pillow
```

---
**Instrucción Final para la IA**: "Recrea este proyecto siguiendo estrictamente el diseño visual y la lógica de hilos. Prioriza la estética premium y la fluidez de la interfaz."
