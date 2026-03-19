class DetRepairacion:
    def __init__(self,id_pieza=None,folio=None,detalle_folio=None,cantidad=None):
        self.id_pieza = id_pieza
        self.folio = folio
        self.detalle_folio = detalle_folio
        self.cantidad = cantidad
    def setIdPieza(self, id_pieza):
        self.id_pieza = id_pieza
    def setDetalleFolio(self, detalle_folio):
        self.detalle_folio = detalle_folio
    def setCantidad(self, cantidad):
        self.cantidad = cantidad
    def setFolio(self, folio):
        self.folio = folio

    def getidPieza(self):
        return self.id_pieza
    def getFolio(self):
        return self.folio
    def getDetalleFolio(self):
        return self.detalle_folio
    def getCantidad(self):
        return self.cantidad