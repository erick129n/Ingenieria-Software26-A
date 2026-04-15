import traceback
import mysql.connector
# CORREGIDO: eliminado 'import mysql' suelto — mysql.connector es suficiente
from src.databases.conection2 import Conection
from src.utils.logger import Logger
from src.models.vehiculo import Vehiculo

class DbVehiculo:
    def __init__(self):
        self.conn = None
        self.con = None
        self.cursor = None
        self.cliente = None
        self.usuario = None
        self.vehiculo = None
        self.lista = []
        self.nombre_cliente = None

    def save(self, vehiculo):
        try:
            self.con = Conection()
            self.conn = self.con.open()
            self.cursor = self.conn.cursor()
            sql = '''INSERT INTO vehiculos(
                        matricula,
                        cliente_id,
                        marca,
                        modelo) VALUES(%s, %s, %s, %s)'''
            datos = (
                vehiculo.getMatricula(),
                vehiculo.getIdCliente(),
                vehiculo.getMarca(),
                vehiculo.getModelo()
            )
            self.cursor.execute(sql, datos)
            self.conn.commit()
            return True
        except mysql.connector.Error as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
            return False
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
            return False
        finally:
            self.close()

    def search(self, matricula):
        try:
            aux = None
            self.con = Conection()
            self.conn = self.con.open()
            self.cursor = self.conn.cursor()
            sql = '''SELECT vehiculos.matricula,
                            vehiculos.cliente_id,
                            vehiculos.marca,
                            vehiculos.modelo,
                            clientes.nombre
                     FROM vehiculos
                     JOIN clientes ON vehiculos.cliente_id = clientes.id_cliente
                     AND vehiculos.matricula = %s'''
            self.cursor.execute(sql, (matricula,))
            row = self.cursor.fetchone()
            if row:
                aux = Vehiculo()
                aux.setMatricula(row[0])
                aux.setId_cliente(row[1])
                aux.setMarca(row[2])
                aux.setModelo(row[3])
                self.nombre_cliente = row[4]
                self.lista.append(aux)
                return True, aux
            else:
                return False, None
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
            return False, None
        finally:
            self.close()

    def editar(self, vehiculo):
        try:
            self.con = Conection()
            self.conn = self.con.open()
            self.cursor = self.conn.cursor()
            # CORREGIDO: había una coma extra antes del WHERE — causaba SyntaxError en MySQL
            sql = '''UPDATE vehiculos
                     SET cliente_id = %s,
                         marca      = %s,
                         modelo     = %s
                     WHERE matricula = %s'''
            datos = (
                vehiculo.getIdCliente(),
                vehiculo.getMarca(),
                vehiculo.getModelo(),
                vehiculo.getMatricula()
            )
            self.cursor.execute(sql, datos)
            self.conn.commit()
            return self.cursor.rowcount > 0
        except mysql.connector.Error as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
            return False
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
            return False
        finally:
            self.close()

    def borrar(self, vehiculo):
        try:
            self.con = Conection()
            self.conn = self.con.open()
            self.cursor = self.conn.cursor()
            sql = 'DELETE FROM vehiculos WHERE matricula = %s'
            self.cursor.execute(sql, (vehiculo.getMatricula(),))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except mysql.connector.IntegrityError as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
            return False
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
            return False
        finally:
            self.close()

    def get_name_clintes(self):
        try:
            self.con = Conection()
            self.conn = self.con.open()
            self.cursor = self.conn.cursor()
            sql = 'SELECT nombre FROM clientes ORDER BY id_cliente'
            self.cursor.execute(sql)
            slist = self.cursor.fetchall()
            values = [row[0] for row in slist]
            return values
        except mysql.connector.Error as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
            return []
        finally:
            self.close()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        if self.con:
            self.con.close()
