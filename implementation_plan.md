# Plan: Creación de Sentinel Demo (Portfolio Edition)

Este plan detalla la creación de una versión independiente y optimizada del proyecto **Anvic Network Sentinel** para ser subida a GitHub y utilizada en un portfolio profesional.

## Objetivos
1.  **Independencia**: Crear una carpeta nueva con todo lo necesario para funcionar (código, assets, dependencias).
2.  **Modo Simulación**: Añadir una funcionalidad que permita simular caídas y recuperaciones aleatorias para que el video de demostración sea dinámico.
3.  **Documentación Pro**: Crear un `README.md` de alto impacto con instrucciones claras y descripción de tecnologías.
4.  **Código Limpio**: Eliminar rutas absolutas y referencias locales innecesarias.

## Estructura Propuesta
- `Sentinel_Demo/`
    - [main.py](file:///d:/respaldo_de_todo_anvic/entrenamiento/Proyectos/ProyectoMonitoreoMod_V2/main.py): Punto de entrada simplificado.
    - [monitor.py](file:///d:/respaldo_de_todo_anvic/entrenamiento/Proyectos/ProyectoMonitoreoMod_V2/monitor.py): Interfaz con los gauges y heatmap (versión final optimizada).
    - [ping_logic.py](file:///d:/respaldo_de_todo_anvic/entrenamiento/Proyectos/ProyectoMonitoreoMod_V2/ping_logic.py): Lógica con soporte para **Modo Demo** (simulación de latencia y estados).
    - [metrics_manager.py](file:///d:/respaldo_de_todo_anvic/entrenamiento/Proyectos/ProyectoMonitoreoMod_V2/metrics_manager.py): Gestión de datos históricos.
    - `assets/`: Carpeta con logo y sonidos.
    - [requirements.txt](file:///d:/respaldo_de_todo_anvic/entrenamiento/Proyectos/ProyectoMonitoreoMod_V2/requirements.txt): Lista limpia de dependencias.
    - `README.md`: Presentación del proyecto.

## User Review Required
> [!IMPORTANT]
> **Ubicación del Proyecto**: Necesito que me confirmes en qué carpeta quieres que cree este nuevo proyecto. ¿Te parece bien en `d:\respaldo_de_todo_anvic\entrenamiento\Proyectos\Sentinel_Demo`?
>
> **Modo Simulación**: ¿Quieres que el "Modo Demo" sea automático (caídas aleatorias cada X segundos) o prefieres que use IPs reales pero con latencia simulada?

## Pasos a Seguir
1.  **Crear Directorio**: Una vez confirmada la ruta.
2.  **Copiar y Adaptar Assets**: Asegurar que el logo y sonidos estén presentes.
3.  **Refactorizar Código**:
    - Adaptar [ping_logic.py](file:///d:/respaldo_de_todo_anvic/entrenamiento/Proyectos/ProyectoMonitoreoMod_V2/ping_logic.py) para incluir una función `ping_simulado`.
    - Adaptar [monitor.py](file:///d:/respaldo_de_todo_anvic/entrenamiento/Proyectos/ProyectoMonitoreoMod_V2/monitor.py) para que sea fácil de ejecutar sin configuraciones previas.
4.  **Crear Documentación**: Redactar un README profesional en español e inglés (opcional).
5.  **Verificación**: Ejecutar la demo para asegurar que sea "Plug & Play".
