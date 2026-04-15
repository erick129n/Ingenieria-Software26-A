import sqlite3
import traceback
from tkinter import messagebox
from tkinter import ttk
from src.models.vehiculo import Vehiculo
from src.databases.db_vehiculo import DbVehiculo
from src.databases.db_cliente import DBCliente
from utils.logger import Logger
from src.utils.base import Base, ESTADO_REPOSO, ESTADO_RESULTADO, ESTADO_NUEVO, ESTADO_EDITANDO

class VehiculoPage(Base):
    def __init__(self, master, controller):
        super().__init__(master, controller)

        if not self._verificar_acceso(perfil_denegado='Mecanico'):
            return
        self.vehiculo = Vehiculo()
        self.frameBuscar  = ttk.Frame(master)
        self.frameDatos   = ttk.Frame(master)
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
        self.combo_cliente.bind("<<ComboboxSelected>>", self.on_cliente_seleccionado)
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

        self._registrar_widget(
            btn_buscar=self.button_buscar,
            entry_buscar=self.entry_id_buscar,
            btn_new=self.button_new,
            btn_save=self.button_save,
            btn_cancel=self.button_cancel,
            btn_edit=self.button_edit,
            btn_delete=self.button_delete,
            campos=[self.entry_marca, self.entry_modelo],
            campos_solo_nuevo=[self.entry_matricula, self.combo_cliente],
            campos_readonly=[self.entry_id_cliente],
        )
        self._aplicar_estado(ESTADO_REPOSO)


    def activa_boton_busqueda_key(self, content):
        if content.isalnum():
            self.button_buscar.config(state='normal')
        else:
            self.button_buscar.config(state='disabled')
        return content.isalnum() or content == ''

    def get_data_cliente(self):
        db = DbVehiculo()
        try:
            self.combo_cliente['values'] = db.get_name_clintes()
        except Exception as e:
            Logger.add_to_log("erorr", str(e))
            Logger.add_to_log("erorr", traceback.format_exc())
    def _limpiar_campos(self):
        self._limpiar_todos(
            self.entry_id_buscar, self.entry_matricula,
            self.entry_marca, self.entry_modelo, self.entry_id_cliente
        )
        self.combo_cliente.set('')

    def _poblar_campos(self, nombre_cliente):
        for entry, valor in(
            (self.entry_matricula, self.vehiculo.getMatricula()),
            (self.entry_marca, self.vehiculo.getMarca()),
            (self.entry_modelo, self.vehiculo.getModelo()),
        ):
            entry.config(state='normal')
            entry.insert(0, str(valor))
        self.combo_cliente.set(nombre_cliente)
        self.entry_id_cliente.config(state='normal')
        self.entry_id_cliente.insert(0, str(self.vehiculo.getIdCliente()))
        self.entry_id_cliente.config(state='disabled')

    def _leer_id_cliente(self):
        self.entry_id_cliente.delete(0, 'end')
        id_cliente = self.entry_id_cliente.get().strip()
        self.entry_id_cliente.config(state='disabled')
        return int(id_cliente) if id_cliente else None

    def on_cliente_seleccionado(self, event):
        nombre = self.combo_cliente.get()
        try:
            dbcli = DBCliente()
            exito, cliente = dbcli.search(nombre)
            if exito:
                self.entry_id_cliente.config(state='normal')
                self.entry_id_cliente.delete(0, 'end')
                self.entry_id_cliente.insert(0, str(cliente.getIdCliente()))
                self.entry_id_cliente.config(state='disabled')
            else:
                Logger.add_to_log("erorr", f"Cliente no encontrado: {nombre}")
        except Exception as e:
            Logger.add_to_log("erorr", str(e))
            Logger.add_to_log("erorr", traceback.format_exc())



    def buscar_vehiculo(self):
        try:
            try:
                matricula = str(self.entry_id_buscar.get().strip())
            except Exception as e:
                Logger.add_to_log("erorr", str(e))
                Logger.add_to_log("erorr", traceback.format_exc())
                return

            db = DbVehiculo()
            exito, vehiculo = db.search(matricula)
            if exito:
                self.vehiculo = vehiculo
                self._limpiar_campos()
                self.get_data_cliente()
                self._poblar_campos(db.nombre_cliente)
                self._aplicar_estado(ESTADO_RESULTADO)
            else:
                messagebox.showerror("erorr", "Vehiculo no encontrado")
                Logger.add_to_log("erorr", "Vehiculo no encontrado")
                self.entry_id_buscar.delete(0, 'end')
                self.entry_id_buscar.focus_force()
        except Exception as e:
            Logger.add_to_log("erorr", str(e))
            Logger.add_to_log("erorr", traceback.format_exc())
            self._aplicar_estado(ESTADO_REPOSO)

    def cancelar(self):
        self._limpiar_campos()
        self._aplicar_estado(ESTADO_REPOSO)

    def new_vehicle(self):
        try:
            self._limpiar_campos()
            self.get_data_cliente()
            self._aplicar_estado(ESTADO_NUEVO)
        except Exception as e:
            Logger.add_to_log("erorr", str(e))
            Logger.add_to_log("erorr", traceback.format_exc())
            self._aplicar_estado(ESTADO_REPOSO)
        except sqlite3.IntegrityError as e:
            Logger.add_to_log("erorr", str(e))
            Logger.add_to_log("erorr", traceback.format_exc())

    def salvar_vehiculo(self):
        try:
            matricula = str(self.entry_matricula.get().strip())
            marca = str(self.entry_marca.get().strip())
            modelo = str(self.entry_modelo.get().strip())
            id_cliente = int(self._leer_id_cliente())
            if not matricula:
                messagebox.showerror("erorr", "Campo matricula faltante"); return
            if not marca:
                messagebox.showerror('error', 'Campo marca faltante'); return
            if not modelo:
                messagebox.showerror('error', 'Campo modelo faltante'); return
            if not id_cliente:
                messagebox.showerror('error', 'Campo id_cliente faltante'); return
            vehiculo = Vehiculo(matricula, id_cliente, marca, modelo)
            db = DbVehiculo()
            if self.estado_actual == ESTADO_EDITANDO:
                if db.editar(vehiculo):
                    messagebox.showinfo("succes", "Vehiculo editado")
                    Logger.add_to_log("info", "Vehiculo editado:" + str(self.vehiculo))
                    self._limpiar_campos()
                    self._aplicar_estado(ESTADO_REPOSO)
                else:
                    messagebox.showerror("erorr", "Vehiculo no editado")
                    Logger.add_to_log("erorr", "Vehiculo no editado")
            else:
                exito = db.save(self.vehiculo)
                if exito:
                    messagebox.showinfo('succes', 'Vehiculo guardado')
                    Logger.add_to_log("succes", "Vehiculo guardado")
                    self._limpiar_campos()
                    self._aplicar_estado(ESTADO_REPOSO)
                else:
                    messagebox.showerror('error', 'Vehiculo no guardado')
                    Logger.add_to_log("error", "Vehiculo no guardado")
        except Exception as e:
            Logger.add_to_log("erorr", str(e))
            Logger.add_to_log("erorr", traceback.format_exc())
            self._aplicar_estado(ESTADO_REPOSO)

    def editar_vehiculo(self):
        try:
            self.get_data_cliente()
            self._aplicar_estado(ESTADO_EDITANDO)
        except Exception as e:
            Logger.add_to_log("erorr", str(e))
            Logger.add_to_log("erorr", traceback.format_exc())
            self._aplicar_estado(ESTADO_REPOSO)

    def remove_vehiculo(self):
        try:
            resultado = messagebox.askyesno("remover", "Estas seguro de eliminar este vehiculo?")
            if resultado:
                db = DbVehiculo()
                exito = db.borrar(self.vehiculo)
                if exito:
                    messagebox.showinfo("succes", "Vehiculo eliminado")
                    Logger.add_to_log("succes", "Vehiculo eliminado")
                    self._limpiar_campos()
                    self._aplicar_estado(ESTADO_REPOSO)
                else:
                    messagebox.showerror("erorr", "Vehiculo no eliminado")
                    self._aplicar_estado(ESTADO_RESULTADO)
            else:
                return
        except Exception as e:
            Logger.add_to_log("erorr", str(e))
            Logger.add_to_log("erorr", traceback.format_exc())
            self._aplicar_estado(ESTADO_REPOSO)