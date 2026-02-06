import os

from Persona import Cliente

class Archivos():
    def __init__(self, nombre_archivo):
        self.nombre_archivo = nombre_archivo

    def guardar_cliente(self, cliente):
        with open(self.nombre_archivo, 'a') as archivo:
            archivo.write(f"{cliente.nombre},{cliente.direccion},{cliente.telefono},{cliente.genero},{cliente.nacimiento},{cliente.talla},{cliente.imc}\n")

    def cargar_clientes(self):
        clientes = []
        if os.path.exists(self.nombre_archivo):
            with open(self.nombre_archivo, 'r') as archivo:
                for linea in archivo:
                    datos = linea.strip().split(',')
                    if len(datos) == 7:
                        cliente = Cliente(*datos)
                        clientes.append(cliente)
        return clientes