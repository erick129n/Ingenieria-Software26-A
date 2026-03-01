from Cliente import Cliente
from Habitacion import Room  # Asumo que esta es la clase correcta
from Reservacion import Reservacion
import os

class Archivo:
    def __init__(self, nombre_archivo):
        self.nombre_archivo = nombre_archivo
    
    def guardar_cliente(self, cliente):
        """Guarda un objeto Cliente en el archivo"""
        with open(self.nombre_archivo, 'a') as archivo:
            # Formato: Cliente|id|nombre|direccion|correo|telefono
            linea = f"{cliente.id_cliente}|{cliente.nombre}|{cliente.direccion}|{cliente.correo}|{cliente.telefono}\n"
            archivo.write(linea)
    
    def guardar_habitacion(self, habitacion):
        """Guarda un objeto Habitacion en el archivo"""
        with open(self.nombre_archivo, 'a') as archivo:
            # Asumo los atributos de Habitacion, ajústalo según tu clase
            linea = f"{habitacion.id_habitacion}|{habitacion.numero}|{habitacion.estado}\n"
            archivo.write(linea)
    
    def guardar_reservacion(self, reservacion):
        """Guarda un objeto Reservacion en el archivo"""
        with open(self.nombre_archivo, 'a') as archivo:
            # Asumo los atributos de Reservacion, ajústalo según tu clase
            linea = f"{reservacion.id_reservacion}|{reservacion.id_cliente}|{reservacion.id_habitacion}|{reservacion.fecha_entrada}|{reservacion.fecha_salida}\n"
            archivo.write(linea)
     
    def cargar_datos_cliente(self):
        """Carga los datos del archivo y los separa en listas de objetos"""
        clientes = []
        if os.path.exists(self.nombre_archivo):
            with open(self.nombre_archivo, 'r') as archivo:
                for linea in archivo:
                    linea = linea.strip()
                    if not linea:
                        continue
                    
                    partes = linea.split('|')
                    
                    try:
                        cliente = Cliente(
                            id_cliente=int(partes[0]),
                            nombre=partes[1],
                            direccion=partes[2],
                            correo=partes[3],
                            telefono=partes[4]
                        )
                        clientes.append(cliente)
                            
                      
                    except Exception as e:
                        print(f"Error al cargar línea: {linea}")
                        print(f"Error: {e}")
        
        return clientes
    
    def cargar_datos_habitacion(self):
        """Carga los datos del archivo y los separa en listas de objetos"""
        habitaciones = []
        if os.path.exists(self.nombre_archivo):
            with open(self.nombre_archivo, 'r') as archivo:
                for linea in archivo:
                    linea = linea.strip()
                    if not linea:
                        continue
                    
                    partes = linea.split('|')
                    
                    try:
                        habitacion = Room(
                            id_habitacion=int(partes[0]),
                            numero=partes[1],
                            estado=partes[2]
                        )
                        habitaciones.append(habitacion)
                            
                      
                    except Exception as e:
                        print(f"Error al cargar línea: {linea}")
                        print(f"Error: {e}")
        
        return habitaciones
    
    def cargar_datos_reservacion(self):
        """Carga los datos del archivo y los separa en listas de objetos"""
        reservaciones = []
        if os.path.exists(self.nombre_archivo):
            with open(self.nombre_archivo, 'r') as archivo:
                for linea in archivo:
                    linea = linea.strip()
                    if not linea:
                        continue
                    
                    partes = linea.split('|')
                    
                    try:
                        reservacion = Reservacion(
                            id_reservacion=int(partes[0]),
                            clienteID=int(partes[1]),
                            id_habitacion=int(partes[2]),
                            costo=float(partes[3]),  # Asumo que el costo es un número, ajusta si es necesario
                            fecha_reservacion=partes[4],
                            fecha_salida=partes[5],
                            hora_reserva=partes[6],
                        )
                        reservaciones.append(reservacion)
                            
                      
                    except Exception as e:
                        print(f"Error al cargar línea: {linea}")
                        print(f"Error: {e}")
        
        return reservaciones