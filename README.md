# Automatización de BD con Python y Faker

Este proyecto es un script automatizado que genera 100,000 registros de personas sintéticas utilizando la librería "Faker" y los inserta mediante procesamiento por lotes (batch insert) en una base de datos MySQL local utilizando "SQLAlchemy".

## Prerrequisitos
- Python 3.10+
- MySQL Server local
- Entorno virtual configurado

## Instalación y Ejecución
1. Clonar el repositorio.
2. Crear y activar un entorno virtual: "python -m venv .venv"
3. Instalar dependencias: "pip install -r requirements.txt"
4. Configurar las variables de entorno basándose en el archivo ".env.example".
5. Ejecutar el script principal:
   ```bash
   python main.py
## Autor
Desarrollado por Ivan para el curso de Bases de Datos para Ciencia de Datos.