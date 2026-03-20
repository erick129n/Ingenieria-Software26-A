import traceback

from src.databases.conection2 import Conection  # CORREGIDO: eliminado import duplicado y 'from models.piece import Pieza' (ruta incorrecta)
from src.utils.logger import Logger
from src.models.repair import Repair
from src.models.detRepair import DetRepairacion
from src.models.piece import Pieza
# CORREGIDO: eliminado 'from tkinter.constants import PIESLICE' — no se usa en ningún lado

class DbPieza:  # CORREGIDO: no debe heredar de Conection — usa composición, no herencia
    def __init__(self):
        self.con = None
        self.conn = None
        self.cursor = None
        self.pieza = Pieza()  # CORREGIDO: Pieza() no recibe argumentos en __init__ de esta forma; era Pieza(self) lo cual es incorrecto

    def save(self, pieza):
        try:
            self.con = Conection()
            self.conn = self.con.open()
            self.cursor = self.conn.cursor()
            # CORREGIDO: SQL tenía 5 %s pero solo 4 columnas (descripcion, precio, cantidad, n_serie)
            sql = 'INSERT INTO piezas (descripcion, precio, cantidad, n_serie) VALUES (%s, %s, %s, %s)'
            datos = (
                pieza.getDescripcion(),
                pieza.getPrecio(),    # CORREGIDO: get_precio() → getPrecio() (nombre real del getter)
                pieza.getCantidad(),  # CORREGIDO: get_cantidad() → getCantidad()
                pieza.getSerie()      # CORREGIDO: get_serie() → getSerie()
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

    def search(self, value):
        try:
            self.con = Conection()
            self.conn = self.con.open()
            self.cursor = self.conn.cursor()
            if isinstance(value, int):
                sql = 'SELECT * FROM piezas WHERE id_pieza = %s'
            else:
                sql = 'SELECT * FROM piezas WHERE n_serie = %s'

            self.cursor.execute(sql, (value,))
            row = self.cursor.fetchone()
            if row:
                aux = Pieza()
                # CORREGIDO: el orden de asignación era incorrecto (descripcion en row[0] pero id_pieza es la PK)
                aux.setIdPieza(row[0])
                aux.setDescripcion(row[1])
                aux.setPrecio(row[2])
                aux.setCantidad(row[3])
                aux.setSerie(row[4])
                return True, aux
            else:
                return False, None
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
            return False, None
        finally:
            self.close()

    def delete(self, pieza):
        try:
            self.con = Conection()
            self.conn = self.con.open()
            self.cursor = self.conn.cursor()
            sql = 'DELETE FROM piezas WHERE id_pieza = %s'
            self.cursor.execute(sql, (pieza.getIdPieza(),))  # CORREGIDO: get_id_pieza() → getIdPieza()
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
            return False
        finally:
            self.close()

    def editPiece(self, pieza):
        try:
            self.con = Conection()
            self.conn = self.con.open()
            self.cursor = self.conn.cursor()
            # CORREGIDO: faltaba la cláusula WHERE — sin ella se actualizarían TODAS las filas
            sql = """
            UPDATE piezas
            SET descripcion = %s,
                precio      = %s,
                cantidad    = %s,
                n_serie     = %s
            WHERE id_pieza  = %s
            """
            datos = (
                pieza.getDescripcion(),  # CORREGIDO: get_descripcion() → getDescripcion()
                pieza.getPrecio(),       # CORREGIDO: get_precio() → getPrecio()
                pieza.getCantidad(),     # CORREGIDO: get_cantidad() → getCantidad()
                pieza.getSerie(),        # CORREGIDO: get_serie() → getSerie()
                pieza.getIdPieza()       # CORREGIDO: agregado el ID para el WHERE
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

    def getMaxIdPieza(self):
        try:
            self.con = Conection()
            self.conn = self.con.open()
            self.cursor = self.conn.cursor()
            sql = 'SELECT MAX(id_pieza) id_pieza FROM piezas'
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            if result and result[0] is not None:
                return result[0] + 1
            return 1
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
            return 1
        finally:
            self.close()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        if self.con:
            self.con.close()