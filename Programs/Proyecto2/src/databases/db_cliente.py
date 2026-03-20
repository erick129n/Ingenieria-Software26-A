import traceback

from src.databases.conection2 import Conection
from src.utils.logger import Logger
from src.models.cliente import Cliente
from src.models.usuario import User


class DBCliente:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.con = None
        self.usuario = User()

    def save(self, cliente):
        try:
            self.con = Conection()
            self.conn = self.con.open()
            self.cursor = self.conn.cursor()
            sql="INSERT INTO clientes(id_cliente, nombre, telefono, email, rfc, usuario_id) VALUES (%s, %s, %s, %s, %s, %s)"
            datos=(cliente.getIdCliente(),
                   cliente.getNombre(),
                   cliente.getTelefono(),
                   cliente.getEmail(),
                   cliente.getRfc(),
                   cliente.getUserId())
            self.cursor.execute(sql, datos)
            self.conn.commit()
            self.con.close()
            return True
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('erorr', traceback.format_exc())
            return False
        finally:
            self.close()

    def search(self, nombre):
        try:
            self.con = Conection()
            self.conn = self.con.open()
            self.cursor = self.conn.cursor()
            sql="SELECT * FROM clientes WHERE nombre = %s"
            self.cursor.execute(sql, (nombre,))
            row = self.cursor.fetchone()
            if row:
                aux = Cliente()
                aux.setId_cliente(row[0])
                aux.setNombre(row[1])
                aux.setTelefono(row[2])
                aux.setEmail(row[3])
                aux.setRfc(row[4])
                aux.setUserId(row[5])
                return True, aux
            else:
                return False, None
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('erorr', traceback.format_exc())
            return False, None
        finally:
            self.close()
    def editar(self, cliente):
        try:
            self.con = Conection()
            self.conn = self.con.open()
            self.cursor = self.conn.cursor()

            sql="""
            UPDATE clientes
            SET nombre = %s,
                telefono = %s,
                email = %s,
                rfc = %s,
                usuario_id = %s
                WHERE id_cliente = %s
            """

            datos=(cliente.getNombre(),
                   cliente.getTelefono(),
                   cliente.getEmail(),
                   cliente.getRfc(),
                   cliente.getUserId(),
                   cliente.getIdCliente()
            )

            self.cursor.execute(sql, datos)
            self.conn.commit()

            return self.cursor.rowcount > 0
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('erorr', traceback.format_exc())
            return False
        finally:
            self.close()


    def borrar(self, cliente):
        try:
            self.con = Conection()
            self.conn = self.con.open()
            self.cursor = self.conn.cursor()
            sql="DELETE FROM clientes WHERE id_cliente = %s"
            self.cursor.execute(sql, (cliente.getIdCliente(),))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('erorr', traceback.format_exc())
            return False
        finally:
            self.close()

    def getMaxId(self):
        maxId=1
        try:
            self.con = Conection()
            self.conn = self.con.open()
            self.cursor = self.conn.cursor()
            sql="SELECT MAX(id_cliente) AS id_cliente FROM clientes"
            self.cursor.execute(sql)
            resultado = self.cursor.fetchone()
            if resultado and resultado[0] is not None:
                maxId = resultado[0]+1
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('erorr', traceback.format_exc())

        finally:
            self.close()
        return maxId

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        if self.con:
            self.con.close()