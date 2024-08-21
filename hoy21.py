import mysql.connector
from mysql.connector import Error
from tabulate import tabulate

def conectar():
    try:
        conexion = mysql.connector.connect(
            host="18.116.82.240",
            port=3306,
            user="studentsucundi",
            password="mami_prende_la_radi0",
            database="employees"
        )
        if conexion.is_connected():
            print("Conexión exitosa")
            return conexion
    except Error as err:
        print(f"Error: {err}")
        return None

def mostrar_tablas(conexion):
    try:
        cursor = conexion.cursor()
        cursor.execute("SHOW TABLES")
        tablas = cursor.fetchall()
        print("Tablas en la base de datos:")
        for tabla in tablas:
            print(tabla[0])
    except Error as err:
        print(f"Error al obtener las tablas: {err}")
    finally:
        cursor.close()

def mostrar_estructura_tabla(conexion, nombre_tabla):
    try:
        cursor = conexion.cursor()
        cursor.execute(f"DESCRIBE {nombre_tabla}")
        estructura = cursor.fetchall()
        headers = ["Nombre", "Tipo", "Nulo", "Clave", "Predeterminado", "Extra"]
        filas = [(
            columna[0],  # Nombre
            columna[1],  # Tipo
            columna[2],  # Nulo
            columna[3],  # Clave
            columna[4],  # Predeterminado
            columna[5]   # Extra
        ) for columna in estructura]
        print(f"\nEstructura de la tabla {nombre_tabla}:")
        print(tabulate(filas, headers=headers, tablefmt="grid"))
    except Error as err:
        print(f"Error al obtener la estructura de la tabla {nombre_tabla}: {err}")
    finally:
        cursor.close()

def mostrar_datos_tabla(conexion, nombre_tabla):
    try:
        cursor = conexion.cursor()
        cursor.execute(f"SELECT * FROM {nombre_tabla}")
        datos = cursor.fetchall()
        cursor.execute(f"DESCRIBE {nombre_tabla}")
        columnas = cursor.fetchall()
        headers = [columna[0] for columna in columnas]
        print(f"\nDatos de la tabla {nombre_tabla}:")
        print(tabulate(datos, headers=headers, tablefmt="grid"))
    except Error as err:
        print(f"Error al obtener los datos de la tabla {nombre_tabla}: {err}")
    finally:
        cursor.close()

if __name__ == "__main__":
    conexion = conectar()
    if conexion:
        try:
            mostrar_tablas(conexion)
            mostrar_estructura_tabla(conexion, "empleados")
            mostrar_datos_tabla(conexion, "empleados")
        finally:
            conexion.close()
            print("Conexión cerrada")
