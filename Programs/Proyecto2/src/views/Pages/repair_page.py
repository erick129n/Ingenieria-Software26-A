import traceback
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import date

from src.models.repair import Repair
from src.models.detRepair import DetRepairacion
from src.databases.db_repair import DbRepair
from src.utils.logger import Logger
from src.utils.base import Base, ESTADO_REPOSO, ESTADO_RESULTADO, ESTADO_NUEVO, ESTADO_EDITANDO


class RepairPage(Base):
    """
    Página de Reparaciones ajustada a ventana 700×400.

    Layout (columnas 0..1, filas 0..3):
        fila 0: frame_busqueda  (span 2 cols)
        fila 1: frame_datos (col 0) | frame_tabla (col 1)   ← lado a lado
        fila 2: frame_det       (span 2 cols)
        fila 3: frame_botones   (span 2 cols)
    """

    def __init__(self, master, controller):
        super().__init__(master, controller)

        if not self._verificar_acceso(perfil_denegado='Auxiliar'):
            return

        self.reparacion     = Repair()
        self.det_reparacion = DetRepairacion()

        # ── Configuración del contenedor padre ───────────────────────────────
        master.columnconfigure(0, weight=2)   # col datos
        master.columnconfigure(1, weight=3)   # col tabla (más ancha)
        master.rowconfigure(0, weight=0)
        master.rowconfigure(1, weight=1)      # fila principal se expande
        master.rowconfigure(2, weight=0)
        master.rowconfigure(3, weight=0)

        # ── Frames ───────────────────────────────────────────────────────────
        self.frame_busqueda = ttk.Frame(master)
        self.frame_datos    = ttk.LabelFrame(master, text='Reparación')
        self.frame_tabla    = ttk.LabelFrame(master, text='Detalle de piezas')
        self.frame_det      = ttk.Frame(master)
        self.frame_botones  = ttk.Frame(master)

        self.frame_busqueda.grid(row=0, column=0, columnspan=2, sticky='ew',  padx=6, pady=(4,0))
        self.frame_datos   .grid(row=1, column=0, sticky='nsew', padx=(6,3),  pady=2)
        self.frame_tabla   .grid(row=1, column=1, sticky='nsew', padx=(3,6),  pady=2)
        self.frame_det     .grid(row=2, column=0, columnspan=2, sticky='ew',  padx=6, pady=(0,2))
        self.frame_botones .grid(row=3, column=0, columnspan=2, sticky='ew',  padx=6, pady=(0,4))

        # ── BÚSQUEDA ─────────────────────────────────────────────────────────
        vcmd = (self.register(self._activar_boton_busqueda_key), '%P')

        self.label_buscar  = ttk.Label(self.frame_busqueda, text='Folio:')
        self.entry_buscar  = ttk.Entry(self.frame_busqueda, width=12,
                                       validate='key', validatecommand=vcmd)
        self.button_buscar = ttk.Button(self.frame_busqueda, text='Buscar',
                                        command=self.buscar_reparacion)

        self.label_buscar .grid(row=0, column=0, sticky='e', pady=3, padx=4)
        self.entry_buscar .grid(row=0, column=1, sticky='w', pady=3, padx=4)
        self.button_buscar.grid(row=0, column=2, sticky='w', pady=3, padx=4)

        # ── DATOS DE REPARACIÓN (columna izquierda) ──────────────────────────
        self.frame_datos.columnconfigure(1, weight=1)

        self.label_folio         = ttk.Label(self.frame_datos, text='Folio')
        self.entry_folio         = ttk.Entry(self.frame_datos, width=8)

        self.label_matricula     = ttk.Label(self.frame_datos, text='Matrícula')
        self.combo_matricula     = ttk.Combobox(self.frame_datos, width=14, state='readonly')

        self.label_fecha_entrada = ttk.Label(self.frame_datos, text='F. entrada')
        self.date_entrada        = DateEntry(self.frame_datos, width=11,
                                             date_pattern='yyyy-mm-dd',
                                             maxdate=date.today())

        self.label_fecha_salida  = ttk.Label(self.frame_datos, text='F. salida')
        self.date_salida         = DateEntry(self.frame_datos, width=11,
                                             date_pattern='yyyy-mm-dd',
                                             mindate=date.today())

        self.label_descripcion   = ttk.Label(self.frame_datos, text='Descripción')
        self.entry_descripcion   = ttk.Entry(self.frame_datos, width=18)

        self.label_usuario_id    = ttk.Label(self.frame_datos, text='Usuario ID')
        self.entry_usuario_id    = ttk.Entry(self.frame_datos, width=8)

        for row, (lbl, wdg) in enumerate([
            (self.label_folio,         self.entry_folio),
            (self.label_matricula,     self.combo_matricula),
            (self.label_fecha_entrada, self.date_entrada),
            (self.label_fecha_salida,  self.date_salida),
            (self.label_descripcion,   self.entry_descripcion),
            (self.label_usuario_id,    self.entry_usuario_id),
        ]):
            lbl.grid(row=row, column=0, sticky='e', pady=2, padx=(6,2))
            wdg.grid(row=row, column=1, sticky='ew', pady=2, padx=(2,6))

        self.date_entrada.bind("<<DateEntrySelected>>", self._validar_fechas)
        self.date_salida .bind("<<DateEntrySelected>>", self._validar_fechas)

        # ── TABLA DE DETALLE (columna derecha) ───────────────────────────────
        self.frame_tabla.columnconfigure(0, weight=1)
        self.frame_tabla.rowconfigure(0, weight=1)

        columnas = ('folio', 'rep_id', 'pieza_id', 'cantidad')
        self.tree = ttk.Treeview(self.frame_tabla, columns=columnas,
                                 show='headings', height=5)
        for col, ancho, titulo in [
            ('folio',    55,  'Folio'),
            ('rep_id',   55,  'Rep.ID'),
            ('pieza_id', 65,  'Pieza'),
            ('cantidad', 55,  'Cant.'),
        ]:
            self.tree.heading(col, text=titulo)
            self.tree.column (col, width=ancho, anchor='center', stretch=True)

        scroll_tree = ttk.Scrollbar(self.frame_tabla, orient='vertical',
                                    command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll_tree.set)
        self.tree.grid      (row=0, column=0, sticky='nsew', padx=(4,0), pady=4)
        scroll_tree.grid    (row=0, column=1, sticky='ns',             pady=4)

        # ── SECCIÓN DETALLE (fila compacta) ──────────────────────────────────
        vcmd_cant = (self.register(self._validar_cantidad_key), '%P')

        ttk.Label(self.frame_det, text='Pieza:')      .grid(row=0, column=0, padx=(4,2), pady=3, sticky='e')
        self.combo_det_pieza    = ttk.Combobox(self.frame_det, width=16, state='readonly')
        self.combo_det_pieza    .grid(row=0, column=1, padx=2, pady=3, sticky='w')

        ttk.Label(self.frame_det, text='ID:')         .grid(row=0, column=2, padx=(4,2), pady=3, sticky='e')
        self.entry_det_id_pieza = ttk.Entry(self.frame_det, width=5, state='disabled')
        self.entry_det_id_pieza .grid(row=0, column=3, padx=2, pady=3, sticky='w')

        ttk.Label(self.frame_det, text='Cant:')       .grid(row=0, column=4, padx=(4,2), pady=3, sticky='e')
        self.entry_det_cantidad = ttk.Entry(self.frame_det, width=5,
                                            validate='key', validatecommand=vcmd_cant)
        self.entry_det_cantidad .grid(row=0, column=5, padx=2, pady=3, sticky='w')

        self.button_det_agregar = ttk.Button(self.frame_det, text='Agregar',
                                             command=self.agregar_detalle)
        self.button_det_agregar .grid(row=0, column=6, padx=4, pady=3, sticky='w')

        self.button_det_quitar  = ttk.Button(self.frame_det, text='Quitar',
                                             command=self.quitar_detalle)
        self.button_det_quitar  .grid(row=0, column=7, padx=4, pady=3, sticky='w')

        self.combo_det_pieza.bind("<<ComboboxSelected>>", self._on_pieza_seleccionada)

        # ── BOTONES CRUD (fila inferior, centrados) ───────────────────────────
        self.frame_botones.columnconfigure(list(range(5)), weight=1)

        self.button_new    = ttk.Button(self.frame_botones, text='Nuevo',
                                        command=self.nueva_reparacion)
        self.button_save   = ttk.Button(self.frame_botones, text='Salvar',
                                        command=self.salvar_reparacion)
        self.button_cancel = ttk.Button(self.frame_botones, text='Cancelar',
                                        command=self.cancelar)
        self.button_edit   = ttk.Button(self.frame_botones, text='Editar',
                                        command=self.editar_reparacion)
        self.button_remove = ttk.Button(self.frame_botones, text='Remover',
                                        command=self.remover_reparacion)

        for col, btn in enumerate([self.button_new, self.button_save,
                                   self.button_cancel, self.button_edit,
                                   self.button_remove]):
            btn.grid(row=0, column=col, sticky='ew', padx=4, pady=4)

        self.grid(row=0, column=0, sticky='nsew')

        # ── Registro y estado inicial ─────────────────────────────────────────
        self._registrar_widget(
            self.button_buscar,
            self.entry_buscar,
            self.button_new,
            self.button_save,
            self.button_cancel,
            self.button_edit,
            self.button_remove,
            campos_readonly=[self.entry_folio]
        )
        self._aplicar_estado(ESTADO_REPOSO)
        self._cargar_combos()

    # ════════════════════════════════════════════════════════════════════════
    # VALIDACIONES
    # ════════════════════════════════════════════════════════════════════════

    def _activar_boton_busqueda_key(self, content):
        if content.isdigit() and len(content) > 0:
            self.button_buscar.config(state='normal')
        else:
            self.button_buscar.config(state='disabled')
        return content.isdigit() or content == ''

    def _validar_cantidad_key(self, content):
        return content.isdigit() or content == ''

    def _validar_fechas(self, event=None):
        entrada = self.date_entrada.get_date()
        salida  = self.date_salida.get_date()
        if salida < entrada:
            self.date_salida.set_date(entrada)
            messagebox.showwarning(
                'Fecha inválida',
                'La fecha de salida no puede ser anterior a la de entrada.\n'
                'Se ajustó automáticamente.'
            )

    def _validar_campos_reparacion(self):
        if not self.combo_matricula.get():
            messagebox.showwarning('Campo requerido', 'Seleccione la matrícula del vehículo.')
            return False
        if not self.entry_descripcion.get().strip():
            messagebox.showwarning('Campo requerido', 'Ingrese una descripción.')
            return False
        if not self.entry_usuario_id.get().strip():
            messagebox.showwarning('Campo requerido', 'Ingrese el ID de usuario.')
            return False
        self._validar_fechas()
        return True

    # ════════════════════════════════════════════════════════════════════════
    # HELPERS
    # ════════════════════════════════════════════════════════════════════════

    def _cargar_combos(self):
        db = DbRepair()
        try:
            self.combo_matricula['values'] = db.get_lista_matriculas()
            self.combo_det_pieza['values'] = db.get_lista_piezas()
            self._map_piezas = db.get_map_piezas()
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
        finally:
            db.close()

    def _on_pieza_seleccionada(self, event=None):
        nombre   = self.combo_det_pieza.get()
        pieza_id = self._map_piezas.get(nombre, '')
        self.entry_det_id_pieza.config(state='normal')
        self.entry_det_id_pieza.delete(0, 'end')
        self.entry_det_id_pieza.insert(0, str(pieza_id))
        self.entry_det_id_pieza.config(state='disabled')

    def _limpiar_campos(self):
        for entry in (self.entry_folio, self.entry_descripcion, self.entry_usuario_id):
            entry.config(state='normal')
            entry.delete(0, 'end')
        self.combo_matricula.set('')
        self.date_entrada.set_date(date.today())
        self.date_salida .set_date(date.today())
        self.entry_det_id_pieza.config(state='normal')
        self.entry_det_id_pieza.delete(0, 'end')
        self.entry_det_id_pieza.config(state='disabled')
        self.combo_det_pieza.set('')
        self.entry_det_cantidad.delete(0, 'end')
        for row in self.tree.get_children():
            self.tree.delete(row)

    def _poblar_campos(self):
        self.entry_folio.config(state='normal')
        self.entry_folio.delete(0, 'end')
        self.entry_folio.insert(0, str(self.reparacion.getFolio()))
        self.entry_folio.config(state='disabled')
        self.combo_matricula.set(str(self.reparacion.getMatricula()))
        self.date_entrada.set_date(self.reparacion.getFecha_entrada())
        self.date_salida .set_date(self.reparacion.getFecha_saida())
        self.entry_descripcion.delete(0, 'end')
        self.entry_descripcion.insert(0, str(self.reparacion.getDescripcion()))
        self.entry_usuario_id.delete(0, 'end')
        self.entry_usuario_id.insert(0, str(self.reparacion.getUsuarioId()))

    def _cargar_tabla_detalle(self, rep_id):
        for row in self.tree.get_children():
            self.tree.delete(row)
        db = DbRepair()
        try:
            for det in db.get_detalles_by_rep(rep_id):
                self.tree.insert('', 'end', values=(
                    det.getFolio(), det.getRepId(),
                    det.getIdPieza(), det.getCantidad()
                ))
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
        finally:
            db.close()

    # ════════════════════════════════════════════════════════════════════════
    # ACCIONES DE DETALLE
    # ════════════════════════════════════════════════════════════════════════

    def agregar_detalle(self):
        pieza_id = self.entry_det_id_pieza.get().strip()
        cantidad = self.entry_det_cantidad.get().strip()
        if not pieza_id:
            messagebox.showwarning('Campo requerido', 'Seleccione una pieza.')
            return
        if not cantidad or int(cantidad) <= 0:
            messagebox.showwarning('Cantidad inválida', 'La cantidad debe ser mayor a 0.')
            return
        for item in self.tree.get_children():
            if str(self.tree.item(item, 'values')[2]) == pieza_id:
                messagebox.showwarning('Duplicado', 'Esa pieza ya está en el detalle.')
                return
        rep_id = self.entry_folio.get() or '—'
        self.tree.insert('', 'end', values=('nuevo', rep_id, pieza_id, cantidad))
        self.combo_det_pieza.set('')
        self.entry_det_id_pieza.config(state='normal')
        self.entry_det_id_pieza.delete(0, 'end')
        self.entry_det_id_pieza.config(state='disabled')
        self.entry_det_cantidad.delete(0, 'end')

    def quitar_detalle(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning('Sin selección', 'Seleccione una fila del detalle para quitar.')
            return
        item  = seleccion[0]
        vals  = self.tree.item(item, 'values')
        folio = vals[0]
        if folio != 'nuevo':
            if not messagebox.askyesno('Confirmar', f'¿Eliminar el detalle con folio {folio}?'):
                return
            db = DbRepair()
            try:
                det = DetRepairacion()
                det.setFolio(int(folio))
                if not db.deleteDetail(det):
                    messagebox.showerror('Error', 'No se pudo eliminar el detalle.')
                    return
            except Exception as e:
                Logger.add_to_log('error', str(e))
                Logger.add_to_log('error', traceback.format_exc())
                return
            finally:
                db.close()
        self.tree.delete(item)

    # ════════════════════════════════════════════════════════════════════════
    # CRUD REPARACIÓN
    # ════════════════════════════════════════════════════════════════════════

    def buscar_reparacion(self):
        try:
            folio = self.entry_buscar.get().strip()
            if not folio:
                return
            db = DbRepair()
            exito, reparacion = db.searchRepair(int(folio))
            if exito:
                self.reparacion = reparacion
                self._limpiar_campos()
                self._poblar_campos()
                self._cargar_tabla_detalle(reparacion.getFolio())
                self._aplicar_estado(ESTADO_RESULTADO)
            else:
                messagebox.showerror('No encontrado',
                                     f'No existe una reparación con folio {folio}.')
                self.entry_buscar.delete(0, 'end')
                self.entry_buscar.focus_force()
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())

    def nueva_reparacion(self):
        try:
            self._limpiar_campos()
            nuevo_id = DbRepair().getMaxRepId()
            self.entry_folio.config(state='normal')
            self.entry_folio.insert(0, str(nuevo_id))
            self.entry_folio.config(state='disabled')
            self._aplicar_estado(ESTADO_NUEVO)
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())

    def salvar_reparacion(self):
        try:
            if not self._validar_campos_reparacion():
                return

            rep = Repair()
            rep.setMatricula    (str(self.combo_matricula.get()))
            rep.setFecha_entrada(str(self.date_entrada.get_date()))
            rep.setFecha_saida  (str(self.date_salida.get_date()))
            rep.setDescripcion  (self.entry_descripcion.get().strip())
            rep.setUsuarioId    (self.entry_usuario_id.get().strip())

            db = DbRepair()

            if self.estado_actual == ESTADO_EDITANDO:
                rep.setFolio(int(self.entry_folio.get()))
                if db.editRepair(rep):
                    messagebox.showinfo('Éxito', 'Reparación actualizada correctamente.')
                    Logger.add_to_log('info', f'Reparación editada: {rep.getFolio()}')
                else:
                    messagebox.showerror('Error', 'No se pudo actualizar la reparación.')
                    return
            else:
                if not db.saveRepair(rep):
                    messagebox.showerror('Error', 'No se pudo guardar la reparación.')
                    return
                rep_id = db.getMaxRepId() - 1
                rep.setFolio(rep_id)
                for item in self.tree.get_children():
                    vals = self.tree.item(item, 'values')
                    if vals[0] == 'nuevo':
                        det = DetRepairacion()
                        det.setRepId(rep_id)
                        det.setIdPieza(int(vals[2]))
                        det.setCantidad(int(vals[3]))
                        db.saveDetail(det)
                messagebox.showinfo('Éxito', 'Reparación guardada correctamente.')
                Logger.add_to_log('info', 'Nueva reparación guardada.')

            self._limpiar_campos()
            self.entry_buscar.delete(0, 'end')
            self._aplicar_estado(ESTADO_REPOSO)
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())

    def editar_reparacion(self):
        self._aplicar_estado(ESTADO_EDITANDO)
        self.entry_folio.config(state='disabled')
        self.combo_matricula.config(state='disabled')

    def remover_reparacion(self):
        try:
            if not messagebox.askyesno('Confirmar eliminación',
                                       '¿Estás seguro de eliminar esta reparación y todo su detalle?'):
                return
            db = DbRepair()
            if db.deleteRepair(self.reparacion):
                messagebox.showinfo('Éxito', 'Reparación eliminada.')
                Logger.add_to_log('info', f'Reparación eliminada: {self.reparacion.getFolio()}')
                self._limpiar_campos()
                self.entry_buscar.delete(0, 'end')
                self._aplicar_estado(ESTADO_REPOSO)
            else:
                messagebox.showerror('Error', 'No se pudo eliminar la reparación.')
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())

    def cancelar(self):
        self._limpiar_campos()
        self.entry_buscar.delete(0, 'end')
        self._aplicar_estado(ESTADO_REPOSO)