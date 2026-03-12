import tkinter as tk
import traceback
from tkinter import messagebox
from tkinter.messagebox import showwarning

from databases.dbUsuario import DbUsuario
from src.utils.logger import Logger
from src.views.loggin_window import logginWindow
from src.views.Pages.user_page import UserPage
from src.views.Pages.client_page import ClientPage
from src.views.Pages.vehicle_page import VehiculoPage
from src.views.Pages.main_page import MainPage

class MainWindow(tk.Tk):

    cliente = None
    vehiculo = None
    reparaciones = None
    piezas = None
    def __init__(self):
        super().__init__()
        self.title("Main Window")
        self.geometry("700x400")
        self.container =None
        self.pageUser = None
        self.pageClient = None
        self.pageVehiculo = None
        self.label_principal = None
        self.user = None
        self.loggin=None

        #configuracion de la barra de menu
        self.barra_menu = tk.Menu(self)
        self.menu_file = tk.Menu(self.barra_menu, tearoff=False) #usuarios
        #agregando usuarios
        self.menu_file.add_command(
            label="Usuarios",
            command=lambda:self.menu_press_user()
        )

        self.menu_file.add_command(
            label="Clientes",
            command=lambda:self.menu_press_cliente()
        )
        self.menu_file.add_command(
            label="Vehiculos",
            command=lambda:self.menu_press_vehiculos()
        )
        self.menu_file.add_command(
            label="Reparaciones",
            command=lambda:self.menu_press_reparaciones()
        )
        self.menu_file.add_command(
            label="Piezas",
            command=lambda:self.menu_press_piezas()
        )

        self.menu_file.add_separator()
        # ultimo boton del menu
        self.menu_file.add_command(label="Salir", command=lambda: self.destroy())
        self.barra_menu.add_cascade(menu=self.menu_file, label="File")

        try:
            self.makeContainer()
            self.main_frame = MainPage(self.container,self)
        except Exception as e:
            Logger.add_to_log("Error:", str(e))
            Logger.add_to_log("Exception Log:", traceback.format_exc())


        self.configure(menu=self.barra_menu)
        self.resizable(width=False, height=False)

    def makeContainer(self):
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

    def limpiar_contenedor(self):
        for widget in self.container.winfo_children():
            widget.destroy()
    def menu_press_user(self):
        self.limpiar_contenedor()
        self.pageUser = UserPage(self.container,self)

    def handle_login(self, username, password):
        db = DbUsuario()
        exito, user = db.Autentificar(username, password)
        if exito:
            self.user = user
            self.limpiar_contenedor()
            self.pageClient = ClientPage(self.container,self)
        return exito

    def menu_press_cliente(self):
        self.loggin = logginWindow(self.handle_login)

    def menu_press_vehiculos(self):
        self.limpiar_contenedor()
        self.pageVehiculo = VehiculoPage(self.container,self)
    def menu_press_reparaciones(self):
        messagebox.showwarning("ADVERTENCIA", "Funcion no implementada")
    def menu_press_piezas(self):
        messagebox.showwarning("ADVERTENCIA", "Funcion no implementada")