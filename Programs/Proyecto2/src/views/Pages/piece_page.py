import traceback
from tkinter import ttk, messagebox

from src.models.piece import Pieza
from src.databases.db_pieza import DbPieza
from src.utils.logger import Logger
from src.utils.base import Base, ESTADO_REPOSO, ESTADO_RESULTADO, ESTADO_NUEVO, ESTADO_EDITANDO


class PiezaPage(Base):
    """
    Página CRUD de Piezas.
    Sigue el mismo patrón que RepairPage: hereda Base, usa _registrar_widget
    y _aplicar_estado para manejar el ciclo de estados de la UI.
    """

    def __init__(self, master, controller):
        super().__init__(master, controller)

        if not self._verificar_acceso(perfil_denegado='Auxiliar'):
            return

        self.pieza = Pieza()

        # ── Frames ──────────────────────────────────────────────────────────
        self.frame_busqueda = ttk.Frame(master)
        self.frame_datos    = ttk.Frame(master)
        self.frame_botones  = ttk.Frame(master)

        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)
        master.rowconfigure(1, weight=1)
        master.rowconfigure(2, weight=1)
        master.rowconfigure(3, weight=1)

        self.frame_busqueda.grid(row=0, column=0, columnspan=5, sticky='ns')
        self.frame_datos.grid   (row=1, column=0, columnspan=5, sticky='ns')
        self.frame_botones.grid (row=2, column=0, columnspan=5, sticky='s')

        # ── BÚSQUEDA ────────────────────────────────────────────────────────
        vcmd = (self.register(self._activar_boton_busqueda_key), '%P')

        self.label_buscar  = ttk.Label(self.frame_busqueda,
                                       text='Ingrese el identificador a buscar')
        self.entry_buscar  = ttk.Entry(self.frame_busqueda, width=25,
                                       validate='key', validatecommand=vcmd)
        self.button_buscar = ttk.Button(self.frame_busqueda, text='Buscar',
                                        command=self.buscar_pieza)

        self.label_buscar .grid(row=0, column=0, sticky='e', pady=5, padx=5)
        self.entry_buscar .grid(row=0, column=1, sticky='w', pady=5, padx=5)
        self.button_buscar.grid(row=0, column=2, sticky='w', pady=5, padx=5)

        # ── DATOS ───────────────────────────────────────────────────────────
        self.label_idPieza     = ttk.Label(self.frame_datos, text='ID Pieza')
        self.entry_idPieza     = ttk.Entry(self.frame_datos, width=10)

        self.label_descripcion = ttk.Label(self.frame_datos, text='Descripción')
        self.entry_descripcion = ttk.Entry(self.frame_datos, width=30)

        self.label_num_serie   = ttk.Label(self.frame_datos, text='Número de serie')
        self.entry_num_serie   = ttk.Entry(self.frame_datos, width=20)

        self.label_precio      = ttk.Label(self.frame_datos, text='Precio')
        self.entry_precio      = ttk.Entry(self.frame_datos, width=15)

        self.label_existencia  = ttk.Label(self.frame_datos, text='Existencia')
        self.entry_existencia  = ttk.Entry(self.frame_datos, width=10)

        vcmd_precio = (self.register(self._validar_decimal_key), '%P')
        vcmd_exist  = (self.register(self._validar_entero_key),  '%P')
        self.entry_precio    .config(validate='key', validatecommand=vcmd_precio)
        self.entry_existencia.config(validate='key', validatecommand=vcmd_exist)

        for row_num, (lbl, wdg) in enumerate([
            (self.label_idPieza,     self.entry_idPieza),
            (self.label_descripcion, self.entry_descripcion),
            (self.label_num_serie,   self.entry_num_serie),
            (self.label_precio,      self.entry_precio),
            (self.label_existencia,  self.entry_existencia),
        ]):
            lbl.grid(row=row_num, column=0, sticky='e', pady=5, padx=5)
            wdg.grid(row=row_num, column=1, sticky='w', pady=5, padx=5)

        # ── BOTONES ─────────────────────────────────────────────────────────
        self.button_new    = ttk.Button(self.frame_botones, text='Nuevo',
                                        command=self.nueva_pieza)
        self.button_save   = ttk.Button(self.frame_botones, text='Salvar',
                                        command=self.salvar_pieza)
        self.button_cancel = ttk.Button(self.frame_botones, text='Cancelar',
                                        command=self.cancelar)
        self.button_edit   = ttk.Button(self.frame_botones, text='Editar',
                                        command=self.editar_pieza)
        self.button_remove = ttk.Button(self.frame_botones, text='Remover',
                                        command=self.remover_pieza)

        self.button_new   .grid(row=0, column=0, pady=20, padx=5)
        self.button_save  .grid(row=0, column=1, pady=20, padx=5)
        self.button_cancel.grid(row=0, column=2, pady=20, padx=5)
        self.button_edit  .grid(row=0, column=3, pady=20, padx=5)
        self.button_remove.grid(row=0, column=4, pady=20, padx=5)

        self.grid(row=0, column=0, sticky='nsew')

        self._registrar_widget(
            self.button_buscar,
            self.entry_buscar,
            self.button_new,
            self.button_save,
            self.button_cancel,
            self.button_edit,
            self.button_remove,
            campos_readonly=[self.entry_idPieza]
        )
        self._aplicar_estado(ESTADO_REPOSO)

    # ════════════════════════════════════════════════════════════════════════
    # VALIDACIONES DE TECLADO
    # ════════════════════════════════════════════════════════════════════════

    def _activar_boton_busqueda_key(self, content):
        if content.isalnum():
            self.button_buscar.config(state='normal')
        else:
            self.button_buscar.config(state='disabled')
        return content.isalnum() or content == ''

    def _validar_decimal_key(self, content):
        if content == '':
            return True
        try:
            float(content)
            return True
        except ValueError:
            return False

    def _validar_entero_key(self, content):
        return content.isdigit() or content == ''

    def _validar_campos(self):
        if not self.entry_descripcion.get().strip():
            messagebox.showwarning('Campo requerido', 'Ingrese la descripción.')
            self.entry_descripcion.focus_set()
            return False
        if not self.entry_num_serie.get().strip():
            messagebox.showwarning('Campo requerido', 'Ingrese el número de serie.')
            self.entry_num_serie.focus_set()
            return False
        precio = self.entry_precio.get().strip()
        if not precio:
            messagebox.showwarning('Campo requerido', 'Ingrese el precio.')
            self.entry_precio.focus_set()
            return False
        if float(precio) <= 0:
            messagebox.showwarning('Precio inválido', 'El precio debe ser mayor a 0.')
            self.entry_precio.focus_set()
            return False
        if not self.entry_existencia.get().strip():
            messagebox.showwarning('Campo requerido', 'Ingrese la existencia.')
            self.entry_existencia.focus_set()
            return False
        return True

    # ════════════════════════════════════════════════════════════════════════
    # HELPERS
    # ════════════════════════════════════════════════════════════════════════

    def _limpiar_campos(self):
        for entry in (self.entry_idPieza, self.entry_descripcion,
                      self.entry_num_serie, self.entry_precio,
                      self.entry_existencia):
            entry.config(state='normal')
            entry.delete(0, 'end')

    def _poblar_campos(self, pieza):
        self.entry_idPieza.config(state='normal')
        self.entry_idPieza.delete(0, 'end')
        self.entry_idPieza.insert(0, str(pieza.getIdPieza()))
        self.entry_idPieza.config(state='disabled')

        self.entry_descripcion.delete(0, 'end')
        self.entry_descripcion.insert(0, str(pieza.getDescripcion()))

        self.entry_num_serie.delete(0, 'end')
        self.entry_num_serie.insert(0, str(pieza.getSerie()))

        self.entry_precio.delete(0, 'end')
        self.entry_precio.insert(0, str(pieza.getPrecio()))

        self.entry_existencia.delete(0, 'end')
        self.entry_existencia.insert(0, str(pieza.getCantidad()))

    def _pieza_desde_campos(self):
        p = Pieza()
        p.setIdPieza    (int(self.entry_idPieza.get()))
        p.setDescripcion(self.entry_descripcion.get().strip())
        p.setSerie      (self.entry_num_serie.get().strip())
        p.setPrecio     (float(self.entry_precio.get()))
        p.setCantidad   (int(self.entry_existencia.get()))
        return p

    # ════════════════════════════════════════════════════════════════════════
    # CRUD
    # ════════════════════════════════════════════════════════════════════════

    def buscar_pieza(self):
        try:
            valor = self.entry_buscar.get().strip()
            if not valor:
                return
            clave = int(valor) if valor.isdigit() else valor
            db = DbPieza()
            exito, pieza = db.search(clave)
            if exito:
                self.pieza = pieza
                self._limpiar_campos()
                self._poblar_campos(pieza)
                self._aplicar_estado(ESTADO_RESULTADO)
            else:
                messagebox.showerror('No encontrado',
                                     f'No existe una pieza con el identificador "{valor}".')
                self.entry_buscar.delete(0, 'end')
                self.entry_buscar.focus_force()
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())

    def nueva_pieza(self):
        try:
            self._limpiar_campos()
            db = DbPieza()
            nuevo_id = db.getMaxIdPieza()
            self.entry_idPieza.config(state='normal')
            self.entry_idPieza.insert(0, str(nuevo_id))
            self.entry_idPieza.config(state='disabled')
            self._aplicar_estado(ESTADO_NUEVO)
            self.entry_descripcion.focus_set()
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())

    def salvar_pieza(self):
        db = DbPieza()
        try:
            if not self._validar_campos():
                return
            self.entry_idPieza.config(state='normal')
            pieza = self._pieza_desde_campos()
            self.entry_idPieza.config(state='disabled')

            if self._aplicar_estado(ESTADO_EDITANDO):
                if db.editPiece(pieza):
                    messagebox.showinfo('Éxito', 'Pieza actualizada correctamente.')
                    Logger.add_to_log('info', f'Pieza editada: {pieza.getIdPieza()}')
                    self._limpiar_campos()
                    self.entry_buscar.delete(0, 'end')
                    self._aplicar_estado(ESTADO_REPOSO)
                else:
                    messagebox.showerror('Error', 'No se pudo actualizar la pieza.')
            else:
                if db.save(pieza):
                    messagebox.showinfo('Éxito', 'Pieza guardada correctamente.')
                    Logger.add_to_log('info', f'Pieza guardada: {pieza.getIdPieza()}')
                    self._limpiar_campos()
                    self.entry_buscar.delete(0, 'end')
                    self._aplicar_estado(ESTADO_REPOSO)
                else:
                    messagebox.showerror('Error', 'No se pudo guardar la pieza.')
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
        finally:
            db.close()

    def editar_pieza(self):
        self._aplicar_estado(ESTADO_EDITANDO)
        self.entry_idPieza.config(state='disabled')

    def remover_pieza(self):
        db = DbPieza()
        try:
            confirmado = messagebox.askyesno(
                'Confirmar eliminación',
                f'¿Estás seguro de eliminar la pieza '
                f'"{self.pieza.getDescripcion()}" (ID: {self.pieza.getIdPieza()})?'
            )
            if not confirmado:
                return
            if db.delete(self.pieza):
                messagebox.showinfo('Éxito', 'Pieza eliminada correctamente.')
                Logger.add_to_log('info', f'Pieza eliminada: {self.pieza.getIdPieza()}')
                self._limpiar_campos()
                self.entry_buscar.delete(0, 'end')
                self._aplicar_estado(ESTADO_REPOSO)
            else:
                messagebox.showerror('Error', 'No se pudo eliminar la pieza.')
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
        finally:
            db.close()

    def cancelar(self):
        self._limpiar_campos()
        self.entry_buscar.delete(0, 'end')
        self._aplicar_estado(ESTADO_REPOSO)