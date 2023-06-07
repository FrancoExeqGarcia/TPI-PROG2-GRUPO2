import sqlite3

class Libreria:
    def _init_(self):
        self.conexion = Conexiones()
        self.conexion.abrirConexion()
        self.conexion.miCursor.execute(
            "create table if not exists LIBROS (id_libro INTEGER PRIMARY KEY, titulo VARCHAR(30), autor VARCHAR(30),genero VARCHAR(30), precio FLOAT NOT NULL,FechaUltimoPrecio VARCHAR(10),  cantidadDisponibles INTEGER NOT NULL, UNIQUE(titulo, autor))")
        self.conexion.miConexion.commit()

    def agregar_libro(self, titulo, autor, precio, cantidadDisponibles):
        try:
            self.conexion.miCursor.execute(
                "INSERT INTO LIBROS (titulo, autor, precio, cantidadDisponibles) VALUES (?, ?, ?, ?)",
                (titulo, autor, precio, cantidadDisponibles))
            self.conexion.miConexion.commit()
            print("Libro agregado exitosamente")
        except:
            print("Error al agregar un libro")

    def modificar_libro(self, titulo, autor, precio):
        try:
            self.conexion.miCursor.execute("UPDATE LIBROS SET precio = ? WHERE titulo = ? AND autor = ?",
                                           (precio, titulo, autor))
            self.conexion.miConexion.commit()
            print("Libro modificado correctamente")
        except:
            print("Error al modificar un libro")

    def borrar_libro(self, id):
        try:
            self.conexion.miCursor.execute("DELETE FROM LIBROS WHERE id_libro = ?", (id))
            self.conexion.miConexion.commit()
            print("Libro borrado correctamente")
        except:
            print("Error al borrar un libro")

    def cargar_stock(self, id, cantidad):
        try:
            self.conexion.miCursor.execute("UPDATE LIBROS SET cantidadDisponible = ? WHERE id_libro = ?",
                                           (cantidad, id))
            self.conexion.miConexion.commit()
            print("Stock actualizado correctamente")
        except:
            print("Error al actualizar stock")

    def cerrar_libreria(self):
        self.conexion.cerrarConexion()





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
    print("0- Salir del menú")

    opcion = int(input("Por favor ingrese un número: "))

    if opcion == 1:
        titulo = input("Por favor ingrese el título del libro: ")
        autor = input("Por favor ingrese el autor del libro: ")
        precio = float(input("Por favor ingrese el precio del libro: "))
        cantidadDisponibles = int(input("Por favor ingrese la cantidad de unidades disponibles: "))
        libreria.agregar_libro(titulo, autor, precio, cantidadDisponibles)
    elif opcion == 2:
        titulo = input("Por favor ingrese el título del libro a modificar: ")
        autor = input("Por favor ingrese el autor del libro a modificar: ")
        precio = float(input("Por favor ingrese el nuevo precio del libro: "))
        libreria.modificar_libro(titulo, autor, precio)
    elif opcion == 3:
        id_libro_borrar = input("Ingrece id de libro a borrar: ")
        libreria.borrar_libro(id_libro_borrar)
    elif opcion == 4:
        id_libro_borrar = input("Ingrece id de libro a borrar: ")
        cantidad_nueva = input("Ingrece el stock actual: ")
        libreria.cargar_stock(id_libro_borrar, cantidad_nueva)
    elif opcion == 0:
        libreria.cerrar_libreria()
        break