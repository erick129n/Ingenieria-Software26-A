import traceback

import mysql.connector

from src.databases.conection2 import Conection
from src.models.repair import Repair
from src.utils.logger import Logger
from src.models.detRepair import DetRepairacion


class DbRepair:
    def __init__(self):
        self.conn   = None
        self.con    = None
        self.cursor = None
        self.lista          = []
        self.lista_clientes = []

    # ════════════════════════════════════════════════════════════════════════
    # REPARACIONES
    # ════════════════════════════════════════════════════════════════════════

    def saveRepair(self, reparacion):
        try:
            self.con    = Conection()
            self.conn   = self.con.open()
            self.cursor = self.conn.cursor()
            sql = """INSERT INTO reparaciones(
                        matricula,
                        fecha_entrada,
                        fecha_salida,
                        descripcion,
                        usuario_id) VALUES (%s, %s, %s, %s, %s)"""
            datos = (
                reparacion.getMatricula(),
                reparacion.getFecha_entrada(),   # CORREGIDO: getFechaEntrada() → getFecha_entrada() (nombre real)
                reparacion.getFecha_saida(),     # CORREGIDO: getFechaSalida() → getFecha_saida() (nombre real)
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
            self.close()

    def searchRepair(self, rep_id):
        """Busca una reparación por su rep_id (folio)."""
        try:
            self.con    = Conection()
            self.conn   = self.con.open()
            self.cursor = self.conn.cursor()
            sql = "SELECT * FROM reparaciones WHERE rep_id = %s"
            self.cursor.execute(sql, (rep_id,))
            row = self.cursor.fetchone()
            if row:
                rep = Repair()
                rep.setFolio        (row[0])
                rep.setMatricula    (row[1])
                rep.setFecha_entrada(row[2])
                rep.setFecha_saida  (row[3])
                rep.setDescripcion  (row[4])
                rep.setUsuarioId    (row[5])
                return True, rep
            return False, None
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
            return False, None
        finally:
            self.close()

    def editRepair(self, reparacion):
        try:
            self.con    = Conection()
            self.conn   = self.con.open()
            self.cursor = self.conn.cursor()
            sql = """UPDATE reparaciones
                     SET fecha_entrada = %s,
                         fecha_salida  = %s,
                         descripcion   = %s
                     WHERE rep_id = %s"""
            datos = (
                reparacion.getFecha_entrada(),   # CORREGIDO: getFechaEntrada() → getFecha_entrada()
                reparacion.getFecha_saida(),     # CORREGIDO: getFechaSalida() → getFecha_saida()
                reparacion.getDescripcion(),
                reparacion.getFolio()            # CORREGIDO: getRepId() → getFolio() (Repair usa folio como PK)
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

    def deleteRepair(self, reparacion):
        try:
            self.con    = Conection()
            self.conn   = self.con.open()
            self.cursor = self.conn.cursor()
            sql = "DELETE FROM reparaciones WHERE rep_id = %s"
            self.cursor.execute(sql, (reparacion.getFolio(),))  # CORREGIDO: getRepId() → getFolio()
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
            return False
        finally:
            self.close()

    def getMaxRepId(self):
        try:
            self.con    = Conection()
            self.conn   = self.con.open()
            self.cursor = self.conn.cursor()
            sql = "SELECT MAX(rep_id) AS rep_id FROM reparaciones"
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

    # ════════════════════════════════════════════════════════════════════════
    # DETALLE DE REPARACIÓN
    # ════════════════════════════════════════════════════════════════════════

    def saveDetail(self, detReparacion):
        try:
            self.con    = Conection()
            self.conn   = self.con.open()
            self.cursor = self.conn.cursor()
            # CORREGIDO: columna 'precio' duplicada y getter getPieza() incorrecto para pieza_id
            sql = """INSERT INTO det_reparacion(
                        rep_id,
                        pieza_id,
                        cantidad) VALUES (%s, %s, %s)"""
            datos = (
                detReparacion.getRepId(),
                detReparacion.getidPieza(),  # CORREGIDO: getPieza() → getidPieza() (getter real del modelo)
                detReparacion.getCantidad(),
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
            self.con    = Conection()
            self.conn   = self.con.open()
            self.cursor = self.conn.cursor()
            sql = "SELECT * FROM det_reparacion WHERE folio = %s"
            self.cursor.execute(sql, (folio,))
            row = self.cursor.fetchone()
            if row:
                aux = DetRepairacion()
                aux.setFolio   (row[0])
                aux.setRepId   (row[1])
                aux.setIdPieza (row[2])
                aux.setCantidad(row[3])
                return True, aux
            return False, None
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
            return False, None
        finally:
            self.close()

    def get_detalles_by_rep(self, rep_id):
        """Retorna lista de DetRepairacion para un rep_id dado."""
        try:
            self.con    = Conection()
            self.conn   = self.con.open()
            self.cursor = self.conn.cursor()
            sql = "SELECT * FROM det_reparacion WHERE rep_id = %s"
            self.cursor.execute(sql, (rep_id,))
            rows = self.cursor.fetchall()
            result = []
            for row in rows:
                det = DetRepairacion()
                det.setFolio   (row[0])
                det.setRepId   (row[1])
                det.setIdPieza (row[2])
                det.setCantidad(row[3])
                result.append(det)
            return result
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
            return []
        finally:
            self.close()

    def deleteDetail(self, detReparacion):
        try:
            self.con    = Conection()
            self.conn   = self.con.open()
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

    def getMaxFolio(self):
        try:
            self.con    = Conection()
            self.conn   = self.con.open()
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

    # ════════════════════════════════════════════════════════════════════════
    # LISTAS PARA COMBOBOXES
    # ════════════════════════════════════════════════════════════════════════

    def get_lista_matriculas(self):
        try:
            self.con    = Conection()
            self.conn   = self.con.open()
            self.cursor = self.conn.cursor()
            self.cursor.execute("SELECT matricula FROM vehiculos ORDER BY matricula")
            return [str(row[0]) for row in self.cursor.fetchall()]
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
            return []
        finally:
            self.close()

    def get_lista_piezas(self):
        try:
            self.con    = Conection()
            self.conn   = self.con.open()
            self.cursor = self.conn.cursor()
            self.cursor.execute("SELECT descripcion FROM piezas ORDER BY descripcion")
            return [row[0] for row in self.cursor.fetchall()]
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
            return []
        finally:
            self.close()

    def get_map_piezas(self):
        try:
            self.con    = Conection()
            self.conn   = self.con.open()
            self.cursor = self.conn.cursor()
            self.cursor.execute("SELECT descripcion, id_pieza FROM piezas")
            return {row[0]: row[1] for row in self.cursor.fetchall()}
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
            return {}
        finally:
            self.close()

    # ════════════════════════════════════════════════════════════════════════
    # CONEXIÓN
    # ════════════════════════════════════════════════════════════════════════

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
