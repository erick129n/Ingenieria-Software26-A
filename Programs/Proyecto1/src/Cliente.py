class Cliente:
    def __init__(self, id_cliente, nombre, direccion, correo, telefono):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.direccion = direccion  # Agregado para almacenar la dirección del cliente
        self.correo = correo
        self.telefono = telefono