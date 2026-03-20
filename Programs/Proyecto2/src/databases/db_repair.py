import traceback

import mysql.connector

from src.databases.conection2 import Conection
from src.models.repair import Repair
from src.utils.logger import Logger
from src.models.detRepair import DetRepairacion


class DbRepair:
    def __init__(self):
        self.conn = None
        self.con = None
        self.cursor = None
        self.lista = []
        self.lista_clientes = []

    def saveRepair(self, reparacion):
        try:
            self.con = Conection()
            self.conn = self.con.open()
            self.cursor = self.conn.cursor()
            sql = """INSERT INTO reparaciones(
                        matricula,
                        fecha_entrada,
                        fecha_salida,
                        descripcion,
                        usuario_id) VALUES (%s, %s, %s, %s, %s)"""
            datos = (
                reparacion.getMatricula(),
                reparacion.getFechaEntrada(),
                reparacion.getFechaSalida(),
                reparacion.getDescripcion(),
                reparacion.getUsuarioId()
            )
            self.cursor.execute(sql, datos)
            self.conn.commit()
            return True
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
            return False
        finally:
            self.close()  # FIX: eliminado el close() doble del try, solo queda el finally

    def saveDetail(self, detReparacion):
        """
        FIX: eliminada la definición duplicada del método.
        Se conserva esta versión (sin folio en el INSERT, ya que es autoincremental).
        """
        try:
            self.con = Conection()
            self.conn = self.con.open()
            self.cursor = self.conn.cursor()
            sql = """INSERT INTO det_reparacion(
                        rep_id,
                        pieza_id,
                        cantidad) VALUES (%s, %s, %s)"""
            datos = (
                detReparacion.getRepId(),
                detReparacion.getPieza(),
                detReparacion.getCantidad()
            )
            self.cursor.execute(sql, datos)
            self.conn.commit()
            return True
        except mysql.connector.Error as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
            return False
        finally:
            self.close()

    def searchFolio(self, folio):
        try:
            self.con = Conection()
            self.conn = self.con.open()
            self.cursor = self.conn.cursor()
            sql = "SELECT * FROM det_reparacion WHERE folio = %s"
            self.cursor.execute(sql, (folio,))
            row = self.cursor.fetchone()
            if row:
                aux = DetRepairacion()
                aux.setFolio(row[0])
                aux.setRepId(row[1])
                aux.setIdPieza(row[2])
                aux.setCantidad(row[3])
                return True, aux
            else:
                return False, None
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
            return False, None
        finally:
            self.close()

    def deleteDetail(self, detReparacion):
        try:
            self.con = Conection()
            self.conn = self.con.open()
            self.cursor = self.conn.cursor()
            sql = "DELETE FROM det_reparacion WHERE folio = %s"
            self.cursor.execute(sql, (detReparacion.getFolio(),))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
            return False
        finally:
            self.close()

    def deleteRepair(self, reparacion):
        try:
            self.con = Conection()
            self.conn = self.con.open()
            self.cursor = self.conn.cursor()
            sql = "DELETE FROM reparaciones WHERE rep_id = %s"
            self.cursor.execute(sql, (reparacion.getRepId(),))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
            return False
        finally:
            self.close()

    def editRepair(self, reparacion):
        try:
            self.con = Conection()
            self.conn = self.con.open()
            self.cursor = self.conn.cursor()
            # FIX: SQL completamente reescrito — faltaban "= %s" en SET y faltaba WHERE
            sql = """UPDATE reparaciones
                     SET fecha_entrada = %s,
                         fecha_salida  = %s,
                         descripcion   = %s
                     WHERE rep_id = %s"""
            datos = (
                reparacion.getFechaEntrada(),
                reparacion.getFechaSalida(),
                reparacion.getDescripcion(),
                reparacion.getRepId()
            )
            self.cursor.execute(sql, datos)
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
            return False
        finally:
            self.close()

    def getMaxFolio(self):
        try:
            self.con = Conection()
            self.conn = self.con.open()
            self.cursor = self.conn.cursor()
            sql = "SELECT MAX(folio) AS folio FROM det_reparacion"
            self.cursor.execute(sql)
            resultado = self.cursor.fetchone()
            if resultado and resultado[0] is not None:
                return resultado[0] + 1
            return 1
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
            return 1
        finally:
            self.close()

    def getMaxRepId(self):
        try:
            self.con = Conection()
            self.conn = self.con.open()
            self.cursor = self.conn.cursor()
            sql = "SELECT MAX(rep_id) AS rep_id FROM reparaciones"
            self.cursor.execute(sql)
            resultado = self.cursor.fetchone()
            # FIX: verificar que resultado[0] no sea None (tabla vacía)
            if resultado and resultado[0] is not None:
                return resultado[0] + 1
            return 1
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
            return 1
        finally:
            self.close()

    def close(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
            if self.con:
                self.con.close()
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())