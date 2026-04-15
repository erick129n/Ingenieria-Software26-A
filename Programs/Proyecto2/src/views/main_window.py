import tkinter as tk
import traceback
from tkinter import messagebox
from src.databases.dbUsuario import DbUsuario  # CORREGIDO: faltaba 'src.'
from src.utils.logger import Logger
from src.views.loggin_window import logginWindow
from src.views.Pages.user_page import UserPage
from src.views.Pages.client_page import ClientPage
from src.views.Pages.vehicle_page import VehiculoPage
from src.views.Pages.main_page import MainPage
from src.views.Pages.piece_page import PiezaPage
from src.views.Pages.repair_page import RepairPage

class MainWindow(tk.Tk):

    cliente = None
    vehiculo = None
    reparaciones = None
    piezas = None

    def __init__(self):
        super().__init__()
        self.title("Main Window")
        self.geometry("700x400")
        self.container = None
        self.pageUser = None
        self.pageClient = None
        self.pageVehiculo = None
        self.pagePieza = None
        self.pageReparaciones = None
        self.label_principal = None
        self.user = None
        self.loggin = None
        self.pagina_pendiente = None

        self.barra_menu = tk.Menu(self)
        self.menu_file = tk.Menu(self.barra_menu, tearoff=False)

        self.menu_file.add_command(label="Usuarios",     command=lambda: self.menu_press_user())
        self.menu_file.add_command(label="Clientes",     command=lambda: self.menu_press_cliente())
        self.menu_file.add_command(label="Vehiculos",    command=lambda: self.menu_press_vehiculos())
        self.menu_file.add_command(label="Reparaciones", command=lambda: self.menu_press_reparaciones())
        self.menu_file.add_command(label="Piezas",       command=lambda: self.menu_press_piezas())
        self.menu_file.add_separator()
        self.menu_file.add_command(label="Salir", command=lambda: self.destroy())
        self.barra_menu.add_cascade(menu=self.menu_file, label="File")

        self.menu_sesion = tk.Menu(self.barra_menu, tearoff=False)
        self.actualizar_menu_sesion()
        self.barra_menu.add_cascade(menu=self.menu_sesion, label="Ingreso")

        try:
            self.makeContainer()
            self.main_frame = MainPage(self.container, self)
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())

        self.configure(menu=self.barra_menu)
        self.resizable(width=False, height=False)

    def actualizar_menu_sesion(self):
        self.menu_sesion.delete(0, tk.END)
        if self.user:
            self.menu_sesion.add_command(
                label=f"Usuario: {self.user.getNombre()} | {self.user.getPerfil()}",  # CORREGIDO: agregado separador legible
                state='disabled'
            )
            self.menu_sesion.add_separator()
            self.menu_sesion.add_command(label="Cerrar sesion", command=lambda: self.log_out())
        else:
            self.menu_sesion.add_command(label='No has iniciado sesion', state='disabled')
            self.menu_sesion.add_separator()
            self.menu_sesion.add_command(label="Iniciar sesion", command=lambda: self.requerir_login(None))

    def makeContainer(self):
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

    def limpiar_contenedor(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def requerir_login(self, pagina_destino, perfil_requerido=None):
        if self.user:
            if perfil_requerido and self.user.getPerfil() != perfil_requerido:
                messagebox.showwarning('Acceso denegado', f'Solo {perfil_requerido}')
                return False
            if pagina_destino:
                self.show_page(pagina_destino)
            return True
        else:
            self.pagina_pendiente = {
                'pagina': pagina_destino,
                'perfil': perfil_requerido
            }
            if not logginWindow.en_uso:
                self.loggin = logginWindow(self.handle_login)
            return False

    def show_page(self, nombre_pagina):
        self.limpiar_contenedor()
        paginas = {
            'UserPage':     UserPage,
            'ClientPage':   ClientPage,
            'VehiculoPage': VehiculoPage,
            'PiezaPage':    PiezaPage,
            'Reparaciones' : RepairPage,
            'MainPage':     MainPage
        }
        if nombre_pagina in paginas:
            pagina_class = paginas[nombre_pagina]
            pagina = pagina_class(self.container, self)
            if nombre_pagina == 'UserPage':
                self.pageUser = pagina
            elif nombre_pagina == 'ClientPage':
                self.pageClient = pagina
            elif nombre_pagina == 'VehiculoPage':
                self.pageVehiculo = pagina
            elif nombre_pagina == 'PiezaPage':
                self.pagePieza = pagina
            elif nombre_pagina == 'Reparaciones':
                self.pageReparaciones = pagina

    def handle_login(self, username, password):
        db = DbUsuario()
        exito, user = db.Autentificar(username, password)
        if exito:
            self.user = user
            self.actualizar_menu_sesion()
            if self.pagina_pendiente:
                destino = self.pagina_pendiente['pagina']
                perfil  = self.pagina_pendiente['perfil']
                if perfil and user.getPerfil() != perfil:
                    messagebox.showerror("Acceso denegado", f"Solo {perfil}")
                    self.pagina_pendiente = None
                    self.show_page('MainPage')
                    return exito  # CORREGIDO: logginWindow.login() espera bool, no tupla
                self.show_page(destino)
                self.pagina_pendiente = None
            else:
                self.show_page('MainPage')
        return exito  # CORREGIDO: devuelve solo el bool que logginWindow necesita

    def cerrar_sesion(self):
        self.user = None
        self.pagina_pendiente = None
        self.actualizar_menu_sesion()
        self.show_page('MainPage')
        messagebox.showwarning('Sesion cerrada', 'Has cerrado sesion')

    def menu_press_user(self):
        self.requerir_login('UserPage', perfil_requerido='Administrador')

    def log_out(self):
        self.user = None
        self.limpiar_contenedor()
        self.main_frame = MainPage(self.container, self)
        messagebox.showinfo("Sesion cerrada", 'Has cerrado sesion.')

    def menu_press_cliente(self):
        self.requerir_login('ClientPage')

    def menu_press_vehiculos(self):
        self.requerir_login('VehiculoPage')

    def menu_press_reparaciones(self):
        self.requerir_login('Reparaciones')

    def menu_press_piezas(self):
        self.requerir_login('PiezaPage')