import traceback
from tkinter.constants import PIESLICE

from models.piece import Pieza
from src.databases.conection2 import Conection
from src.utils.logger import Logger
from src.models.repair import Repair
from src.models.detRepair import DetRepairacion
from src.models.piece import Pieza

class DbPieza(Conection):
    def __init__(self):
        self.con =None
        self.conn = None
        self.cursor = None
        self.pieza = Pieza(self)

    def save(self, pieza):
        try:
            self.con = Conection()
            self.conn = self.con.open()
            self.cursor = self.conn.cursor()
            sql = 'INSERT INTO piezas (descripcion, precio, cantidad, n_serie)  VALUES (%s, %s, %s, %s, %s)'
            datos = (
                pieza.get_descripcion(),
                pieza.get_precio(),
                pieza.get_cantidad(),
                pieza.get_serie()
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
                    aux.setDescripcion(row[0])
                    aux.setIdPieza(row[1])
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
            self.cursor.execute(sql, (pieza.get_id_pieza(),))
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
            sql = """
            UPDATE piezas
            SET descripcion = %s,
                  precio = %s,
                  cantidad = %s,
                  n_serie = %s"""
            datos = (
                pieza.get_descripcion(),
                pieza.get_precio(),
                pieza.get_cantidad(),
                pieza.get_serie()
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
                return result[0]+1
            return 1
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
            return False
        finally:
            self.close()
    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        if self.con:
            self.con.close()