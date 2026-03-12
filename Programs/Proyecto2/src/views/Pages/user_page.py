import sqlite3
import tkinter as tk
import traceback
from tkinter import messagebox
from tkinter import ttk

from src.databases.dbUsuario import DbUsuario
from src.models.usuario import User
from src.utils.logger import Logger

class UserPage(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.usuario_actual = controller.user

        if not self.usuario_actual or self.usuario_actual.getPerfil() != "Administrador":
            messagebox.showerror("Acceso denegado", 'No tienes permisos para acceder')
            controller.show_page('MainPage')
            return

        self.usuario = User()
        self.seEditaElUsuario = False
        self.frameBuscarUser = tk.Frame(master)
        self.frameDatosUser = tk.Frame(master)
        self.frameBotones = tk.Frame(master)
        self.grid(row=0, column=0, pady=5, padx=5, sticky="nsew")
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)
        master.rowconfigure(1, weight=1)
        master.rowconfigure(2, weight=1)

        self.frameBuscarUser.grid(row=0, column=0, pady=5, padx=5, sticky="ns")
        self.frameDatosUser.grid(row=2, column=0, pady=5, padx=5, sticky="ns")
        self.frameBotones.grid(row=3, column=0, pady=5, padx=5, sticky="s")
        #######  VARIABLE LOCAL QUE VALIDA SI HAY DATOS EN LA BARARA DE BUSQUEDA
        vcmd = (self.register(self.activa_Boton_Busqueda_key), '%P')
        # frame de busqueda de usuario
        self.labelBuscarId = ttk.Label(self.frameBuscarUser, text="Buscar ID de usuario: ")
        self.entryBuscarId = ttk.Entry(self.frameBuscarUser, validate='key', width=10, validatecommand=vcmd)
        self.buttonBuscar = ttk.Button(self.frameBuscarUser, text='Buscar', command=lambda:self.buscar_usuario())
        self.labelBuscarId.grid(row=0, column=0)
        self.entryBuscarId.grid(row=0, column=1)
        self.buttonBuscar.grid(row=0, column=2)


        # frame datos del usuario
        self.labelId = ttk.Label(self.frameDatosUser, text="ID: ")
        self.entryId = ttk.Entry(self.frameDatosUser,width=10)
        self.labelNombre = ttk.Label(self.frameDatosUser, text="Nombre: ")
        self.entryNombre = ttk.Entry(self.frameDatosUser,width=30)
        self.labelUserName = ttk.Label(self.frameDatosUser, text="Username: ")
        self.entryUserName = ttk.Entry(self.frameDatosUser,width=30)
        self.labelPassword = ttk.Label(self.frameDatosUser, text="Password: ")
        self.entryPassword = ttk.Entry(self.frameDatosUser,width=20, show='*')
        self.checkPassword = ttk.Checkbutton(self.frameDatosUser, text="Mostrar contraseña", command=lambda:self.show_password())
        self.labelPerfil = ttk.Label(self.frameDatosUser, text="Perfil: ")
        self.comboBoxPerfil = ttk.Combobox(self.frameDatosUser, values=['Administrador', 'Auxiliar', 'Mecanico'])

        self.labelId.grid(row=0, column=0, sticky="e")
        self.entryId.grid(row=0, column=1, sticky="w")
        self.labelNombre.grid(row=1, column=0, sticky="e")
        self.entryNombre.grid(row=1, column=1, sticky="w")
        self.labelUserName.grid(row=2, column=0, sticky="e")
        self.entryUserName.grid(row=2, column=1, sticky="w")
        self.labelPassword.grid(row=3, column=0, sticky="e")
        self.entryPassword.grid(row=3, column=1, sticky="w")
        self.checkPassword.grid(row=3, column=2, sticky="w")
        self.labelPerfil.grid(row=4, column=0, sticky="e")
        self.comboBoxPerfil.grid(row=4, column=1, sticky="w")



        #frame de botones
        self.buttonNew = ttk.Button(self.frameBotones, text='Nuevo', command=lambda:self.new_usuario())
        self.buttonSave = ttk.Button(self.frameBotones, text='Salvar', command=lambda:self.salvarUsuario())
        self.buttonCancel = ttk.Button(self.frameBotones, text='Cancelar', command=lambda:self.cancelarUsuario())
        self.buttonEdit = ttk.Button(self.frameBotones, text='Editar', command=lambda:self.editarUsuario())
        self.buttonRemove = ttk.Button(self.frameBotones, text='Remover', command=lambda:self.removeUsuario())

        self.buttonNew.grid(row=0, column=0, sticky="e")
        self.buttonSave.grid(row=0, column=1, sticky="e")
        self.buttonCancel.grid(row=0, column=2, sticky="e")
        self.buttonEdit.grid(row=0, column=3, sticky="e")
        self.buttonRemove.grid(row=0, column=4, sticky="e")


        for widget in self.frameBuscarUser.winfo_children():
            widget.grid_configure(pady=15, padx=5)
        for widget in self.frameDatosUser.winfo_children():
            widget.grid_configure(pady=10, padx=5)
        for widget in self.frameBotones.winfo_children():
            widget.grid_configure(pady=50, padx=5)

        """
            ES FUNDAMENTAL ENTENDER QUE AQUI SE DESABILITAN AL INICAR EL PROGRAMA
            AQUI ESTA EL CONTROL Y LA FUNCION
        """
        self.config_state_to_init('disabled')

    def config_state_to_init(self, control):
        self.buttonBuscar.configure(state=control)
        self.entryId.configure(state=control)
        self.entryNombre.configure(state=control)
        self.entryUserName.configure(state=control)
        self.entryPassword.configure(state=control)
        self.checkPassword.configure(state=control)
        self.comboBoxPerfil.configure(state=control)
        self.buttonSave.configure(state=control)
        self.buttonCancel.configure(state=control)
        self.buttonEdit.configure(state=control)
        self.buttonRemove.configure(state=control)

    def config_state_entrys(self, control):
        self.entryId.config(state=control)
        self.entryNombre.config(state=control)
        self.entryUserName.config(state=control)
        self.entryPassword.config(state=control)
        self.comboBoxPerfil.config(state=control)
        self.checkPassword.config(state=control)

    def delete_entry(self):
        self.entryId.delete(0, 'end')
        self.entryNombre.delete(0, 'end')
        self.entryUserName.delete(0, 'end')
        self.entryPassword.delete(0, 'end')
        self.comboBoxPerfil.delete(0, 'end')
        self.entryBuscarId.delete(0, 'end')

    def put_data_user_in_entry(self, usuario):
        self.entryId.insert(0, str(usuario.getUsuario_id()))
        self.entryNombre.insert(0, str(usuario.getNombre()))
        self.entryUserName.insert(0, str(usuario.getUserName()))
        self.entryPassword.insert(0, str(usuario.getPassword()))
        self.comboBoxPerfil.insert(0, str(usuario.getPerfil()))

    def show_password(self):
        if self.entryPassword.cget('show') == '*':
            self.entryPassword.config(show='')
            Logger.add_to_log('warning', 'se ah mostrado una contraseña')
        else:
            self.entryPassword.config(show='*')
    def activa_Boton_Busqueda_key(self, content):
        if content.isdigit():
            self.buttonBuscar.config(state=tk.NORMAL)
        else:
            self.buttonBuscar.config(state=tk.DISABLED)
        return content.isdigit() or content == ""

    def buscar_usuario(self):
        try:
            try:
                id_usuario = int(self.entryBuscarId.get().strip())
            except ValueError as e:
                Logger.add_to_log('error', str(e))
                Logger.add_to_log('error', traceback.format_exc())
                return
            db = DbUsuario()
            exito, aux = db.buscar(id_usuario)
            if exito:
                self.usuario = aux
                Logger.add_to_log('debug', 'Usuario buscado:' + str(aux.getNombre()))
                self.config_state_to_init('NORMAL')
                self.delete_entry()
                self.put_data_user_in_entry(self.usuario)
                self.config_state_to_init('disabled')
                self.buttonNew.config(state=tk.DISABLED)
                self.checkPassword.configure(state=tk.NORMAL)
                self.buttonEdit.configure(state=tk.NORMAL)
                self.buttonRemove.configure(state=tk.NORMAL)
                self.buttonCancel.configure(state=tk.NORMAL)
            else:
                messagebox.showerror('error', 'Usuario no encontrado')
                Logger.add_to_log('error', 'Usuario no encontrado')
                self.entryBuscarId.delete(0, 'end')
                self.entryBuscarId.focus()
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())

    def new_usuario(self):
        try:
            self.config_state_entrys('NORMAL')
            self.delete_entry()
            db = DbUsuario()
            aux_id = db.getMaxId()
            self.entryId.insert(0, str(aux_id))
            self.entryId.config(state=tk.DISABLED)
            self.buttonSave.configure(state=tk.NORMAL)
            self.buttonCancel.configure(state=tk.NORMAL)
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
        except sqlite3.IntegrityError as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())


    def salvarUsuario(self):
        try:
            self.config_state_entrys('NORMAL')
            user_id = int(self.entryId.get().strip())
            user_nombre = self.entryNombre.get().strip()
            user_username = self.entryUserName.get().strip()
            user_password = (self.entryPassword.get().strip())
            user_perfil = self.comboBoxPerfil.get().strip()
            usr = User(user_id,user_nombre,user_username,user_password,user_perfil)
            db = DbUsuario()
            if self.seEditaElUsuario:
                try:
                    if db.editar(usr):
                        messagebox.showinfo('succes', 'Usuario actualizado')
                        Logger.add_to_log('succes', 'Usuario actualizado')
                        self.delete_entry()
                        self.entryBuscarId.delete(0, 'end')
                        self.config_state_to_init('disabled')
                        self.seEditaElUsuario = False
                        Logger.add_to_log('info','Usuario editado:'+ str(usr.getNombre()))
                        return
                    else:
                        messagebox.showerror('error', 'Usuario no guardado')
                        Logger.add_to_log('error', 'Usuario no guardado')

                except Exception as e:
                    Logger.add_to_log('error', str(e))
                    Logger.add_to_log('error', traceback.format_exc())
            else:
                exito = db.save(usr)
                if exito:
                    messagebox.showinfo('success', 'Usuario guardado')
                    Logger.add_to_log('info','Usuario guardado:'+ str(usr.getNombre()))
                    self.delete_entry()
                    self.config_state_to_init('disabled')
                else:
                    messagebox.showerror('error', 'Usuario no guardado')
                    Logger.add_to_log('error', 'Usuario no guardado')
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())

    def cancelarUsuario(self):
        self.config_state_to_init('NORMAL')
        self.delete_entry()
        self.config_state_to_init('disabled')
        self.buttonNew.configure(state=tk.NORMAL)

    def editarUsuario(self):
        self.config_state_to_init('NORMAL')
        self.entryId.config(state=tk.DISABLED)
        self.buttonNew.configure(state=tk.DISABLED)
        self.buttonEdit.configure(state=tk.DISABLED)
        self.buttonRemove.configure(state=tk.DISABLED)
        self.seEditaElUsuario = True

    def removeUsuario(self):
        if self.usuario.getUsuario_id() == self.usuario_actual.getUsuario_id():
            messagebox.showinfo('Error', 'No puedes elimarte')
            return
        resultado = messagebox.askyesno('Borrar', 'Estas seguro de eliminar este usuario?')
        try:
            if resultado:
                db = DbUsuario()
                exito = db.borrar(self.usuario)
                if exito:
                    self.config_state_entrys('NORMAL')
                    self.delete_entry()
                    self.config_state_to_init('disabled')
                    self.entryBuscarId.delete(0, 'end')
                    messagebox.showinfo('succes', 'Usuario eliminado')
                    Logger.add_to_log('info','Usuario eliminado: ' + str(self.usuario.getNombre()))
                else:
                    messagebox.showerror('error', 'Usuario no borrado')
                    Logger.add_to_log('error', 'Usuario no borrado')
            else:
                pass
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
