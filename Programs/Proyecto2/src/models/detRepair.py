class DetRepairacion:
    def __init__(self,folio=None, rep_id=None, pieza_id=None, cantidad=None):
        self.folio = folio
        self.cantidad = cantidad
        self.id_pieza = pieza_id
        self.rep_id = rep_id


    def setIdPieza(self, id_pieza):
        self.id_pieza = id_pieza
    def setRepId(self, rep_id):
        self.rep_id = rep_id
    def setCantidad(self, cantidad):
        self.cantidad = cantidad
    def setFolio(self, folio):
        self.folio = folio

    def getidPieza(self):
        return self.id_pieza
    def getFolio(self):
        return self.folio
    def getRepId(self):
        return self.rep_id
    def getCantidad(self):
        return self.cantidad