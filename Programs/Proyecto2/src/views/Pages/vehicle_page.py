import sqlite3
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
        self.usuario_actual = controller.user

        if not self.usuario_actual or self.usuario_actual.getPerfil() == 'Mecanico':
            messagebox.showerror("Acceso denegado", "No tienes permisos")
            controller.show_page("MainPage")
            return

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
        self.button_buscar = ttk.Button(self.frameBuscar, text='Buscar', command=lambda:self.buscar_vehiculo())

        #configuracion de datos
        self.label_matricua = ttk.Label(self.frameDatos, text='Matricula')
        self.entry_matricula = ttk.Entry(self.frameDatos)
        self.label_cliente = ttk.Label(self.frameDatos, text='Cliente')
        self.combo_cliente = ttk.Combobox(self.frameDatos)
        self.entry_id_cliente = ttk.Entry(self.frameDatos, state='disabled', width=10)
        self.label_marca = ttk.Label(self.frameDatos, text='Marca')
        self.entry_marca = ttk.Entry(self.frameDatos)
        self.label_modelo = ttk.Label(self.frameDatos, text='Modelo')
        self.entry_modelo = ttk.Entry(self.frameDatos)
        self.get_data_cliente()

        #configuracion de botones
        self.button_new = ttk.Button(self.frameButtons, text='Nuevo', command=lambda:self.new_vehicle())
        self.button_save = ttk.Button(self.frameButtons, text='Salvar', command=lambda:self.salvar_vehiculo())
        self.button_cancel = ttk.Button(self.frameButtons, text='Cancelar', command=lambda:self.cancelar())
        self.button_edit = ttk.Button(self.frameButtons, text='Editar', command=lambda:self.editar_vehiculo())
        self.button_delete = ttk.Button(self.frameButtons, text='Eliminar', command=lambda:self.remove_vehiculo())

        #configuracion de busqueda GRID
        self.label_id_buscar.grid(row=0, column=0)
        self.entry_id_buscar.grid(row=0, column=1)
        self.button_buscar.grid(row=0, column=2)

        #configuracion de datos GRID
        self.label_matricua.grid(row=0, column=0, sticky='e')
        self.entry_matricula.grid(row=0, column=1, sticky='w')
        self.label_cliente.grid(row=1, column=0, sticky='e')
        self.combo_cliente.grid(row=1, column=1, sticky='w')
        self.entry_id_cliente.grid(row=1, column=2, sticky='w')
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

    def aplicar_restriccion_por_rol(self):
        perfil = self.usuario_actual.getPerfil()
        if perfil == "Administrador":
            pass
        elif perfil == "Auxiliar":
            self.button_delete.config(state='disabled')
            self.button_edit.config(state="disabled")
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
        self.entry_id_cliente.config(state=control)
        if self.usuario_actual:
            self.aplicar_restriccion_por_rol()

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
        self.entry_id_cliente.delete(0, 'end')

    def put_data_vehiculo_to_entry(self, nombre_cliente=None):
        self.entry_matricula.insert(0,str(self.vehiculo.getMatricula()))
        self.entry_marca.insert(0,str(self.vehiculo.getMarca()))
        self.entry_modelo.insert(0,str(self.vehiculo.getModelo()))
        self.combo_cliente.set(str(nombre_cliente))
        self.entry_id_cliente.insert(0,str(self.vehiculo.getIdCliente()))

    def get_data_cliente(self):
        db = DbVehiculo()
        try:
            self.combo_cliente['values'] = db.get_name_clintes()
        except Exception as e:
            Logger.add_to_log("erorr", str(e))
            Logger.add_to_log("erorr", traceback.format_exc())

    def buscar_vehiculo(self):
        try:
            try:
                matricula = str(self.entry_id_buscar.get())
            except Exception as e:
                Logger.add_to_log("erorr", str(e))
                Logger.add_to_log("erorr", traceback.format_exc())
                return

            db = DbVehiculo()
            exito, vehiculo = db.search(matricula)
            if exito:
                self.vehiculo = vehiculo
                self.configure_state_to_init('normal')
                self.entry_id_cliente.config(state='normal')
                self.delete_entry()
                self.get_data_cliente()
                self.put_data_vehiculo_to_entry(db.nombre_cliente)
                self.entry_id_cliente.config(state='disabled')
                self.configure_state_to_init('disabled')
                self.button_new.config(state='disabled')
                self.aplicar_restriccion_por_rol()
                self.button_cancel.config(state='normal')
            else:
                messagebox.showerror("erorr", "Vehiculo no encontrado")
                Logger.add_to_log("erorr", "Vehiculo no encontrado")
                self.entry_id_buscar.delete(0, 'end')
                self.entry_id_buscar.focus_force()
        except Exception as e:
            Logger.add_to_log("erorr", str(e))
            Logger.add_to_log("erorr", traceback.format_exc())

    def cancelar(self):
        self.configure_state_to_init('normal')
        self.delete_entry()
        self.entry_id_buscar.delete(0, 'end')
        self.configure_state_to_init('disabled')
        self.button_new.config(state='normal')

    def new_vehicle(self):
        try:
            self.configure_state_to_init('normal')
            self.delete_entry()
            self.entry_id_cliente.config(state='disabled')
            db= DbVehiculo()
            self.button_save.config(state='normal')
            self.button_cancel.config(state='normal')
            self.aplicar_restriccion_por_rol()
        except Exception as e:
            self.configure_state_to_init('normal')
            self.delete_entry()
            self.entry_id_cliente.config(state='disabled')
            Logger.add_to_log("erorr", str(e))
            Logger.add_to_log("erorr", traceback.format_exc())
        except sqlite3.IntegrityError as e:
            Logger.add_to_log("erorr", str(e))
            Logger.add_to_log("erorr", traceback.format_exc())

    def salvar_vehiculo(self):
        try:
            self.configure_state_entry('normal')
            matricula = (int(self.entry_matricula.get()))
            cliente = str(self.entry_id_cliente.get())
            marca = str(self.entry_marca.get())
            modelo = str(self.entry_modelo.get())
            vehiculo = Vehiculo(matricula, cliente, marca, modelo)
            db = DbVehiculo()
            if self.seEditaElVehiculo:
                try:
                    if db.editar(vehiculo):
                        messagebox.showinfo("succes", "Vehiculo editado")
                        Logger.add_to_log("succes", "Vehiculo editado")
                        self.delete_entry()
                        self.entry_id_buscar.delete(0, 'end')
                        self.configure_state_to_init('disabled')
                        self.seEditaElVehiculo = False
                        Logger.add_to_log("succes", "Vehiculo editado:" +str(vehiculo))
                        return
                    else:
                        messagebox.showerror("erorr", "Vehiculo no editado")
                        Logger.add_to_log("erorr", "Vehiculo no editado")
                except Exception as e:
                    self.configure_state_to_init('normal')
                    self.delete_entry()
                    self.configure_state_to_init('disabled')
                    Logger.add_to_log("erorr", "Vehiculo no editado:" +str(e))
                    Logger.add_to_log("erorr", traceback.format_exc())
            else:
                exito = db.save(vehiculo)
                if exito:
                    messagebox.showinfo('succes', 'Vehiculo guardado')
                    Logger.add_to_log("succes", "Vehiculo guardado")
                    self.delete_entry()
                    self.configure_state_to_init('disabled')
                    self.entry_matricula.config(state='disabled')
                else:
                    messagebox.showerror('error', 'Vehiculo no guardado')
                    Logger.add_to_log("error", "Vehiculo no guardado")
                self.aplicar_restriccion_por_rol()
        except Exception as e:
            self.configure_state_to_init('normal')
            self.delete_entry()
            self.configure_state_to_init('disabled')
            Logger.add_to_log("erorr", str(e))
            Logger.add_to_log("erorr", traceback.format_exc())

    def editar_vehiculo(self):
        self.configure_state_to_init('normal')
        self.get_data_cliente()
        self.entry_matricula.config(state='disabled')
        self.combo_cliente.config(state='disabled')
        self.entry_id_cliente.config(state='disabled')
        self.button_new.config(state='disabled')
        self.button_edit.config(state='disabled')
        self.button_delete.config(state='disabled')

    def remove_vehiculo(self):
        try:
            resultado = messagebox.askyesno("remover", "Estas seguro de eliminar este vehiculo?")
            if resultado:
                db = DbVehiculo()
                exito = db.borrar(self.vehiculo)
                if exito:
                    self.configure_state_to_init('normal')
                    self.delete_entry()
                    self.configure_state_to_init('disabled')
                    self.entry_id_buscar.delete(0, 'end')
                    messagebox.showinfo("succes", "Vehiculo eliminado")
                    Logger.add_to_log("succes", "Vehiculo eliminado")
                else:
                    messagebox.showerror("erorr", "Vehiculo no eliminado")
                    messagebox.showinfo("error", "Vehiculo no eliminado")
            else:
                self.aplicar_restriccion_por_rol()
                pass
        except Exception as e:
            self.configure_state_to_init('normal')
            self.delete_entry()
            self.configure_state_to_init('disabled')
            Logger.add_to_log("erorr", str(e))
            Logger.add_to_log("erorr", traceback.format_exc())


