import traceback

import mysql.connector

from src.databases.conection2 import Conection
from src.models.repair import Repair
from src.utils.logger import Logger
from src.models.usuario import User
from src.models.detRepair import DetRepairacion

class DbRepair:
    def __init__(self):
        self.conn = None
        self.con = None
        self.cursor = None
        self.cliente = None
        self.lista = []
        self.lista_clientes = []

    def saveDetail(self, detReparacion):
        try:
            self.con = Conection()
            self.conn = self.con.open()
            self.cursor = self.conn.cursor()
            sql = """INSERT INTO det_reparaciones(
            folio_detalle,
            folio,
            pieza_id,
            cantidad) VALUES (%s,%s,%s,%s)"""
            datos = (detReparacion.getDetReparacion(),
                    detReparacion.getFolio(),
                    detReparacion.getPieza(),
                    detReparacion.getCantidad())
            self.cursor.execute(sql, datos)
            self.conn.commit()
        except mysql.connector.Error as error:
            Logger.add_to_log('error', str(error))
            Logger.add_to_log('error', traceback.format_exc())
        finally:
            self.conn.close()

    def close(self):
        if self.conn:
            self.conn.close()
        if self.cursor:
            self.cursor.close()
        if self.con:
            self.con.close()