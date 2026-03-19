import sqlite3
import tkinter as tk
import traceback
from tkinter import messagebox
from tkinter import ttk

from src.databases.dbUsuario import DbUsuario
from src.models.usuario import User
from src.utils.logger import Logger
from src.utils.base import Base, ESTADO_REPOSO, ESTADO_RESULTADO, ESTADO_NUEVO, ESTADO_EDITANDO

class UserPage(Base):
    def __init__(self, master, controller):
        super().__init__(master, controller)

        if not self._verificar_acceso(perfi_requerido='Administrador'):
            return

        self.usuario = User()

        self.frameBuscarUser = tk.Frame(master)
        self.frameDatosUser  = tk.Frame(master)
        self.frameBotones    = tk.Frame(master)
        self.grid(row=0, column=0, pady=5, padx=5, sticky="nsew")
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)
        master.rowconfigure(1, weight=1)
        master.rowconfigure(2, weight=1)

        self.frameBuscarUser.grid(row=0, column=0, pady=5, padx=5, sticky="ns")
        self.frameDatosUser.grid(row=2, column=0, pady=5, padx=5, sticky="ns")
        self.frameBotones.grid(row=3, column=0, pady=5, padx=5, sticky="s")



        #######  VARIABLE LOCAL QUE VALIDA SI HAY DATOS EN LA BARARA DE BUSQUEDA
        vcmd = (self.register(self.validar_busqueda), '%P')
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

        self._registrar_widget(
            btn_buscar= self.buttonBuscar,
            entry_buscar = self.entryBuscarId,
            btn_new = self.buttonNew,
            btn_save = self.buttonSave,
            btn_cancel= self.buttonCancel,
            btn_edit= self.buttonEdit,
            btn_delete=self.buttonRemove,
            campos = [
                self.entryNombre,
                self.entryUserName,
                self.entryPassword,
                self.checkPassword,
                self.comboBoxPerfil,
            ],
            campos_readonly= [self.entryId],
        )
        self._aplicar_estado(ESTADO_REPOSO)

    def poblar_campos(self, usuario:User):
        for entry, valor in(
                (self.entryId, usuario.getUsuario_id()),
                (self.entryNombre, usuario.getNombre()),
                (self.entryUserName, usuario.getUserName()),
                (self.entryPassword, usuario.getPassword()),
        ):
            entry.config(state='normal')
            entry.insert(0, str(valor))
        self.comboBoxPerfil.set(str(usuario.getPerfil()))

    def validar_busqueda(self, content):
        valido = content == '' or content.isdigit()
        if valido:
            self.buttonBuscar.config(state='normal' if content else 'disabled')
        return valido

    def limpiar_campos(self):
        self._limpiar_todos(
            self.entryBuscarId,
            self.entryId,
            self.entryNombre,
            self.entryUserName,
            self.entryPassword,
        ),
        self.comboBoxPerfil.set('')

    def poblar_campos(self, usuario):
        for entry, valor in(
                (self.entryId, usuario.getUsuario_id()),
                (self.entryNombre, usuario.getNombre()),
                (self.entryUserName, usuario.getUserName()),
                (self.entryPassword, usuario.getPassword()),
        ):
            entry.config(state='normal')
            entry.insert(0, str(valor))
            self.comboBoxPerfil.set(str(usuario.getPerfil()))


    def show_password(self):
        if self.entryPassword.cget('show') == '*':
            self.entryPassword.config(show='')
            Logger.add_to_log('warning', 'se ah mostrado una contraseña')
        else:
            self.entryPassword.config(show='*')

    def buscar_usuario(self):
        try:
            try:
                id_usuario = int(self.entryBuscarId.get().strip())
            except ValueError as e:
                Logger.add_to_log('error', str(e))
                Logger.add_to_log('error', traceback.format_exc())
                return
            db = DbUsuario()
            exito, aux = db.buscar(int(id_usuario))
            if exito:
                self.usuario = aux

                self.limpiar_campos()
                self.poblar_campos(self.usuario)
                self._aplicar_estado(ESTADO_RESULTADO)
                #check password
                self.checkPassword.config(state='normal')
                Logger.add_to_log('debug', 'Usuario buscado:' + str(aux.getNombre()))
            else:
                messagebox.showerror('error', 'Usuario no encontrado')
                Logger.add_to_log('error', 'Usuario no encontrado')
                self.entryBuscarId.delete(0, 'end')
                self.entryBuscarId.focus()
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
            self._aplicar_estado(ESTADO_REPOSO)

    def new_usuario(self):
        try:
            self.limpiar_campos()
            db = DbUsuario()
            aux_id = db.getMaxId()
            self.entryId.config(state='normal')
            self.entryId.insert(0, str(aux_id))
            self.entryId.config(state=tk.DISABLED)
            self._aplicar_estado(ESTADO_NUEVO)
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
            self._aplicar_estado(ESTADO_REPOSO)
        except sqlite3.IntegrityError as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())


    def salvarUsuario(self):
        try:
            self.entryId.config(state='normal')
            user_id = int(self.entryId.get().strip())
            self.entryId.config(state=tk.DISABLED)
            user_nombre = self.entryNombre.get().strip()
            user_username = self.entryUserName.get().strip()
            user_password = (self.entryPassword.get().strip())
            user_perfil = self.comboBoxPerfil.get().strip()

            if not user_id:
                messagebox.showerror('error', 'El campo es obligatorio'); return
            if not user_nombre:
                messagebox.showerror('error', 'El campo es obligatorio'); return
            if not user_username:
                messagebox.showerror('error', 'El campo es obligatorio'); return
            if not user_password:
                messagebox.showerror('error', 'El campo es obligatorio'); return
            if not user_perfil:
                messagebox.showerror('error', 'El campo es obligatorio'); return

            usr = User(user_id,user_nombre,user_username,user_password,user_perfil)
            db = DbUsuario()
            if self.estado_actual == ESTADO_EDITANDO:
                try:
                    if db.editar(usr):
                        messagebox.showinfo('succes', 'Usuario actualizado')
                        Logger.add_to_log('succes', 'Usuario actualizado')
                        self.limpiar_campos()
                        self._aplicar_estado(ESTADO_REPOSO)
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
                    self.limpiar_campos()
                    self._aplicar_estado(ESTADO_REPOSO)
                else:
                    messagebox.showerror('error', 'Usuario no guardado')
                    Logger.add_to_log('error', 'Usuario no guardado')
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
            self._aplicar_estado(ESTADO_REPOSO)

    def cancelarUsuario(self):
        self.limpiar_campos()
        self._aplicar_estado(ESTADO_REPOSO)

    def editarUsuario(self):
        try:
            self._aplicar_estado(ESTADO_EDITANDO)
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
            self._aplicar_estado(ESTADO_REPOSO)

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
                    messagebox.showinfo('succes', 'Usuario eliminado')
                    Logger.add_to_log('info','Usuario eliminado: ' + str(self.usuario.getNombre()))
                    self.limpiar_campos()
                    self._aplicar_estado(ESTADO_REPOSO)
                else:
                    messagebox.showerror('error', 'Usuario no borrado')
                    Logger.add_to_log('error', 'Usuario no borrado')
                    self._aplicar_estado(ESTADO_RESULTADO)
            else:
                return
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
            self._aplicar_estado(ESTADO_REPOSO)
