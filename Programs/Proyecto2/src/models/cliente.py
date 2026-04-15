# CORREGIDO: eliminado 'from src.models.usuario import User' — no se usa en esta clase

class Cliente:
    def __init__(self, id_cliente=None, nombre=None, telefono=None, email=None, rfc=None, userId=None):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.telefono = telefono
        self.email = email
        self.rfc = rfc
        self.userId = userId

    def setId_cliente(self, id_cliente):
        self.id_cliente = id_cliente
    def setNombre(self, nombre):
        self.nombre = nombre
    def setTelefono(self, telefono):
        self.telefono = telefono
    def setEmail(self, email):
        self.email = email
    def setRfc(self, rfc):
        self.rfc = rfc
    def setUserId(self, userId):
        self.userId = userId

    def getIdCliente(self):
        return self.id_cliente
    def getNombre(self):
        return self.nombre
    def getTelefono(self):
        return self.telefono
    def getEmail(self):
        return self.email
    def getRfc(self):
        return self.rfc
    def getUserId(self):
        return self.userId