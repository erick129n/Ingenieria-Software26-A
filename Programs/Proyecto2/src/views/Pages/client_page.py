import sqlite3
import tkinter as tk
import traceback
from tkinter import messagebox
from tkinter import ttk

from databases.dbUsuario import DbUsuario
from src.utils.logger import Logger
from src.databases.db_cliente import DBCliente
from src.models.cliente import Cliente
from src.utils.base import Base, ESTADO_REPOSO, ESTADO_RESULTADO, ESTADO_NUEVO, ESTADO_EDITANDO


class ClientPage(Base):
    def __init__(self, master, controller):
        super().__init__(master, controller)
        if not self._verificar_acceso(perfil_denegado='Mecanico'):
            return
        self.cliente = Cliente()

        self.frameBuscarCliente = ttk.Frame(master)
        self.frameDatosCliente  = ttk.Frame(master)
        self.frameBotones       = ttk.Frame(master)
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)
        master.rowconfigure(1, weight=1)
        master.rowconfigure(2, weight=1)
        self.grid(row=0, column=0, pady=5, padx=5, sticky="nsew")
        self.frameBuscarCliente.grid(row=0, column=0, padx=5, pady=5, sticky='ns')
        self.frameDatosCliente.grid(row=1, column=0, padx=5, pady=5, sticky='ns')
        self.frameBotones.grid(row=2, column=0, padx=5, pady=5, sticky='s')

        ###############VARIABLE QUE VALIDA SI HAY DATOS EN LA BARRA DE BUSQUEDA ###############################
        vcmd = (self.register(self.activa_boton_busqueda_key), '%P')

        ############ frame de busqueda
        self.label_nombre_buscar = ttk.Label(self.frameBuscarCliente, text="Nombre del cliente:")
        self.entry_nombre_buscar = ttk.Entry(self.frameBuscarCliente, validate='key', width=35, validatecommand=vcmd)
        self.buttonBuscar = ttk.Button(self.frameBuscarCliente, text='Buscar', command=lambda:self.buscarCliente())

        self.label_nombre_buscar.grid(row=0, column=0)
        self.entry_nombre_buscar.grid(row=0, column=1)
        self.buttonBuscar.grid(row=0, column=2)

        ########### frame de datos
        self.label_id_cliente = ttk.Label(self.frameDatosCliente, text="ID")
        self.entry_id_cliente = ttk.Entry(self.frameDatosCliente, width=15)
        self.label_nombre_cliente = ttk.Label(self.frameDatosCliente, text="Nombre")
        self.entry_nombre_cliente = ttk.Entry(self.frameDatosCliente, width=35)
        self.label_telefono_cliente = ttk.Label(self.frameDatosCliente, text="Telefono")
        self.entry_telefono_cliente = ttk.Entry(self.frameDatosCliente, width=15)
        self.label_email_cliente = ttk.Label(self.frameDatosCliente, text="Email")
        self.entry_email_cliente = ttk.Entry(self.frameDatosCliente, width=35)
        self.label_rfc_cliente = ttk.Label(self.frameDatosCliente, text="RFC")
        self.entry_rfc_cliente = ttk.Entry(self.frameDatosCliente, width=35)
        self.label_userId_cliente = ttk.Label(self.frameDatosCliente, text='Usuario ID')
        self.combo_userID_cliente = ttk.Combobox(self.frameDatosCliente, width=15)
        self.get_data_cliente()

        self.label_id_cliente.grid(row=0, column=0, sticky="e")
        self.entry_id_cliente.grid(row=0, column=1, sticky="w")
        self.label_nombre_cliente.grid(row=1, column=0, sticky="e")
        self.entry_nombre_cliente.grid(row=1, column=1, sticky="w")
        self.label_telefono_cliente.grid(row=2, column=0, sticky="e")
        self.entry_telefono_cliente.grid(row=2, column=1, sticky="w")
        self.label_email_cliente.grid(row=3, column=0, sticky="e")
        self.entry_email_cliente.grid(row=3, column=1, sticky="w")
        self.label_rfc_cliente.grid(row=4, column=0, sticky="e")
        self.entry_rfc_cliente.grid(row=4, column=1, sticky="w")
        self.label_userId_cliente.grid(row=5, column=0, sticky="e")
        self.combo_userID_cliente.grid(row=5, column=1, sticky="w")


        ########## Botones de cliente
        self.buttonNew = ttk.Button(self.frameBotones, text='Nuevo', command=lambda:self.newClient())
        self.buttonSave = ttk.Button(self.frameBotones, text='Salvar', command=lambda:self.salvarCliente())
        self.buttonCancel = ttk.Button(self.frameBotones, text='Cancelar', command=lambda:self.cancelar())
        self.buttonEdit = ttk.Button(self.frameBotones, text='Editar', command=lambda:self.editarCliente())
        self.buttonDelete = ttk.Button(self.frameBotones, text='Remover', command=lambda:self.removerCliente())

        self.buttonNew.grid(row=0, column=0)
        self.buttonSave.grid(row=0, column=1)
        self.buttonCancel.grid(row=0, column=2)
        self.buttonEdit.grid(row=0, column=3)
        self.buttonDelete.grid(row=0, column=4)

        for widget in self.frameBuscarCliente.winfo_children():
            widget.grid_configure(padx=5, pady=5)
        for widget in self.frameDatosCliente.winfo_children():
            widget.grid_configure(padx=5, pady=5)
        for widget in self.frameBotones.winfo_children():
            widget.grid_configure(padx=5, pady=50)

        self._registrar_widget(
            btn_buscar=self.buttonBuscar,
            entry_buscar=self.entry_nombre_buscar,
            btn_new=self.buttonNew,
            btn_save=self.buttonSave,
            btn_cancel=self.buttonCancel,
            btn_edit=self.buttonEdit,
            btn_delete=self.buttonDelete,
            campos_readonly= [self.entry_id_cliente],
        )
        self._aplicar_estado(ESTADO_REPOSO)

    def activa_boton_busqueda_key(self, content):
        if all(content.isalpha() or c.isspace() for c in content):
            self.buttonBuscar.config(state=tk.NORMAL)
        else:
            self.buttonBuscar.config(state=tk.DISABLED)
        return True


    def get_data_cliente(self):
        db = DbUsuario()
        try:
            self.combo_userID_cliente['values'] = db.getIdsUsers()
        except ValueError as e:
            Logger.add_to_log("erorr", str(e))
            Logger.add_to_log("erorr", traceback.format_exc())

    def _limpiar_campos(self):
        self._limpiar_todos(
            self.entry_nombre_buscar,
            self.entry_id_cliente,
            self.entry_nombre_cliente,
            self.entry_telefono_cliente,
            self.entry_email_cliente,
            self.entry_rfc_cliente,
        )
        self.combo_userID_cliente.set('')

    def _poblar_campos(self, cliente: Cliente):
        for entry, valor in (
                (self.entry_id_cliente, cliente.getIdCliente()),
                (self.entry_nombre_cliente, cliente.getNombre()),
                (self.entry_telefono_cliente, cliente.getTelefono()),
                (self.entry_email_cliente, cliente.getEmail()),
                (self.entry_rfc_cliente, cliente.getRfc()),
        ):
            entry.config(state='normal')
            entry.insert(tk.END, str(valor))
        self.combo_userID_cliente.set(str(cliente.getUserId()))


    def buscarCliente(self):
        try:
            try:
                nombre = self.entry_nombre_buscar.get().strip()
            except ValueError as e:
                Logger.add_to_log("erorr", str(e))
                Logger.add_to_log("erorr", traceback.format_exc())
                return

            db = DBCliente()
            exito, cliente = db.search(nombre)
            if exito:
                self.cliente = cliente
                self.get_data_cliente()
                self._poblar_campos(self.cliente)
                self._aplicar_estado(ESTADO_RESULTADO)
            else:
                messagebox.showerror("erorr", "Cliente no existe")
                Logger.add_to_log("erorr", 'Cliente no existe')
                Logger.add_to_log("error", traceback.format_exc())
                self.entry_nombre_buscar.delete(0, tk.END)
                self.entry_nombre_buscar.focus()

        except Exception as e:
            Logger.add_to_log("erorr", str(e))
            Logger.add_to_log("erorr", traceback.format_exc())
            self._aplicar_estado(ESTADO_REPOSO)

    def cancelar(self):
        self._limpiar_campos()
        self._aplicar_estado(ESTADO_REPOSO)

    def newClient(self):
        try:
            self._limpiar_campos()
            self.get_data_cliente()
            db= DBCliente()
            auxId = db.getMaxId()
            self.entry_id_cliente.config(state=tk.NORMAL)
            self.entry_id_cliente.insert(tk.END, str(auxId))
            self.entry_id_cliente.config(state=tk.DISABLED)
            self._aplicar_estado(ESTADO_NUEVO)
        except Exception as e:
            Logger.add_to_log("erorr", str(e))
            Logger.add_to_log("erorr", traceback.format_exc())
            self._aplicar_estado(ESTADO_REPOSO)
        except sqlite3.IntegrityError as e:
            Logger.add_to_log("erorr", str(e))
            Logger.add_to_log("erorr", traceback.format_exc())

    def salvarCliente(self):
        try:
            self.entry_id_cliente.config(state=tk.NORMAL)
            id_cliente = int(self.entry_id_cliente.get().strip())
            self.entry_id_cliente.config(state=tk.DISABLED)
            nombre = self.entry_nombre_cliente.get().strip()
            telefono = self.entry_telefono_cliente.get().strip()
            email = self.entry_email_cliente.get().strip()
            rfc = self.entry_rfc_cliente.get().strip()
            idUser = int(self.combo_userID_cliente.get().strip())

            if not id_cliente:
                messagebox.showerror('error', 'Campo id cliente faltante'); return
            if not nombre:
                messagebox.showerror('error', 'Campo nombre faltante'); return
            if not telefono:
                messagebox.showerror('error', 'Campo telefono faltante'); return
            if not email:
                messagebox.showerror('error', 'Campo email faltante'); return
            if not rfc:
                messagebox.showerror('error', 'Campo rfc'); return
            if not idUser:
                messagebox.showerror('error', 'Campo idUser'); return

            client = Cliente(id_cliente, nombre, telefono, email, rfc, idUser)
            db = DBCliente()
            if self.estado_actual == ESTADO_EDITANDO:
                try:
                    if db.editar(client):
                        messagebox.showinfo('Exito', 'Cliente actualizado')
                        self._limpiar_campos()
                        self._aplicar_estado(ESTADO_REPOSO)
                        Logger.add_to_log("info", 'Cliente editado:'+str(client.getNombre()))
                    else:
                        messagebox.showerror('error', 'Cliente no editado')
                        Logger.add_to_log('error', 'Cliente no editado')

                except Exception as e:
                    Logger.add_to_log('error', str(e))
                    Logger.add_to_log('error', traceback.format_exc())
            else:
                exito = db.save(client)
                if exito:
                    messagebox.showinfo('success', 'Cliente guardado')
                    Logger.add_to_log('succes', 'Cliente guardado')
                    self._limpiar_campos()
                    self._aplicar_estado(ESTADO_REPOSO)
                else:
                    messagebox.showerror('error', 'Cliente no guardado')
                    Logger.add_to_log('error', 'Cliente no guardado')
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
            self._aplicar_estado(ESTADO_REPOSO)

    def editarCliente(self):
        try:
            self.get_data_cliente()
            self._aplicar_estado(ESTADO_EDITANDO)
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
            self._aplicar_estado(ESTADO_REPOSO)


    def removerCliente(self):
        try:
            resultado = messagebox.askyesno('Remover', 'Estas seguro de remover el cliente?')
            if resultado:
                db = DBCliente()
                exito = db.borrar(self.cliente)
                if exito:
                    messagebox.showinfo('succes', 'Cliente removido')
                    Logger.add_to_log('succes', 'Cliente removido')
                    self._limpiar_campos()
                    self._aplicar_estado(ESTADO_REPOSO)
                else:
                    messagebox.showerror('error', 'Cliente no borrado')
                    Logger.add_to_log('error', traceback.format_exc())
                    self._aplicar_estado(ESTADO_RESULTADO)
            else:
                return
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
            self._aplicar_estado(ESTADO_REPOSO)