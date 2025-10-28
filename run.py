#!/usr/bin/env python3
"""
Script para ejecutar la aplicación ANXRISK localmente
"""
import os
import sys
import subprocess

def main():
    # Verificar si estamos en un entorno virtual
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    
    if not in_venv:
        print("No se detectó un entorno virtual activo.")
        create_venv = input("¿Desea crear y activar un nuevo entorno virtual? (s/n): ").lower()
        
        if create_venv == 's':
            print("\n Creando entorno virtual...")
            subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
            
            # Determinar el script de activación según el sistema operativo
            if sys.platform == "win32":
                activate_script = os.path.join("venv", "Scripts", "activate")
            else:
                activate_script = os.path.join("venv", "bin", "activate")
            
            print(f"\n🔧 Para activar el entorno virtual, ejecute:")
            if sys.platform == "win32":
                print(f"    {activate_script}")
            else:
                print(f"    source {activate_script}")
            
            print("\nLuego vuelva a ejecutar este script.")
            sys.exit(1)
        else:
            print("\n Continuando sin entorno virtual...")
    
    # Verificar si streamlit está instalado
    try:
        import streamlit
    except ImportError:
        print("\n Instalando dependencias...")
        subprocess.run([sys.executable, "-m", "pip", "install", "streamlit"], check=True)
    
    # Ejecutar la aplicación
    print("\n Iniciando la aplicación ANXRISK...")
    subprocess.run(["streamlit", "run", "app.py"])

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n ¡Hasta luego!")
        sys.exit(0)
    except Exception as e:
        print(f"\n Error: {e}")
        sys.exit(1)
