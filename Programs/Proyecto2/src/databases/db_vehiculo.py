import traceback

from src.databases.conection2 import Conection
from enum import nonmember
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
        self.lista=[]
        self.nombre_cliente = None

    def save(self, vehiculo):
        try:
            self.con = Conection()
            self.conn = self.con.open()
            self.cursor=self.conn.cursor()
            sql=('''INSERT INTO vehiculos(
                                matricula,
                                cliente_id,
                                marca,
                                modelo) VALUES(%s,%s,%s,%s)''')
            datos=(vehiculo.getMatricula(),
                        vehiculo.getCliente(),
                        vehiculo.getMarca(),
                        vehiculo.getModelo())
            self.cursor.execute(sql, datos)
            self.conn.commit()
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
        finally:
            self.conn.close()

    def search(self, vehiculo):
        try:
            aux =None
            self.con = Conection()
            self.conn=self.con.open()
            self.cursor=self.conn.cursor()
            sql=('''SELECT vehiculos.matricula,
                          vehiculos.cliente_id,
                          vehiculos.marca,
                          vehiculos.modelo,
                          clientes.nombre FROM vehiculos JOIN clientes ON vehiculos.cliente_id = clientes.id AND vehiculos.matricula = %s
            ''')
            self.cursor.execute(sql,(vehiculo.getMatricula(),))
            row = self.cursor.fetchone()
            if row:
                aux = Vehiculo()
                aux.matricula = row[0],
                aux.cliente_id = row[1],
                aux.marca = row[2],
                aux.modelo = row[3],
                aux.nombre = row[4],
                self.nombre_cliente = row[5]
                self.lista.append(aux)
                return True, aux
            else:
                return False, aux
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
            return False, aux
        finally:
            self.conn.close()

    def editar(self, vehiculo):
        try:
            self.con = Conection()
            self.conn=self.con.open()
            self.cursor=self.conn.cursor()

            sql=('''UPDATE
                    vehiculos SET
                 matricula = %s,
                 cliente_id = %s,
                 marca = %s,
                 modelo = %s,
                 nombre = %s
                 WHERE matricula = %s''')
            datos=(vehiculo.getMatricula(),
                   vehiculo.getCliente(),
                   vehiculo.getMarca(),
                   vehiculo.getModelo()
                   )
            self.cursor.execute(sql, datos)
            self.conn.commit()

            return self.cursor.rowcount > 0
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
        finally:
            self.conn.close()

    def borrar(self, vehiculo):
        try:
            self.con = Conection()
            self.conn=self.con.open()
            self.cursor=self.conn.cursor()
            sql=('''SELECT * FROM vehiculos WHERE matricula = %s''')
            self.cursor.execute(sql,(vehiculo.getMatricula(),))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            Logger.add_to_log('error', str(e))
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