@echo off
title Ejecutando Monitor de IP's Demo
cd /d "d:\respaldo_de_todo_anvic\entrenamiento\Proyectos\Sentinel_Demo"
echo Activando entorno virtual...
call "demoEnv\Scripts\activate.bat"
echo Iniciando aplicacion...
python main.py
pause
