import sqlite3
from datetime import datetime

class Libreria:
    def __init__(self):
        self.conexion = Conexiones()
        self.conexion.abrirConexion()
        self.conexion.miCursor.execute("CREATE TABLE IF NOT EXISTS LIBROS (id_libro INTEGER PRIMARY KEY, titulo VARCHAR(30), autor VARCHAR(30), isbn INTEGER NOT NULL, precio FLOAT NOT NULL,fecha_ultimo_precio VARCHAR(10), cantidadDisponibles INTEGER NOT NULL, UNIQUE(titulo, autor))")
        self.conexion.miCursor.execute("CREATE TABLE IF NOT EXISTS HISTORICO_LIBROS (id_libro INTEGER, isbn INTEGER, titulo VARCHAR(30), autor VARCHAR(30), genero VARCHAR(30), precio FLOAT NOT NULL, fecha_ultimo_precio VARCHAR(10), cantidad_disponible INTEGER NOT NULL)")
        self.conexion.miConexion.commit()
    
    def agregar_libro(self, titulo, autor, precio, cantidadDisponibles, isbn):
        try:
            self.conexion.miCursor.execute("INSERT INTO LIBROS (titulo, autor, precio, cantidadDisponibles, isbn) VALUES (?, ?, ?, ?, ?)", (titulo, autor, precio, cantidadDisponibles, isbn))
            self.conexion.miConexion.commit()
            print("Libro agregado exitosamente")
        except:
            print("Error al agregar un libro")
    
    def modificar_libro(self, titulo, autor, precio):
        try:
            self.conexion.miCursor.execute("UPDATE LIBROS SET precio = ? WHERE titulo = ? AND autor = ?", (precio, titulo, autor))
            self.conexion.miConexion.commit()
            print("Libro modificado correctamente")
        except:
            print("Error al modificar un libro")
    
    def borrar_libro(self,id):
        try:
            self.conexion.miCursor.execute("DELETE FROM LIBROS WHERE id_libro = ?",(id))
            self.conexion.miConexion.commit()
            print("Libro borrado correctamente")
        except:
            print("Error al borrar un libro")
    
    def cargar_stock(self,id,cantidad):
        try:
            self.conexion.miCursor.execute("UPDATE LIBROS SET cantidadDisponible = ? WHERE id_libro = ?",(cantidad,id))
            self.conexion.miConexion.commit()
            print("Stock actualizado correctamente")
        except:
            print("Error al actualizar stock")
    
    def listar_libros(self):
        try:
            self.conexion.miCursor.execute("SELECT * FROM LIBROS")
            libros = self.conexion.miCursor.fetchall()
            for x in libros:
                print(x)
        except:
            print("No se pudo listar libros.")
    
    def cerrar_libreria(self):
        self.conexion.cerrarConexion()

    def registrar_venta(self, id_libro, cantidad):
        try:
            fecha= datetime.now().strftime("%Y-%m-%d")
            self.conexion.miCursor.execute("CREATE TABLE IF NOT EXISTS Ventas (id_venta INTEGER PRIMARY KEY, id_libro INTEGER, cantidad INTEGER, fecha DATE)")
            self.conexion.miConexion.commit()
            self.conexion.miCursor.execute("INSERT INTO Ventas (id_libro, cantidad, fecha) VALUES (?, ?, ?)", (id_libro, cantidad, fecha))
            self.conexion.miConexion.commit()
            self.conexion.miCursor.execute("UPDATE LIBROS SET cantidadDisponibles = cantidadDisponibles - ? WHERE id_libro = ?",(cantidad, id_libro))
            self.conexion.miConexion.commit()
            print("Venta registrada exitosamente")
            print(fecha)
        except:
            print("Error al registrar la venta")
   
    def actualizar_precios(self, porcentaje):
        try:
            fecha= datetime.now().strftime("%Y-%m-%d")
            self.conexion.miCursor.execute("INSERT INTO HISTORICO_LIBROS SELECT * FROM LIBROS")
            self.conexion.miConexion.commit()
            self.conexion.miCursor.execute("UPDATE LIBROS SET precio = precio * (1 + ? / 100), fecha_ultimo_precio = ?",(porcentaje,fecha))
            self.conexion.miConexion.commit()
            print("Precios actualizados correctamente")
            print(fecha)
        except:
            print("Error al actualizar los precios")

    def mostrar_registros_anteriores(self, fecha):
        try:
            self.conexion.miCursor.execute("SELECT * FROM LIBROS WHERE fecha_ultimo_precio < ?",(fecha,))
            registros = self.conexion.miCursor.fetchall()
            print("Registros anteriores a la fecha especificada:")
            for registro in registros:
                print(registro)
        except:
            print("Error al mostrar los registros anteriores")


class Conexiones:
    def abrirConexion(self):
        self.miConexion = sqlite3.connect("Libreria.db")
        self.miCursor = self.miConexion.cursor()
        
    def cerrarConexion(self):
        self.miConexion.close()  


libreria = Libreria()

while True:
    print("Menu de opciones Libreria")
    print("1- Agregar libro")
    print("2- Modificar libro")
    print("3- Borrar un libro")
    print("4- Cargar disponibilidad")
    print("5- Listado de Libros")
    print("6- Ventas")
    print("7- Actualizar Precios")
    print("8- Listar libros por fecha")
    print("0- Salir del menú")
    
    opcion = int(input("Por favor ingrese un número: "))
    
    if opcion == 1:
        titulo = input("Por favor ingrese el título del libro: ")
        autor = input("Por favor ingrese el autor del libro: ")
        isbn = int(input("Por favor ingrese el ISBN del libro: "))
        precio = float(input("Por favor ingrese el precio del libro: "))
        cantidadDisponibles = int(input("Por favor ingrese la cantidad de unidades disponibles: "))
        libreria.agregar_libro(titulo, autor, precio, cantidadDisponibles,isbn)
    elif opcion == 2:
        titulo = input("Por favor ingrese el título del libro a modificar: ")
        autor = input("Por favor ingrese el autor del libro a modificar: ")
        precio = float(input("Por favor ingrese el nuevo precio del libro: "))
        libreria.modificar_libro(titulo, autor, precio)
    elif opcion ==3:
        id_libro_borrar = input("Ingrece id de libro a borrar: ")
        libreria.borrar_libro(id_libro_borrar)   
    elif opcion ==4:
        id_libro_borrar = input("Ingrece id de libro a borrar: ")
        cantidad_nueva = input("Ingrece el stock actual: ")
        libreria.cargar_stock(id_libro_borrar,cantidad_nueva)   
    elif opcion == 5:
        libreria.listar_libros()
    elif opcion == 6:
        id_libro = int(input("Por favor ingrese el ID del libro vendido: "))
        cantidad = int(input("Por favor ingrese la cantidad vendida: "))
        libreria.registrar_venta(id_libro, cantidad)
    elif opcion == 7:
        porcentaje = float(input("Por favor ingrese el porcentaje de aumento de precios: "))
        libreria.actualizar_precios(porcentaje)
    elif opcion == 8:
        fecha = input("Por favor ingrese la fecha en formato YYYY-MM-DD: ")
        libreria.mostrar_registros_anteriores(fecha)
    elif opcion == 0:
        libreria.cerrar_libreria()
        break