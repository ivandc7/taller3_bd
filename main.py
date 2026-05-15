import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from faker import Faker
# Autor: Ivan Durango - Taller 3 Automatización

def main():
    # 1. Cargamos las credenciales secretas desde el archivo .env
    load_dotenv()
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")

    # 2. Conexión Inicial (Para crear la Base de Datos si no existe)
    # Nos conectamos al motor general primero
    url_server = f"mysql+pymysql://{user}:{password}@{host}:{port}/"
    engine_server = create_engine(url_server)

    with engine_server.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))
        print(f"Base de datos '{db_name}' verificada/creada.")

    # 3. Conexión Específica a nuestra Base de Datos
    url_db = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"
    engine = create_engine(url_db)

    # 4. Creación de la Tabla (DDL automatizado)
    nombre_tabla = "personas_ivan"  # Cumple con el formato personas_<tu_nombre> como lo estás pidiendo profe
    
    ddl_query = f"""
    CREATE TABLE IF NOT EXISTS {nombre_tabla} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(100),
        correo VARCHAR(100),
        fecha_nacimiento DATE,
        ciudad VARCHAR(100),
        telefono VARCHAR(50),
        trabajo VARCHAR(100),
        empresa VARCHAR(100)
    )
    """
    
    with engine.connect() as conn:
        # Ejecutamos el DDL
        conn.execute(text(ddl_query))
        print(f"Tabla '{nombre_tabla}' verificada/creada con éxito.")

        # 5. Generación de Datos falsos (Faker)
        fake = Faker('es_CO') # Genera datos con formato de Colombia
        cantidad_registros = 100000
        lote_datos = [] # Aquí guardaremos los diccionarios

        print(f"Generando {cantidad_registros} registros falsos... (esto tomará unos segundos)")
        
        for _ in range(cantidad_registros):
            # Creamos un diccionario por cada persona (7 atributos exigidos)
            registro = {
                "p_nombre": fake.name(),
                "p_correo": fake.email(),
                "p_fecha": fake.date_of_birth(minimum_age=18, maximum_age=80),
                "p_ciudad": fake.city(),
                "p_telefono": fake.phone_number(),
                "p_trabajo": fake.job(),
                "p_empresa": fake.company()
            }
            lote_datos.append(registro)

        # 6. Inserción por Lotes (Optimización que se exige en la pista 4)
        print("Insertando 100,000 registros en MySQL de un solo golpe...")
        
        insert_query = text(f"""
            INSERT INTO {nombre_tabla} 
            (nombre, correo, fecha_nacimiento, ciudad, telefono, trabajo, empresa) 
            VALUES (:p_nombre, :p_correo, :p_fecha, :p_ciudad, :p_telefono, :p_trabajo, :p_empresa)
        """)
        
        # Si pasamos la lista de diccionarios, SQLAlchemy hace la inserción masiva automáticamente
        conn.execute(insert_query, lote_datos)
        conn.commit() # Axioma de Transacción: Guardar los cambios permanentemente
        
        print("¡Proceso completado con éxito! Revisa DBeaver.")

# Bloque de ejecución como usted lo está pidiendo profe
if __name__ == "__main__":
    main()
