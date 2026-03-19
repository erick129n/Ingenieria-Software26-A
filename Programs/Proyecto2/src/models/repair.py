
class Repair:
    def __init__(self, folio=None, pieza=None, id_pieza=None, matricula=None, fecha_entrada=None, fecha_saida=None, descripcion=None, cantidad=None, usuario_id=None):
        self.folio = folio
        self.pieza = pieza
        self.matricula = matricula
        self.fecha_entrada = fecha_entrada
        self.fecha_saida = fecha_saida
        self.descripcion = descripcion
        self.cantidad = cantidad
        self.usuario_id = usuario_id
        self.id_pieza = id_pieza


    def getFolio(self):
        return self.folio
    def getPieza(self):
        return self.pieza
    def getMatricula(self):
        return self.matricula
    def getFecha_entrada(self):
        return self.fecha_entrada
    def getFecha_saida(self):
        return self.fecha_saida
    def getDescripcion(self):
        return self.descripcion
    def getCantidad(self):
        return self.cantidad
    def getUsuarioId(self):
        return self.usuario_id
    def getIdPieza(self):
        return self.id_pieza


    def setFolio(self, folio):
        self.folio = folio
    def setPieza(self, pieza):
        self.pieza = pieza
    def setMatricula(self, matricula):
        self.matricula = matricula
    def setFecha_entrada(self, fecha_entrada):
        self.fecha_entrada = fecha_entrada
    def setFecha_saida(self, fecha_saida):
        self.fecha_saida = fecha_saida
    def setDescripcion(self, descripcion):
        self.descripcion = descripcion
    def setCantidad(self, cantidad):
        self.cantidad = cantidad
    def setUsuarioId(self, usuario_id):
        self.usuario_id = usuario_id
    def setIdPieza(self, id_pieza):
        self.id_pieza = id_pieza