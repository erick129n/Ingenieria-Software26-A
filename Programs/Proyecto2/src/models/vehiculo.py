class Vehiculo:
    def __init__(self, matricula=None, id_cliente=None, marca=None, modelo=None):
        self.matricula = matricula
        self.id_cliente = id_cliente
        self.marca = marca
        self.modelo = modelo


    def setId_cliente(self, id_cliente):
        self.id_cliente = id_cliente

    def setMarca(self, marca):
        self.marca = marca
    def setModelo(self, modelo):
        self.modelo = modelo
    def setMatricula(self, matricula):
        self.matricula = matricula

    def getMatricula(self):
        return self.matricula
    def getIdCliente(self):
        return self.id_cliente
    def getMarca(self):
        return self.marca
    def getModelo(self):
        return self.modelo