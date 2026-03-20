import traceback

import mysql
import mysql.connector
from src.databases.conection2 import Conection
from src.models.usuario import User
from src.utils.logger import Logger


class DbUsuario:
    def __init__(self):
        self.con = None
        self.cursor = None
        self.conn = None

    def save(self, usuario):
        try:
            self.con = Conection()
            self.conn = self.con.open()
            self.cursor=self.conn.cursor()
            sql="INSERT INTO usuarios(id, nombre, username, password, perfil) VALUES (%s, %s, %s, %s, %s)"
            datos=(usuario.getUsuario_id(),
                        usuario.getNombre(),
                        usuario.getUserName(),
                        usuario.getPassword(),
                        usuario.getPerfil())
            self.cursor.execute(sql,datos)
            self.conn.commit()
            return True
        except mysql.connector.Error as e:
            Logger.add_to_log('error', 'Error MysQl en guardar:'+str(e))
            Logger.add_to_log('error', traceback.format_exc())
            return False
        finally:
            self.close()

    def getMecanicos(self):
        try:
            self.con = Conection()
            self.conn = self.con.open()
            self.cursor=self.conn.cursor()
            sql="SELECT * FROM usuarios WHERE perfil = 'Mecanicos' ORDER BY id"
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except Exception as e:
            Logger.add_to_log('error', str(e))
            return []
        finally:
            self.close()

    def getAllUsers(self):
        try:
            self.con = Conection()
            self.conn = self.con.open()
            self.cursor = self.conn.cursor()
            sql = "SELECT id FROM usuarios ORDER BY id"
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except Exception as e:
            Logger.add_to_log('error', str(e))
            return []
        finally:
            self.close()


    def search(self, usuario_id):
        aux = None
        try:
            self.con = Conection()
            self.conn = self.con.open()
            self.cursor = self.conn.cursor()

            sql="SELECT * FROM usuarios WHERE id= %s"
            self.cursor.execute(sql, (usuario_id,))
            row=self.cursor.fetchone()
            if row:
                aux = User()
                aux.setUsuario_id(int(row[0]))
                aux.setNombre(row[1])
                aux.setUserName(row[2])
                aux.setPassword(row[3])
                aux.setPerfil(row[4])
                return True, aux
            else:
                return False, None
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
        finally:
            self.close()

    def editar(self, usuario):
        try:
            self.con = Conection()
            self.conn = self.con.open()

            if not self.conn:
                return False

            self.cursor = self.conn.cursor()

            sql = """UPDATE usuarios
                     SET nombre   = %s,
                         username = %s,
                         password = %s,
                         perfil   = %s
                     WHERE id = %s"""

            datos = (
                usuario.getNombre(),
                usuario.getUserName(),
                usuario.getPassword(),
                usuario.getPerfil(),
                usuario.getUsuario_id()
            )

            self.cursor.execute(sql, datos)
            self.conn.commit()

            return self.cursor.rowcount > 0

        except mysql.connector.Error as e:
            Logger.add_to_log('error','Erorr Mysql al editar:'+ str(e))
            Logger.add_to_log('error', traceback.format_exc())
            return False
        finally:
            self.close()


    def borrar(self, usuario):
        try:
            self.con = Conection()
            self.conn = self.con.open()
            self.cursor=self.conn.cursor()

            sql="DELETE FROM usuarios WHERE id= %s"
            self.cursor.execute(sql, (usuario.getUsuario_id(),))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except mysql.connector.IntegrityError:
            Logger.add_to_log('warning', 'No se puede borrar porque tiene registros asociados')
            return False
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
            return False
        finally:
            self.close()

    def getMaxId(self):
        max_id=1
        try:
            self.con = Conection()
            self.conn = self.con.open()
            self.cursor=self.conn.cursor()
            sql="SELECT MAX(id) AS id FROM usuarios"
            self.cursor.execute(sql)
            resultado = self.cursor.fetchone()
            if resultado and resultado[0] is not None:
                max_id = resultado[0]+1
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
        finally:
            self.close()

        return max_id

    def getIdsUsers(self):
        try:
            self.con = Conection()
            self.conn = self.con.open()
            self.cursor=self.conn.cursor()
            sql="SELECT id FROM usuarios WHERE NOT perfil = 'Auxiliar' ORDER BY id"
            self.cursor.execute(sql)
            slist = self.cursor.fetchall()
            values=[row[0] for row in slist]
            return values
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
            return []
        finally:
            self.close()

    def buscar(self, id_usuario):
        try:
            self.con = Conection()
            self.conn = self.con.open()
            if not self.conn:
                return False, None
            self.cursor=self.conn.cursor()
            sql="SELECT * FROM usuarios WHERE id=%s"
            self.cursor.execute(sql, (id_usuario,))
            row = self.cursor.fetchone()
            if row:
                aux = User()
                aux.setUsuario_id(int(row[0]))
                aux.setNombre(row[1])
                aux.setUserName(row[2])
                aux.setPassword(row[3])
                aux.setPerfil(row[4])
                Logger.add_to_log('info', "Usuario encontrado: "+ str(aux.getUsuario_id()))
                return True, aux
            else:
                return False, None
        except mysql.connector.Error as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
            return False, None
        finally:
            self.close()

    def Autentificar(self, username, password):
        aux = None
        try:
            self.con = Conection()
            self.conn = self.con.open()
            if not self.conn:
                return False, None

            self.cursor=self.conn.cursor()
            sql="SELECT * FROM usuarios WHERE username=%s AND password=%s"
            self.cursor.execute(sql, (username, password))
            row=self.cursor.fetchone()
            if row:
                aux = User()
                aux.setUsuario_id(int(row[0]))
                aux.setNombre(row[1])
                aux.setUserName(row[2])
                aux.setPassword(row[3])
                aux.setPerfil(row[4])
                return True, aux
            else:
                Logger.add_to_log('error', "No hay datos")
                return False, None

        except mysql.connector.Error as err:
            Logger.add_to_log('error', "Eror MySQL:"+str(err))
            Logger.add_to_log('error', traceback.format_exc())
            return False, None
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
            return False, None
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