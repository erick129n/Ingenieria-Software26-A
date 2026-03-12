import sqlite3
import tkinter as tk
import traceback
from tkinter import messagebox
from tkinter import ttk

from databases.dbUsuario import DbUsuario
from src.utils.logger import Logger
from src.databases.db_cliente import DBCliente
from src.models.cliente import Cliente
from src.models.cliente import User


class ClientPage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller
        self.usuario_actual = controller.user

        if self.usuario_actual or self.usuario_actual.getPerfil() == 'Mecanico':
            messagebox.showerror("Accesso denegado", "No tienes permisos")
            controller.show_page('MainPage')
            return
        self.cliente = Cliente()
        self.usuario = User() # verificar si se usa
        self.seEditaElCliente = False
        self.frameBuscarCliente = ttk.Frame(master)
        self.frameDatosCliente = ttk.Frame(master)
        self.frameBotones = ttk.Frame(master)
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
        self.combo_userID_cliente = ttk.Combobox(self.frameDatosCliente, width=15, postcommand=lambda:self.get_data_cliente())

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



        """DESABILITAN LAS OPCIONES AL ENTRAR"""
        self.configure_state_to_init("disabled")

    def aplicar_restricciones_por_rol(self):
        perfil = self.usuario_actual.getPerfil()
        if perfil == "Administrador":
            pass
        elif perfil == "Auxiliar":
            self.buttonDelete.config(state=tk.DISABLED)
            self.buttonEdit.config(state=tk.DISABLED)
    def activa_boton_busqueda_key(self, content):
        if all(content.isalpha() or c.isspace() for c in content):
            self.buttonBuscar.config(state=tk.NORMAL)
        else:
            self.buttonBuscar.config(state=tk.DISABLED)
        return True

    def configure_state_to_init(self, control):
        self.buttonBuscar.config(state= control)
        self.entry_id_cliente.config(state=control)
        self.entry_nombre_cliente.config(state=control)
        self.entry_telefono_cliente.config(state=control)
        self.entry_email_cliente.config(state=control)
        self.entry_rfc_cliente.config(state=control)
        self.combo_userID_cliente.config(state=control)
        self.buttonSave.config(state=control)
        self.buttonCancel.config(state=control)
        self.buttonEdit.config(state=control)
        self.buttonDelete.config(state=control)


    def configure_state_entry(self, control):
        self.entry_id_cliente.config(state=control)
        self.entry_nombre_cliente.config(state=control)
        self.entry_telefono_cliente.config(state=control)
        self.entry_email_cliente.config(state=control)
        self.entry_rfc_cliente.config(state=control)
        self.combo_userID_cliente.config(state=control)

    def delete_entry(self):
        self.entry_id_cliente.delete(0, tk.END)
        self.entry_nombre_cliente.delete(0, tk.END)
        self.entry_telefono_cliente.delete(0, tk.END)
        self.entry_email_cliente.delete(0, tk.END)
        self.entry_rfc_cliente.delete(0, tk.END)
        self.combo_userID_cliente.delete(0, tk.END)

    def put_data_cliente_to_entry(self, cliente):
        self.entry_id_cliente.insert(tk.END, str(cliente.getIdCliente()))
        self.entry_nombre_cliente.insert(tk.END, str(cliente.getNombre()))
        self.entry_telefono_cliente.insert(tk.END, str(cliente.getTelefono()))
        self.entry_email_cliente.insert(tk.END, str(cliente.getEmail()))
        self.entry_rfc_cliente.insert(tk.END, str(cliente.getRfc()))
        self.combo_userID_cliente.set(str(cliente.getUserID()))

    def get_data_cliente(self):
        db = DbUsuario()
        try:
            self.combo_userID_cliente['values'] = db.getIdsUsers()
        except ValueError as e:
            Logger.add_to_log("erorr", str(e))
            Logger.add_to_log("erorr", traceback.format_exc())

    def buscarCliente(self):
        try:
            try:
                nombre = self.entry_nombre_buscar.get()
            except ValueError as e:
                Logger.add_to_log("erorr", str(e))
                Logger.add_to_log("erorr", traceback.format_exc())
                return

            db = DBCliente()
            exito, cliente = db.search(nombre)
            if exito:
                self.cliente = cliente
                self.configure_state_to_init('normal')
                self.put_data_cliente_to_entry(self.cliente)
                self.configure_state_to_init('disabled')
                self.buttonNew.config(state=tk.DISABLED)
                self.buttonEdit.configure(state=tk.NORMAL)
                self.buttonDelete.configure(state=tk.NORMAL)
                self.buttonCancel.configure(state=tk.NORMAL)
            else:
                messagebox.showerror("erorr", "Cliente no existe")
                Logger.add_to_log("erorr", 'Cliente no existe')
                Logger.add_to_log("error", traceback.format_exc())
                self.entry_nombre_buscar.delete(0, tk.END)
                self.entry_nombre_buscar.focus()

        except Exception as e:
            Logger.add_to_log("erorr", str(e))
            Logger.add_to_log("erorr", traceback.format_exc())

    def cancelar(self):
        self.configure_state_to_init('normal')
        self.delete_entry()
        self.configure_state_to_init('disabled')
        self.buttonNew.config(state=tk.NORMAL)

    def newClient(self):
        try:
            self.configure_state_entry('normal')
            self.delete_entry()
            db= DBCliente()
            auxId = db.getMaxId()
            self.entry_id_cliente.insert(tk.END, str(auxId))
            self.entry_id_cliente.config(state=tk.DISABLED)
            self.buttonSave.config(state=tk.NORMAL)
            self.buttonCancel.config(state=tk.NORMAL)
        except Exception as e:
            Logger.add_to_log("erorr", str(e))
            Logger.add_to_log("erorr", traceback.format_exc())
        except sqlite3.IntegrityError as e:
            Logger.add_to_log("erorr", str(e))
            Logger.add_to_log("erorr", traceback.format_exc())

    def salvarCliente(self):
        try:
            self.configure_state_entry('normal')
            id_cliente = int(self.entry_id_cliente.get())
            nombre = self.entry_nombre_cliente.get()
            telefono = self.entry_telefono_cliente.get()
            email = self.entry_email_cliente.get()
            rfc = self.entry_rfc_cliente.get()
            idUser = int(self.combo_userID_cliente.get())
            print(idUser)
            client = Cliente(id_cliente, nombre, telefono, email, rfc, idUser)
            db = DBCliente()
            if self.seEditaElCliente:
                try:
                    if db.editar(client):
                        messagebox.showinfo('Exito', 'Cliente actualizado')
                        Logger.add_to_log('succes', 'Cliente actualizado')
                        self.delete_entry()
                        self.entry_nombre_buscar.delete(0, 'end')
                        self.configure_state_to_init('disabled')
                        self.seEditaElCliente = False
                        Logger.add_to_log("info", 'Cliente editado:'+str(client.getNombre()))
                        return
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
                    self.delete_entry()
                    self.configure_state_to_init('disabled')
                    self.entry_id_cliente.config(state=tk.DISABLED)
                else:
                    messagebox.showerror('error', 'Cliente no guardado')
                    Logger.add_to_log('error', 'Cliente no guardado')
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())

    def editarCliente(self):
        self.configure_state_to_init('normal')
        self.entry_id_cliente.config(state=tk.DISABLED)
        self.combo_userID_cliente.config(state=tk.DISABLED)
        self.buttonNew.config(state=tk.DISABLED)
        self.buttonEdit.config(state=tk.DISABLED)
        self.buttonDelete.config(state=tk.DISABLED)


    def removerCliente(self):
        try:
            resultado = messagebox.askyesno('Remover', 'Estas seguro de remover el cliente?')
            if resultado:
                db = DBCliente()
                exito = db.borrar(self.cliente)
                if exito:
                    self.configure_state_entry('normal')
                    self.delete_entry()
                    self.configure_state_to_init('disabled')
                    self.entry_nombre_buscar.delete(0, 'end')
                    messagebox.showinfo('succes', 'Cliente removido')
                    Logger.add_to_log('succes', 'Cliente removido')
                else:
                    messagebox.showerror('error', 'Cliente no borrado')
                    Logger.add_to_log('error', 'Cliente no borrado')
                    Logger.add_to_log('error', traceback.format_exc())
            else:
                pass
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())