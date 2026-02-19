from Cliente.py import Cliente

def nuevoCliente(id_cliente, nombre, correo, telefono):
    cliente = Cliente(id_cliente, nombre, correo, telefono)
    return cliente