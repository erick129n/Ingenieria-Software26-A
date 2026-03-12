from enum import Enum
class Perfil(Enum):
    ADMINISTRADOR = 'Administrador'
    MECANICO = 'Mecanico'
    AUXILIAR = 'Auxiliar'
class User:
    def __init__(self, user_id=None, nombre=None, username=None, password=None, perfil=None):
        self.user_id = user_id
        self.nombre = nombre
        self.username = username
        self.password = password
        self.perfil = perfil

    # Getter methods
    def getUsuario_id(self):
        return self.user_id

    def getNombre(self):
        return self.nombre

    def getUserName(self):
        return self.username

    def getPassword(self):
        return self.password

    def getPerfil(self):
        return self.perfil

    # Setter methods (optional)
    def setUsuario_id(self, user_id):
        self.user_id = user_id

    def setNombre(self, nombre):
        self.nombre = nombre

    def setUserName(self, username):
        self.username = username

    def setPassword(self, password):
        self.password = password

    def setPerfil(self, perfil):
        self.perfil = perfil

    def es_mecanico(self):
        return self.perfil == Perfil.MECANICO.value
    def es_auxiliar(self):
        return self.perfil == Perfil.AUXILIAR.value
    def es_administrador(self):
        return self.perfil == Perfil.ADMINISTRADOR.value




    def puede_editar(self):
        return self.es_administrador()
    def puede_buscar(self):
        return not self.es_mecanico()
    def puede_crear(self):
        return self.es_administrador()

    def puede_asignar_mecanicos(self):
        return self.es_administrador()
    def puede_ver_clientes(self):
        return not self.es_mecanico()