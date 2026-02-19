class Reservacion:
    def __init__(self, id_reservacion, clienteID, id_habitacion, costo, fecha_reservacion, fecha_salida, hora_reserva):
        self.id_reservacion = id_reservacion
        self.clienteID = clienteID
        self.id_habitacion = id_habitacion
        self.fecha_reservacion = fecha_reservacion
        self.fecha_entrada = fecha_reservacion
        self.hora_reserva = hora_reserva
        self.fecha_salida = fecha_salida
        self.costo = costo
