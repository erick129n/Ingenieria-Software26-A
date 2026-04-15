class Pieza:
    def __init__(self, id_pieza=None, descripcion=None, precio=None, cantidad=None, n_serie=None):
        self.id_pieza = id_pieza       # CORREGIDO: faltaba self.
        self.descripcion = descripcion  # CORREGIDO: faltaba self.
        self.precio = precio            # CORREGIDO: faltaba self.
        self.cantidad = cantidad        # CORREGIDO: faltaba self.
        self.n_serie = n_serie         # CORREGIDO: faltaba self.

    def setIdPieza(self, id_pieza):
        self.id_pieza = id_pieza
    def setDescripcion(self, descripcion):
        self.descripcion = descripcion
    def setPrecio(self, precio):
        self.precio = precio
    def setCantidad(self, cantidad):
        self.cantidad = cantidad
    def setSerie(self, n_serie):
        self.n_serie = n_serie

    def getIdPieza(self):
        return self.id_pieza
    def getDescripcion(self):
        return self.descripcion
    def getPrecio(self):
        return self.precio
    def getCantidad(self):
        return self.cantidad
    def getSerie(self):
        return self.n_serie