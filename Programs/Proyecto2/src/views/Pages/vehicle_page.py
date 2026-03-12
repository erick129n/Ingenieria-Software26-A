import tkinter as tk
import traceback
from tkinter import messagebox
from tkinter import ttk
from src.models.vehiculo import Vehiculo
from src.models.cliente import Cliente
from src.databases.db_vehiculo import DbVehiculo
from utils.logger import Logger


class VehiculoPage(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.vehiculo = Vehiculo()
        self.cliente = Cliente()
        self.lista_nombres = []
        self.seEditaElVehiculo =None
        self.frameBuscar = ttk.Frame(master)
        self.frameDatos = ttk.Frame(master)
        self.frameButtons = ttk.Frame(master)


        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)
        master.rowconfigure(1, weight=1)
        master.rowconfigure(2, weight=1)
        master.rowconfigure(3, weight=1)
        self.frameBuscar.grid(row=0, column=0, rowspan=5, columnspan=5, sticky='ns')
        self.frameDatos.grid(row=1, column=0, rowspan=5, columnspan=5, sticky='ns')
        self.frameButtons.grid(row=2, column=0, columnspan=5, sticky='s')


        vcmd = (self.register(self.activa_boton_busqueda_key), '%P')
        #configuracion de busqueda
        self.label_id_buscar = ttk.Label(self.frameBuscar, text="Ingresa la matricula del vehiculo")
        self.entry_id_buscar = ttk.Entry(self.frameBuscar, validate='key', validatecommand=vcmd)
        self.button_buscar = ttk.Button(self.frameBuscar, text='Buscar')

        #configuracion de datos
        self.label_matricua = ttk.Label(self.frameDatos, text='Marticula')
        self.entry_matricula = ttk.Entry(self.frameDatos)
        self.label_cliente = ttk.Label(self.frameDatos, text='Cliente')
        self.combo_cliente = ttk.Combobox(self.frameDatos, postcommand=lambda:self.get_data_cliente())
        self.label_marca = ttk.Label(self.frameDatos, text='Marca')
        self.entry_marca = ttk.Entry(self.frameDatos)
        self.label_modelo = ttk.Label(self.frameDatos, text='Modelo')
        self.entry_modelo = ttk.Entry(self.frameDatos)

        #configuracion de botones
        self.button_new = ttk.Button(self.frameButtons, text='Nuevo')
        self.button_save = ttk.Button(self.frameButtons, text='Salvar')
        self.button_cancel = ttk.Button(self.frameButtons, text='Cancelar')
        self.button_edit = ttk.Button(self.frameButtons, text='Editar')
        self.button_delete = ttk.Button(self.frameButtons, text='Eliminar')

        #configuracion de busqueda GRID
        self.label_id_buscar.grid(row=0, column=0)
        self.entry_id_buscar.grid(row=0, column=1)
        self.button_buscar.grid(row=0, column=2)

        #configuracion de datos GRID
        self.label_matricua.grid(row=0, column=0, sticky='e')
        self.entry_matricula.grid(row=0, column=1, sticky='w')
        self.label_cliente.grid(row=1, column=0, sticky='e')
        self.combo_cliente.grid(row=1, column=1, sticky='w')
        self.label_marca.grid(row=2, column=0, sticky='e')
        self.entry_marca.grid(row=2, column=1, sticky='w')
        self.label_modelo.grid(row=3, column=0, sticky='e')
        self.entry_modelo.grid(row=3, column=1, sticky='w')

        #configuracion de botones GRID
        self.button_new.grid(row=0, column=0)
        self.button_save.grid(row=0, column=1)
        self.button_cancel.grid(row=0, column=2)
        self.button_edit.grid(row=0, column=3)
        self.button_delete.grid(row=0, column=4)

        self.grid(row=0, column=0, sticky="nsew")
        for widget in self.frameBuscar.winfo_children():
            widget.grid(pady=5, padx=5)
        for widget in self.frameDatos.winfo_children():
            widget.grid(pady=5, padx=5)
        for widget in self.frameButtons.winfo_children():
            widget.grid(pady=50, padx=5)

        self.configure_state_to_init('disabled')

    def activa_boton_busqueda_key(self, content):
        if content.isalnum():
            self.button_buscar.config(state='normal')
        else:
            self.button_buscar.config(state='disabled')
        return content.isalnum() or content == ''

    def configure_state_to_init(self, control):
        self.button_buscar.config(state= control)
        self.entry_matricula.config(state=control)
        self.combo_cliente.config(state=control)
        self.entry_marca.config(state=control)
        self.entry_modelo.config(state=control)
        self.button_delete.config(state=control)
        self.button_edit.config(state=control)
        self.button_save.config(state=control)
        self.button_cancel.config(state=control)

    def configure_state_entry(self, control):
        self.entry_matricula.config(state=control)
        self.combo_cliente.config(state=control)
        self.entry_marca.config(state=control)
        self.entry_modelo.config(state=control)

    def delete_entry(self):
        self.entry_id_buscar.delete(0, 'end')
        self.entry_matricula.delete(0, 'end')
        self.combo_cliente.delete(0, 'end')
        self.entry_marca.delete(0, 'end')
        self.entry_modelo.delete(0, 'end')
        self.combo_cliente.delete(0, 'end')

    def put_data_vehiculo_to_entry(self):
        self.entry_matricula.insert(0,str(self.vehiculo.getMatricula()))
        self.entry_marca.insert(0,str(self.vehiculo.getMarca()))
        self.entry_modelo.insert(0,str(self.vehiculo.getModelo()))
        self.combo_cliente.insert(0, str(self.cliente.getNombre()))

    def get_data_cliente(self):
        db = DbVehiculo()
        try:
            self.combo_cliente['values'] = db.lista
        except Exception as e:
            Logger.add_to_log("erorr", str(e))
            Logger.add_to_log("erorr", traceback.format_exc())
        finally:
            db.close()

    def buscar_vehiculo(self):
        try:
            try:
                matricula = str(self.entry_matricula.get())
            except Exception as e:
                Logger.add_to_log("erorr", str(e))
                Logger.add_to_log("erorr", traceback.format_exc())

            db = DbVehiculo()
        except Exception as e:
            Logger.add_to_log("erorr", str(e))
            Logger.add_to_log("erorr", traceback.format_exc())