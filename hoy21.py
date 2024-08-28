#Andres Felipe Gordo

import mysql.connector
from mysql.connector import Error
from tabulate import tabulate  

# Función para establecer una conexión con la base de datos
def conectar():
    try:
        conexion = mysql.connector.connect(
            host="18.188.124.77",  
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

# Función para mostrar las tablas existentes en la base de datos
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

# Función para mostrar la estructura de la tabla
def mostrar_estructura_tabla(conexion, nombre_tabla):
    try:
        cursor = conexion.cursor()
        cursor.execute(f"DESCRIBE {nombre_tabla}")
        estructura = cursor.fetchall()
        headers = ["Nombre", "Tipo", "Nulo", "Clave", "Predeterminado", "Extra"]
        filas = [(
            columna[0], 
            columna[1],  
            columna[2],  
            columna[3],  
            columna[4],  
            columna[5]   
        ) for columna in estructura]
        print(f"\nEstructura de la tabla {nombre_tabla}:")
        print(tabulate(filas, headers=headers, tablefmt="grid"))
    except Error as err:
        print(f"Error al obtener la estructura de la tabla {nombre_tabla}: {err}")
    finally:
        cursor.close()

# Función para mostrar los datos de la tabla
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

# Función para agregar un nuevo registro
def agregar_dato(conexion, nombre_tabla, datos):
    try:
        cursor = conexion.cursor()
        columnas = ', '.join(datos.keys())
        valores = ', '.join(['%s'] * len(datos))
        query = f"INSERT INTO {nombre_tabla} ({columnas}) VALUES ({valores})"
        cursor.execute(query, list(datos.values()))
        conexion.commit()
        print(f"Nuevo registro agregado a la tabla {nombre_tabla}")
    except Error as err:
        print(f"Error al agregar el dato a la tabla {nombre_tabla}: {err}")
    finally:
        cursor.close()

# Función para eliminar un registro
def eliminar_dato(conexion, nombre_tabla, condicion):
    try:
        cursor = conexion.cursor()
        cursor.execute(f"DELETE FROM {nombre_tabla} WHERE {condicion}")
        conexion.commit()
        print(f"Datos eliminados de la tabla {nombre_tabla} donde {condicion}")
    except Error as err:
        print(f"Error al eliminar los datos de la tabla {nombre_tabla}: {err}")
    finally:
        cursor.close()

# Función para editar (actualizar) datos en una tabla específica
def editar_dato(conexion, nombre_tabla, cambios, condicion):
    try:
        cursor = conexion.cursor()
        set_clause = ', '.join([f"{columna} = %s" for columna in cambios.keys()])
        valores = list(cambios.values())
        query = f"UPDATE {nombre_tabla} SET {set_clause} WHERE {condicion}"
        cursor.execute(query, valores)
        conexion.commit()
        print(f"Datos actualizados en la tabla {nombre_tabla} donde {condicion}")
    except Error as err:
        print(f"Error al actualizar los datos de la tabla {nombre_tabla}: {err}")
    finally:
        cursor.close()

# Bloque principal de ejecución
if __name__ == "__main__":
    conexion = conectar()
    if conexion:
        try:
            # Mostrar tablas
            mostrar_tablas(conexion)
            mostrar_estructura_tabla(conexion, "empleados")
            mostrar_datos_tabla(conexion, "empleados")
            
            # Agregar un nuevo empleado
            agregar_dato(conexion, "empleados", {"nombre": "Felipe", "salario": 350000, "puesto": "Estudiante"})
            
            # Eliminar un empleado 
            eliminar_dato(conexion, "empleados", "id = 6")
            
            # Editar un empleado 
            editar_dato(conexion, "empleados", {"nombre": "Cesar", "salario": 50000}, "id = 18")
        
        finally:
            conexion.close()
            print("Conexión cerrada")
