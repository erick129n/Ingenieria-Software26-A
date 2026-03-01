import tkinter as tk
import traceback
from tkinter import ttk
from tkinter import messagebox
from src.models.usuario import User
from src.databases.dbUsuario import DbUsuario

from src.utils.logger import Logger
class logginWindow(tk.Toplevel):
    en_uso = False
    user = User
    def __init__(self):
        super().__init__()


        self.title("Iniciar sesion")
        self.resizable(width=False, height=False)
        self.geometry("250x100")
        self.label_userName = ttk.Label(self, text="Username:")
        self.label_password = ttk.Label(self, text="Password:")
        self.entry_username = ttk.Entry(self)
        self.entry_password = ttk.Entry(self, show="*")

        self.button_login = ttk.Button(self, text='login', command=lambda:self.login())
        self.label_userName.grid(row=0, column=0, sticky=tk.EW, padx=5, pady=5)
        self.label_password.grid(row=1, column=0, sticky=tk.EW, padx=5, pady=5)
        self.entry_username.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        self.entry_password.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)

        self.button_login.grid(row=3, column=1, sticky=tk.E, padx=5, pady=5)
        self.focus_force()
        self.entry_username.focus_force()

        self.__class__.en_uso = True

    def login(self):
        try:
            username = str(self.entry_username.get())
            password = str(self.entry_password.get())
            db = DbUsuario()
            print('se realizara la operacion')
            exito, usuario = db.Autentificar(username, password)
            print('la operacion se hizo')
            if exito:
                self.user = usuario
                print('Usuario creado')
                self.destroy()
                return True

            else:
                messagebox.showerror("Error", "Usuario no encontrado")
                return False
        except Exception as e:
            Logger.add_to_log('error',str(e))
            Logger.add_to_log('error',traceback.format_exc())
            return False

    def destroy(self):
        self.__class__.en_uso = False
        return super().destroy()