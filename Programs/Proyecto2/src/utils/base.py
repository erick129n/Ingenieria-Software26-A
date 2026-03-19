import traceback
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox

ESTADO_REPOSO = 'reposo'
ESTADO_RESULTADO = 'resultado'
ESTADO_NUEVO = 'nuevo'
ESTADO_EDITANDO = 'editando'

_ORDEN_ESTADOS = [ESTADO_REPOSO, ESTADO_RESULTADO, ESTADO_NUEVO, ESTADO_EDITANDO]

class Base(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller     = controller
        self.usuario_actual = controller.user
        self.perfil         = self.usuario_actual.getPerfil() if self.usuario_actual else None
        self.estado_actual  = None

        self._btn_buscar            = None
        self._entry_buscar          = None
        self._btn_new               = None
        self._btn_save              = None
        self._btn_cancel            = None
        self._btn_edit              = None
        self._btn_delete            = None
        self._campos                = []
        self._campos_solo_nuevo     = []
        self._campos_solo_editando  = []
        self._campos_readonly       = []

    def _registrar_widget(self,
                          btn_buscar,
                          entry_buscar,
                          btn_new,
                          btn_save,
                          btn_cancel,
                          btn_edit,
                          btn_delete,
                          campos=None,
                          campos_solo_nuevo=None,
                          campos_solo_editando=None,
                          campos_readonly=None):
        self._btn_buscar            = btn_buscar
        self._entry_buscar          = entry_buscar
        self._btn_new               = btn_new
        self._btn_save              = btn_save
        self._btn_cancel            = btn_cancel
        self._btn_edit              = btn_edit
        self._btn_delete            = btn_delete
        self._campos                = campos or []
        self._campos_solo_nuevo     = campos_solo_nuevo or []
        self._campos_solo_editando  = campos_solo_editando or []
        self._campos_readonly       = campos_readonly or []

    def _aplicar_estado(self, estado:str):
        self.estado_actual = estado
        es_admin = (self.perfil == "Administrador")

        def on(w):
            if w is not None:
                w.config(state='normal')

        def off(w):
            if w is not None:
                w.config(state='disabled')

        if estado == ESTADO_REPOSO:
            on(self._entry_buscar)
            off(self._btn_buscar)
        else:
            off(self._entry_buscar)
            off(self._btn_buscar)

        for w in self._campos:
            on(w) if estado in (ESTADO_NUEVO, ESTADO_EDITANDO) else off(w)

        for w in self._campos_solo_nuevo:
            on(w) if estado == ESTADO_NUEVO else off(w)

        for w in self._campos_solo_editando:
            on(w) if estado == ESTADO_EDITANDO else off(w)

        for w in self._campos_readonly:
            off(w)
        #nuevo
        on(self._btn_new) if estado == ESTADO_REPOSO else off(self._btn_new)
        #Guardar
        on(self._btn_save) if estado in (ESTADO_NUEVO, ESTADO_EDITANDO) else off(self._btn_save)
        #Cancelar
        on(self._btn_cancel) if estado != ESTADO_REPOSO else off(self._btn_cancel)

        if es_admin and estado == ESTADO_RESULTADO:
            on(self._btn_edit)
            on(self._btn_delete)
        else:
            off(self._btn_edit)
            off(self._btn_delete)

    def _limpiar_entry(self, widget):
        prev = widget.cget('state')
        widget.config(state='normal')
        widget.delete(0, 'end')
        widget.config(state=prev)

    def _limpiar_todos(self, *widgets):
        for w in widgets:
            self._limpiar_entry(w)

    def _verificar_acceso(self, perfil_denegado=None, perfi_requerido=None) -> bool:
        if not self.usuario_actual:
            messagebox.showerror('Acceso denegado', 'Debes inicar sesion')
            self.controller.show_page("MainPage")
            return False
        perfil = self.usuario_actual.getPerfil()
        if perfil_denegado and perfil == perfil_denegado:
            messagebox.showerror('Acceso denegado', 'No tienes permisos')
            self.controller.show_page("MainPage")
            return False
        if perfi_requerido and perfil != perfi_requerido:
            messagebox.showerror('Acceso denegado', 'No tienes permisos')
            self.controller.show_page("MainPage")
            return False
        return True