#!/usr/bin/env python3
"""
Script para ejecutar la aplicación ANXRISK localmente
"""
import os
import sys
import subprocess
import shutil

def verificar_dependencias():
    """Verifica e instala las dependencias necesarias"""
    dependencias_faltantes = []
    
    try:
        import streamlit
    except ImportError:
        dependencias_faltantes.append('streamlit')
    
    try:
        import pandas
    except ImportError:
        dependencias_faltantes.append('pandas')
    
    try:
        import numpy
    except ImportError:
        dependencias_faltantes.append('numpy')
    
    if dependencias_faltantes:
        print(f"\n[INFO] Instalando dependencias faltantes: {', '.join(dependencias_faltantes)}...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
            print("[OK] Dependencias instaladas correctamente\n")
        except subprocess.CalledProcessError:
            print("[ERROR] No se pudieron instalar las dependencias")
            sys.exit(1)

def main():
    print("\n" + "="*50)
    print("   Iniciando ANXRISK")
    print("="*50 + "\n")
    
    # Verificar e instalar dependencias
    verificar_dependencias()
    
    # Ejecutar la aplicación
    print("[OK] Iniciando la aplicación ANXRISK...")
    print("\nPresiona Ctrl+C para detener el servidor\n")
    
    try:
        # Buscar streamlit en diferentes ubicaciones
        streamlit_cmd = shutil.which("streamlit")
        if streamlit_cmd:
            subprocess.run([streamlit_cmd, "run", "app.py"])
        else:
            # Intentar ejecutar como módulo de Python
            subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except FileNotFoundError:
        print("\n[ERROR] No se pudo encontrar streamlit.")
        print("Intente ejecutar: python -m pip install streamlit")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n ¡Hasta luego!")
        sys.exit(0)
    except Exception as e:
        print(f"\n Error: {e}")
        sys.exit(1)
