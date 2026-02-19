import os
import tkinter as tk
from tkinter import ttk
import tkcalendar as tkcal
from tkcalendar import DateEntry
from tkinter import messagebox
from Cliente import Cliente
from Habitacion import Room
from Archivo import Archivo
from Reservacion import Reservacion


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Reservaciones')
        self.geometry('650x400')
        #self.resizable(width=False, height=False)
        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True)
        self.reservations_frame = ttk.Frame(notebook) #es la hija de la padre notebook, es decir, el contenedor de las reservaciones
        self.client_frame = ttk.Frame(notebook)
        self.rooms_frame = ttk.Frame(notebook)

        notebook.add(self.client_frame, text='Clientes')
        notebook.add(self.reservations_frame, text='Reservaciones')
        notebook.add(self.rooms_frame, text='Habitaciones')


        self.ESTADO_VACIO = 'Vacio'
        self.ESTADO_SINGUARDAR = 'Sin guardar'
        self.ESTADO_GUARDADO = 'Guardado'
        self.ESTADO_EDITANDO = 'Editando'
        self.ESTADO_ELIMINANDO = 'Eliminando'
        self.estadoActual = self.ESTADO_VACIO
        print(f"Estado actual al iniciar la app: {self.estadoActual}")
        self.id_cliente = 0
        self.id_habitacion = 0
        self.id_reservacion = 0
        self.numCuarto = 1
        self.actualizar = True
        self.costo_aux = 0
        self.estado_habitacion = 'Libre'
        self.clientes = []
        self.habitaciones = []
        self.reservaciones = []
        self.cargarDatos()
        self.ultimos_valores = {}
        self.iniciar_monitoreo_cliente()
        self.actualizarCosto()
        print(f"Estado actual al iniciar la app: {self.estadoActual}")
        self.notaClientes()
        self.notaReservaciones()
        self.notaHabitacion()

    def notaClientes(self):
        # ============================================
        # CONFIGURACIÓN DE FRAMES
        # ============================================
        frame_busqueda = ttk.Frame(self.client_frame)
        frame_datos = ttk.Frame(self.client_frame)
        frame_botones = ttk.Frame(self.client_frame)
        
        # Configuración del grid
        self.client_frame.columnconfigure(0, weight=1)
        self.client_frame.rowconfigure(0, weight=0)
        self.client_frame.rowconfigure(1, weight=1)
        self.client_frame.rowconfigure(2, weight=0)
        
        frame_busqueda.grid(row=0, column=0, sticky='ew', padx=20, pady=5)
        frame_datos.grid(row=1, column=0, sticky='nsew', padx=50, pady=15)
        frame_botones.grid(row=2, column=0, sticky='ew', padx=50, pady=15)
        
        # ============================================
        # FRAME BÚSQUEDA - WIDGETS CON PREFIJO 'cliente_'
        # ============================================
        self.cliente_label_busqueda = ttk.Label(frame_busqueda, text='Ingrese el nombre del cliente:')
        self.cliente_entry_busqueda = ttk.Entry(frame_busqueda, width=30)
        self.cliente_btn_buscar = ttk.Button(frame_busqueda, text="Buscar", width=10, command=lambda: self.buscarCliente())
        
        self.cliente_label_busqueda.grid(row=0, column=0, columnspan=3, padx=10, pady=20, sticky='e')
        self.cliente_entry_busqueda.grid(row=0, column=3, padx=10, pady=20, sticky='w')
        self.cliente_btn_buscar.grid(row=0, column=4, padx=10, pady=20, sticky='nsew')
        
        # ============================================
        # FRAME DATOS - LABELS CON PREFIJO 'cliente_'
        # ============================================
        self.cliente_label_id = tk.Label(frame_datos, text='ID:')
        self.cliente_label_nombre = tk.Label(frame_datos, text='Nombre:')
        self.cliente_label_direccion = tk.Label(frame_datos, text='Direccion:')
        self.cliente_label_telefono = tk.Label(frame_datos, text='Telefono:')
        self.cliente_label_email = tk.Label(frame_datos, text='Email:')
        
        self.cliente_label_id.grid(row=0, column=1, padx=5, pady=10, sticky='e')
        self.cliente_label_nombre.grid(row=1, column=1, padx=5, pady=10, sticky='e')
        self.cliente_label_direccion.grid(row=2, column=1, padx=5, pady=10, sticky='e')
        self.cliente_label_telefono.grid(row=3, column=1, padx=5, pady=10, sticky='e')
        self.cliente_label_email.grid(row=1, column=3, padx=10, pady=10, sticky='e')
        
        # ============================================
        # FRAME DATOS - ENTRIES CON PREFIJO 'cliente_'
        # ============================================
        self.cliente_entry_id = ttk.Entry(frame_datos, width=10)
        self.cliente_entry_nombre = ttk.Entry(frame_datos, width=30)
        self.cliente_entry_direccion = ttk.Entry(frame_datos, width=30)
        self.cliente_entry_telefono = tk.Entry(frame_datos, width=30)
        self.cliente_entry_email = ttk.Entry(frame_datos, width=30)
        
        self.cliente_entry_id.grid(row=0, column=2, padx=10, pady=10, sticky='w')
        self.cliente_entry_nombre.grid(row=1, column=2, padx=10, pady=10, sticky='w')
        self.cliente_entry_direccion.grid(row=2, column=2, padx=10, pady=10, sticky='w')
        self.cliente_entry_telefono.grid(row=3, column=2, padx=10, pady=10, sticky='w')
        self.cliente_entry_email.grid(row=1, column=4, padx=10, pady=10, sticky='w')
        
        # ============================================
        # FRAME BOTONES - BOTONES CON PREFIJO 'cliente_'
        # ============================================
        self.cliente_btn_nuevo = tk.Button(frame_botones, text="Nuevo", width=10, height=3, command=lambda: self.newcliente())
        self.cliente_btn_salvar = tk.Button(frame_botones, text="Salvar", width=10, height=3, command=lambda: self.salvarCliente())
        self.cliente_btn_cancelar = tk.Button(frame_botones, text="Cancelar", width=10, height=3, command=lambda: self.cliente_cancelar())
        self.cliente_btn_editar = tk.Button(frame_botones, text="Editar", width=10, height=3, command=lambda: self.editarCliente())
        self.cliente_btn_eliminar = tk.Button(frame_botones, text="Eliminar", width=10, height=3, command=lambda: self.eliminarCliente())
        
        self.cliente_btn_nuevo.grid(row=0, column=2, padx=10, pady=10)
        self.cliente_btn_salvar.grid(row=0, column=3, padx=10, pady=10)
        self.cliente_btn_cancelar.grid(row=0, column=4, padx=10, pady=10)
        self.cliente_btn_editar.grid(row=0, column=5, padx=10, pady=10)
        self.cliente_btn_eliminar.grid(row=0, column=6, padx=10, pady=10)

    def notaReservaciones(self):
        # ============================================
        # CONFIGURACIÓN DE FRAMES
        # ============================================
        frame_busqueda = ttk.Frame(self.reservations_frame)
        frame_datos = ttk.Frame(self.reservations_frame)
        frame_botones = ttk.Frame(self.reservations_frame)
        
        frame_busqueda.grid(row=0, column=0, sticky='ew', padx=20, pady=5)
        frame_datos.grid(row=1, column=0, sticky='nsew', padx=50, pady=10)
        frame_botones.grid(row=2, column=0, sticky='ew', padx=40, pady=10)
        
        self.reservations_frame.columnconfigure(0, weight=1)
        self.reservations_frame.rowconfigure(0, weight=0)
        self.reservations_frame.rowconfigure(1, weight=1)
        self.reservations_frame.rowconfigure(2, weight=0)
        self.reservations_frame.rowconfigure(3, weight=0)
        # ============================================
        # FRAME BÚSQUEDA - WIDGETS CON PREFIJO 'reserva_'
        # ============================================
        self.reserva_label_busqueda = ttk.Label(frame_busqueda, text='Ingrese el ID de la habitacion:')
        self.reserva_entry_busqueda = ttk.Entry(frame_busqueda, width=20)
        self.reserva_btn_buscar = ttk.Button(frame_busqueda, text="Buscar Reservacion", width=20, command=lambda: self.buscarReservacion())
        
        self.reserva_label_busqueda.grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.reserva_entry_busqueda.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        self.reserva_btn_buscar.grid(row=0, column=2, padx=10, pady=10, sticky='w')
        
        # ============================================
        # FRAME DATOS - LABELS CON PREFIJO 'reserva_'
        # ============================================
        self.reserva_label_id = tk.Label(frame_datos, text='Reservacion ID:')
        self.reserva_label_cliente_id = ttk.Label(frame_datos, text='Cliente ID:')
        self.reserva_label_habitacion_id = ttk.Label(frame_datos, text='Habitacion ID:')
        self.reserva_label_costo = ttk.Label(frame_datos, text='Costo:')
        self.reserva_label_fecha_reserva = ttk.Label(frame_datos, text='Fecha Reservacion:')
        self.reserva_label_fecha_salida = ttk.Label(frame_datos, text='Fecha Salida:')
        self.reserva_label_hora = ttk.Label(frame_datos, text='Hora Reservacion:')
        
        # ============================================
        # FRAME DATOS - ENTRIES CON PREFIJO 'reserva_'
        # ============================================
        self.reserva_entry_id = ttk.Entry(frame_datos, width=10)
        self.reserva_entry_cliente_id = ttk.Combobox(frame_datos, width=10, state='readonly')
        self.reserva_entry_habitacion_id = ttk.Combobox(frame_datos, width=10, state='readonly')
        self.reserva_entry_costo = ttk.Entry(frame_datos, width=10)
        self.reserva_entry_fecha_reserva = DateEntry(frame_datos, width=20)
        self.reserva_entry_fecha_salida = DateEntry(frame_datos, width=20)
        self.reserva_entry_hora = ttk.Entry(frame_datos, width=20)
    
        self.reserva_entry_cliente_id['values'] = [str(c.id_cliente) for c in self.clientes]
        self.reserva_entry_habitacion_id['values'] = [str(h.id_habitacion) 
                                                      for h in self.habitaciones
                                                          if h.estado == 'Libre']
        
        # Posicionar labels y entries
        self.reserva_label_id.grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.reserva_entry_id.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        
        self.reserva_label_cliente_id.grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.reserva_entry_cliente_id.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        
        self.reserva_label_habitacion_id.grid(row=2, column=0, padx=10, pady=10, sticky='e')
        self.reserva_entry_habitacion_id.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        
        self.reserva_label_costo.grid(row=3, column=0, padx=10, pady=10, sticky='e')
        self.reserva_entry_costo.grid(row=3, column=1, padx=10, pady=10, sticky='w')
        
        self.reserva_label_fecha_reserva.grid(row=0, column=2, padx=10, pady=10, sticky='e')
        self.reserva_entry_fecha_reserva.grid(row=0, column=3, padx=10, pady=10, sticky='w')
        
        self.reserva_label_fecha_salida.grid(row=1, column=2, padx=10, pady=10, sticky='e')
        self.reserva_entry_fecha_salida.grid(row=1, column=3, padx=10, pady=10, sticky='w')
        
        self.reserva_label_hora.grid(row=2, column=2, padx=10, pady=10, sticky='e')
        self.reserva_entry_hora.grid(row=2, column=3, padx=10, pady=10, sticky='w')


        # ============================================
        # FRAME BOTONES - BOTONES CON PREFIJO 'reserva_'
        # ============================================
        self.reserva_btn_nueva = tk.Button(frame_botones, text='Nueva Reservacion', width=15, height=2, command=lambda: self.nuevaReservacion())
        self.reserva_btn_reservar = tk.Button(frame_botones, text='Reservar', width=10, height=2, command=lambda: self.reservarHabitacion())
        self.reserva_btn_cancelar = tk.Button(frame_botones, text='Cancelar', width=10, height=2, command=lambda: self.reserva_cancelar())
        self.reserva_btn_editar = tk.Button(frame_botones, text='Editar', width=10, height=2, command=lambda: self.editarReservacion())
        self.reserva_btn_Eliminar = tk.Button(frame_botones, text='Eliminar', width=10, height=2, command=lambda: self.eliminarReservacion())
        
        self.reserva_btn_nueva.grid(row=0, column=1, padx=10, pady=10)
        self.reserva_btn_reservar.grid(row=0, column=2, padx=10, pady=10)
        self.reserva_btn_cancelar.grid(row=0, column=3, padx=10, pady=10)
        self.reserva_btn_editar.grid(row=0, column=4, padx=10, pady=10)
        self.reserva_btn_Eliminar.grid(row=0, column=5, padx=10, pady=10)
        
        # Configurar padding
        for widget in frame_datos.winfo_children():
            widget.grid_configure(padx=10, pady=10)
        for widget in frame_busqueda.winfo_children():
            widget.grid_configure(padx=10, pady=10)
        for widget in frame_botones.winfo_children():
            widget.grid_configure(padx=10, pady=30)

    def notaHabitacion(self):
        # ============================================
        # CONFIGURACIÓN DE FRAMES
        # ============================================
        frame_busqueda = ttk.Frame(self.rooms_frame)
        frame_datos = ttk.Frame(self.rooms_frame)
        frame_botones = ttk.Frame(self.rooms_frame)
        
        frame_busqueda.grid(row=0, column=0, sticky='ew', padx=70, pady=5)
        frame_datos.grid(row=1, column=0, sticky='nsew', padx=60, pady=10)
        frame_botones.grid(row=2, column=0, sticky='ew', padx=60, pady=20)
        
        self.rooms_frame.columnconfigure(0, weight=1)
        self.rooms_frame.rowconfigure(0, weight=0)
        self.rooms_frame.rowconfigure(1, weight=1)
        self.rooms_frame.rowconfigure(2, weight=0)
        
        # ============================================
        # FRAME BÚSQUEDA - WIDGETS CON PREFIJO 'habitacion_'
        # ============================================
        self.habitacion_label_busqueda = tk.Label(frame_busqueda, text='Ingrese Numero de Habitacion:')
        self.habitacion_entry_busqueda = ttk.Entry(frame_busqueda, width=10)
        self.habitacion_btn_buscar = ttk.Button(frame_busqueda, text='Buscar', command=lambda: self.buscarHabitacion())
        
        self.habitacion_label_busqueda.grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.habitacion_entry_busqueda.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        self.habitacion_btn_buscar.grid(row=0, column=2, padx=10, pady=10, sticky='w')
        
        # ============================================
        # FRAME DATOS - WIDGETS CON PREFIJO 'habitacion_'
        # ============================================
        self.habitacion_label_id = tk.Label(frame_datos, text='Habitacion ID:')
        self.habitacion_entry_id = ttk.Entry(frame_datos, width=10)
        
        self.habitacion_label_numero = ttk.Label(frame_datos, text='Numero:')
        self.habitacion_entry_numero = ttk.Entry(frame_datos, width=10)
        
        self.habitacion_label_estado = ttk.Label(frame_datos, text='Seleccione el estado:')
        
        self.habitacion_combo_estado = ttk.Combobox(frame_datos, state='readonly', 
                                                    values=['Libre', 'Reservado', 'Cancelado'], )
        
        # Posicionar
        self.habitacion_label_id.grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.habitacion_entry_id.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        
        self.habitacion_label_numero.grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.habitacion_entry_numero.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        
        self.habitacion_label_estado.grid(row=0, column=2, padx=10, pady=10, sticky='e')
        self.habitacion_combo_estado.grid(row=1, column=2, padx=10, pady=10, sticky='w')
        
        # ============================================
        # FRAME BOTONES - BOTONES CON PREFIJO 'habitacion_'
        # ============================================
        self.habitacion_btn_nueva = tk.Button(frame_botones, text='Nueva Habitacion', width=15, height=2, command=lambda: self.nuevaHabitacion())
        self.habitacion_btn_editar = tk.Button(frame_botones, text='Editar', width=15, height=2, command=lambda: self.editarHabitacion())
        
        
        self.habitacion_btn_nueva.grid(row=0, column=1, padx=10, pady=10)
        self.habitacion_btn_editar.grid(row=0, column=2, padx=10, pady=10)
        
        # Configurar padding
        for widget in frame_datos.winfo_children():
            widget.grid_configure(padx=10, pady=10)
        for widget in frame_busqueda.winfo_children():
            widget.grid_configure(padx=10, pady=10)
        for widget in frame_botones.winfo_children():
            widget.grid_configure(padx=10, pady=10)

    def buscarCliente(self):
        nombre_cliente = self.cliente_entry_busqueda.get().strip()
        if not nombre_cliente:
            messagebox.showerror('Error', 'Ingrese un nombre de cliente para buscar.')
            return
        
        cliente_encontrado = next((c for c in self.clientes if c.nombre == nombre_cliente), None)
        
        if cliente_encontrado:
            self.cliente_entry_id.delete(0, tk.END)
            self.cliente_entry_nombre.delete(0, tk.END)
            self.cliente_entry_direccion.delete(0, tk.END)
            self.cliente_entry_telefono.delete(0, tk.END)
            self.cliente_entry_email.delete(0, tk.END)

            self.cliente_entry_id.insert(0, str(cliente_encontrado.id_cliente))
            self.cliente_entry_nombre.insert(0, cliente_encontrado.nombre)
            self.cliente_entry_direccion.insert(0, cliente_encontrado.direccion)
            self.cliente_entry_telefono.insert(0, cliente_encontrado.telefono)
            self.cliente_entry_email.insert(0, cliente_encontrado.correo)

            self.cliente_entry_id.config(state='disabled')
            self.cliente_entry_nombre.config(state='disabled')
            self.cliente_entry_direccion.config(state='disabled')
            self.cliente_entry_telefono.config(state='disabled')
            self.cliente_entry_email.config(state='disabled')
            self.cliente_btn_salvar.config(state='disabled')
        else:
            messagebox.showinfo('No Encontrado', f'No se encontró un cliente con nombre {nombre_cliente}.')
    def newcliente(self):
        print(f"Entrando a la funcion Estado: {self.estadoActual}")
        try:
            print(f"Estado actual al entra al try newcliente: {self.estadoActual}")
            # Si hay datos sin guardar, preguntar
            if self.estadoActual == self.ESTADO_SINGUARDAR:
                print(f"Consultando estado actual: {self.estadoActual}")
                if messagebox.askyesno('Nuevo Cliente', '¿Descartar cambios?'):
                    self.deleteEntryClient()
                    self.cliente_entry_id.delete(0, tk.END)
                    self.cliente_entry_nombre.delete(0, tk.END)
                    self.estadoActual = self.ESTADO_VACIO
                    print(f"Dentro del messagebox Estado: {self.estadoActual}")
                else:
                    return
            
            # Si está en edición, no permitir
            elif self.estadoActual == self.ESTADO_EDITANDO:
                messagebox.showwarning('Error', 'Termina la edición primero')
                return
            print(f"Estado actual final: {self.estadoActual}")
            # Limpiar y preparar nuevo cliente
            self.deleteEntryClient()
            self.id_cliente += 1

            self.cliente_entry_id.delete(0, tk.END)
            self.cliente_entry_id.insert(0, str(self.id_cliente))
            self.cliente_entry_nombre.focus()
            self.estadoActual = self.ESTADO_VACIO
            print(f"Estado actual al final newcliente: {self.estadoActual}")
            
        except Exception as e:
            messagebox.showerror('Error', str(e))
    def salvarCliente(self):
        try:
            id_cliente = self.cliente_entry_id.get().strip()
            nombre = self.cliente_entry_nombre.get().strip()
            correo = self.cliente_entry_email.get().strip()
            direccion = self.cliente_entry_direccion.get().strip()
            telefono = self.cliente_entry_telefono.get().strip()

            if not id_cliente or not nombre or not correo or not telefono or not direccion:
                messagebox.showerror('Error', 'ID, Nombre, Correo, Teléfono y Dirección son obligatorios.')
                return False
            try:
                id_cliente_int = int(id_cliente)
            except ValueError:
                messagebox.showerror('Error', 'ID del cliente debe ser un número entero.')
                return False
            
            # Crear directorio Data en el mismo lugar que el script
            import os
            ruta_script = os.path.dirname(os.path.abspath(__file__))
            ruta_data = os.path.join(ruta_script, "Data")
            
            if not os.path.exists(ruta_data):
                os.makedirs(ruta_data)
            print(f'Id del cliente: {id_cliente})')
            ruta_archivo = os.path.join(ruta_data, "clientes.txt")
            print(f"Estado actual en salvarCliente: {self.estadoActual}")
            if self.estadoActual == self.ESTADO_EDITANDO:
                print(f"Editando cliente ID {id_cliente}")
                cliente_encontrado = None
                for cliente in self.clientes:
                    if cliente.id_cliente == id_cliente_int:
                        cliente.nombre = nombre
                        cliente.direccion = direccion
                        cliente.correo = correo
                        cliente.telefono = telefono
                        cliente_encontrado = cliente
                        break
                if not cliente_encontrado:
                    messagebox.showerror('Error', 'Cliente no encontrado para editar.')
                    return
                with open(ruta_archivo, 'w', encoding='utf-8') as f:
                    for cliente in self.clientes:
                        f.write(f"{cliente.id_cliente}|{cliente.nombre}|{cliente.direccion}|{cliente.correo}|{cliente.telefono}\n")

            else:
                print(f"Guardando nuevo cliente ID {id_cliente}")
                for cliente in self.clientes:
                    if cliente.id_cliente == id_cliente_int:
                        messagebox.showerror('Error', 'Ya existe un cliente con ese ID.')
                        return
                nuevo_cliente = Cliente(id_cliente, nombre, direccion, correo, telefono)
                self.clientes.append(nuevo_cliente)
                with open(ruta_archivo, 'a', encoding='utf-8') as f:
                    f.write(f"{id_cliente}|{nombre}|{direccion}|{correo}|{telefono}\n")
                messagebox.showinfo('Éxito', f'Cliente {nombre} guardado correctamente.')
                self.estadoActual = self.ESTADO_GUARDADO
                print(f"Estado actual al final salvarCliente: {self.estadoActual}")
            self.estadoActual = self.ESTADO_GUARDADO
            self.actualizarComboClienteId()
            print(f"Estado actual al editar cliente: {self.estadoActual}")
                
        except Exception as e:
            messagebox.showerror('Error', f'Error al guardar: {str(e)}')
            import traceback
            traceback.print_exc()

    def editarCliente(self):
        try:
            if self.estadoActual == self.ESTADO_EDITANDO:
                messagebox.showwarning('Error', 'Ya estás editando este cliente')
                return
            
            id_cliente = self.cliente_entry_id.get().strip()
            if not id_cliente:
                messagebox.showerror('Error', 'No hay cliente seleccionado para editar.')
                return
            
            self.estadoActual = self.ESTADO_EDITANDO
            self.cliente_btn_salvar.config(state='normal')
            self.cliente_entry_nombre.config(state='normal')
            self.cliente_entry_direccion.config(state='normal')
            self.cliente_entry_telefono.config(state='normal')
            self.cliente_entry_email.config(state='normal')
            self.cliente_entry_id.config(state='disabled')
            self.cliente_entry_nombre.focus()
            print(f"Estado actual al iniciar edición: {self.estadoActual}")
        except Exception as e:
            messagebox.showerror('Error', f'Error al iniciar edición: {str(e)}')

    def cliente_cancelar(self):
        self.cliente_entry_busqueda.delete(0, tk.END)
        self.cliente_entry_id.config(state='normal')
        self.cliente_entry_nombre.config(state='normal')
        self.cliente_entry_direccion.config(state='normal')
        self.cliente_entry_telefono.config(state='normal')
        self.cliente_entry_email.config(state='normal')
        self.cliente_btn_salvar.config(state='normal')
        if self.estadoActual in [self.ESTADO_EDITANDO, self.ESTADO_SINGUARDAR]:
            if messagebox.askyesno('Cancelar', '¿Deseas cancelar los cambios?'):
                self.deleteEntryClient()
                self.estadoActual = self.ESTADO_VACIO
                print(f"Estado actual al cancelar: {self.estadoActual}")    
        else:
            self.deleteEntryClient()

    def eliminarCliente(self):
        self.cliente_entry_id.config(state='normal')
        id_cliente = self.cliente_entry_id.get().strip()
        self.cliente_entry_id.config(state='disabled')
        if not id_cliente:
            messagebox.showerror('Error', 'No hay cliente seleccionado para eliminar.')
            return
        for reservacion in self.reservaciones:
            print(f"Revisando reservacion ID {reservacion.id_reservacion} para cliente ID {reservacion.clienteID}")
            if reservacion.clienteID == int(id_cliente):
                print(f"Cliente ID {id_cliente} tiene reservacion ID {reservacion.id_reservacion}")
                messagebox.showerror('Error', 'No se puede eliminar el cliente porque tiene reservaciones activas.')
                return
        if messagebox.askyesno('Eliminar Cliente', f'¿Estás seguro de eliminar el cliente con ID {id_cliente}?'):
            # Aquí podrías implementar la lógica para eliminar el cliente del archivo o base de datos
            self.deleteEntryClient()
            self.estadoActual = self.ESTADO_VACIO
            print(f"Estado actual al eliminar cliente: {self.estadoActual}")
            self.clientes = [c for c in self.clientes if c.id_cliente != id_cliente]  # Eliminar de la lista en memoria
            messagebox.showinfo('Cliente Eliminado', f'Cliente con ID {id_cliente} ha sido eliminado.')
    
    ########################################### LOGICA PARA RESERVACIONES ############################################
    def buscarReservacion(self):
        self.reserva_entry_id.config(state='normal')
        self.reserva_entry_cliente_id.config(state='normal')
        self.reserva_entry_habitacion_id.config(state='normal')
        self.reserva_entry_fecha_reserva.config(state='normal')
        self.reserva_entry_fecha_salida.config(state='normal')
        self.reserva_entry_hora.config(state='normal')
        self.reserva_entry_id.delete(0, tk.END)
        self.reserva_entry_cliente_id.delete(0, tk.END)
        self.reserva_entry_habitacion_id.delete(0, tk.END)
        self.reserva_entry_fecha_reserva.delete(0, tk.END)
        self.reserva_entry_fecha_salida.delete(0, tk.END)
        self.reserva_entry_hora.delete(0, tk.END)
        self.reserva_entry_costo.delete(0, tk.END)
        try:
            nombre_cliente = self.reserva_entry_busqueda.get().strip()
            if not nombre_cliente:
                messagebox.showerror('Error', 'Ingrese un nombre de cliente para buscar.')
                return
            id_cliente = None
            for cliente in self.clientes:
                if cliente.nombre == nombre_cliente:
                    id_cliente = cliente.id_cliente
                    break
            if id_cliente is None:
                messagebox.showinfo('No Encontrado', f'No se encontró un cliente con nombre {nombre_cliente}.')
                return
            reservacion_encontrada = next((r for r in self.reservaciones if r.clienteID == id_cliente), None)
            if reservacion_encontrada:  
                self.reserva_entry_id.delete(0, tk.END)
                self.reserva_entry_id.insert(0, str(reservacion_encontrada.id_reservacion))
                self.reserva_entry_cliente_id.delete(0, tk.END)
                self.reserva_entry_cliente_id.insert(0, str(reservacion_encontrada.clienteID))
                self.reserva_entry_habitacion_id.delete(0, tk.END)
                self.reserva_entry_habitacion_id.insert(0, str(reservacion_encontrada.id_habitacion))
                self.reserva_entry_fecha_reserva.set_date(reservacion_encontrada.fecha_reservacion)
                self.reserva_entry_fecha_salida.set_date(reservacion_encontrada.fecha_salida)
                self.reserva_entry_hora.delete(0, tk.END)
                self.reserva_entry_hora.insert(0, str(reservacion_encontrada.hora_reserva))
                self.reserva_entry_costo.delete(0, tk.END)
                self.reserva_entry_costo.insert(0, str(reservacion_encontrada.costo))
                self.reserva_entry_id.config(state='disabled')
                self.reserva_entry_cliente_id.config(state='disabled')
                self.reserva_entry_habitacion_id.config(state='disabled')
                self.reserva_entry_fecha_reserva.config(state='disabled')
                self.reserva_entry_fecha_salida.config(state='disabled')
                self.reserva_entry_hora.config(state='disabled')
                self.reserva_entry_costo.config(state='disabled')
                self.reserva_btn_reservar.config(state='disabled')
                self.estadoActual = self.ESTADO_GUARDADO
                print(f"Estado actual al cargar reservacion: {self.estadoActual}")
        except Exception as e:
            messagebox.showerror('Error', f'Error al buscar reservación: {str(e)}')

    def nuevaReservacion(self):
        try:
            self.reserva_entry_id.config(state='normal')
            self.reserva_entry_id.delete(0,tk.END)
            self.id_reservacion = len(self.reservaciones) + 1
            self.reserva_entry_id.insert(0, str(self.id_reservacion))
            self.reserva_entry_id.config(state='disabled')
            self.actualizar_habitaciones_libres()
            self.habilitar_campos_reservacion()
            self.reserva_entry_cliente_id.delete(0, tk.END)
            self.reserva_entry_habitacion_id.delete(0, tk.END)
            self.reserva_entry_hora.delete(0, tk.END)
            self.reserva_entry_costo.delete(0, tk.END)
            self.reserva_entry_cliente_id.focus()

        except Exception as e:
            messagebox.showerror('Error', f'Error al crear reservación: {str(e)}')
    def editarReservacion(self):
        self.reserva_entry_cliente_id.config(state='normal')
        self.reserva_entry_habitacion_id.config(state='normal')
        self.reserva_entry_fecha_reserva.config(state='normal')
        self.reserva_entry_fecha_salida.config(state='normal')
        self.reserva_entry_hora.config(state='normal')
        self.reserva_entry_costo.config(state='normal')
        self.reserva_btn_reservar.config(state='normal')
        self.estadoActual = self.ESTADO_EDITANDO
        print(f"Estado actual al editar reservacion: {self.estadoActual}")
        

    def reservarHabitacion(self):
        try:
            id_reservacion = self.reserva_entry_id.get().strip()
            cliente_id = self.reserva_entry_cliente_id.get().strip()
            habitacion_id = self.reserva_entry_habitacion_id.get().strip()
            fecha_reserva = self.reserva_entry_fecha_reserva.get_date()
            fecha_salida = self.reserva_entry_fecha_salida.get_date()
            hora = self.reserva_entry_hora.get().strip()
            costo = self.costo_aux
            fecha_reserva_str = fecha_reserva.strftime('%m/%d/%Y')
            fecha_salida_str = fecha_salida.strftime('%m/%d/%Y')
            if not all([id_reservacion, cliente_id, habitacion_id, fecha_reserva_str, fecha_salida_str, hora]):
                messagebox.showerror('Error', 'Todos los campos son obligatorios para reservar una habitación.')
                return
            
            habitacion = self.buscar_habitacion_por_id(habitacion_id)
            if not habitacion:
                messagebox.showerror('Error', 'Habitación no encontrada.')
                return
            
            if habitacion.estado != 'Libre' and self.estadoActual != self.ESTADO_EDITANDO:
                messagebox.showerror('Error', 'La habitación seleccionada no está disponible.')
                return
            
            if fecha_salida <= fecha_reserva:
                messagebox.showerror('Error', 'La fecha de salida debe ser posterior a la fecha de reservación.')
                return
            
            habitacion_encontrada = None
            for habitacion in self.habitaciones:
                if str(habitacion.id_habitacion) == habitacion_id:
                    habitacion_encontrada = habitacion
                    if habitacion.estado != 'Libre' and self.estadoActual != self.ESTADO_EDITANDO:
                        messagebox.showerror('Error', 'La habitación seleccionada no está disponible.')
                        self.estadoActual = self.ESTADO_VACIO
                        print(f"Estado actual al intentar reservar habitacion no disponible: {self.estadoActual}")
                        return
                    break

            if self.estadoActual == self.ESTADO_EDITANDO:
                for reservacion in self.reservaciones:
                    if str(reservacion.id_reservacion) == id_reservacion:
                        reservacion.clienteID = int(cliente_id)
                        reservacion.id_habitacion = int(habitacion_id)
                        reservacion.fecha_reservacion = fecha_reserva
                        reservacion.fecha_salida = fecha_salida
                        reservacion.hora_reserva = hora
                        reservacion.costo = costo
                        self.estadoActual = self.ESTADO_GUARDADO
                        print(f"Estado actual al guardar edición de reservacion: {self.estadoActual}")
                        break
            else:  
                nueva_reservacion = Reservacion(id_reservacion, cliente_id, habitacion_id, costo, fecha_reserva_str, fecha_salida_str, hora)
                self.reservaciones.append(nueva_reservacion)
                habitacion_encontrada.estado = 'Reservado'  # Actualizar estado en memoria
                with open("src/Data/reservaciones.txt", 'a', encoding='utf-8') as f:
                    f.write(f"{id_reservacion}|{cliente_id}|{habitacion_id}|{costo}|{fecha_reserva_str}|{fecha_salida_str}|{hora}\n")
                self.guardar_habitaciones()  # Guardar cambios en habitaciones para reflejar la nueva reserva
                self.actualizar_habitaciones_libres()  # Actualizar la lista de habitaciones libres en el combo
                self.bloquear_campos_reservacion()  # Bloquear campos después de reservar

            self.estadoActual = self.ESTADO_GUARDADO
            print(f"Estado actual al guardar reservacion: {self.estadoActual}")
            
            # Aquí podrías agregar lógica para guardar la reservación en un archivo o base de datos
            with open("src/Data/habitaciones.txt", 'r', encoding='utf-8') as f:
                lineas = f.readlines()
            with open("src/Data/habitaciones.txt", 'w', encoding='utf-8') as f:
                for linea in lineas:
                    datos = linea.strip().split('|')
                    if datos[0] == habitacion_id:
                        f.write(f"{datos[0]}|{datos[1]}|Reservado\n")
                    else:
                        f.write(linea)

            messagebox.showinfo('Éxito', f'Reservación {id_reservacion} creada correctamente.')
            self.reserva_entry_id.config(state='disabled')
            self.reserva_entry_cliente_id.config(state='disabled')
            self.reserva_entry_habitacion_id.config(state='disabled')
            self.reserva_entry_fecha_reserva.config(state='disabled')
            self.reserva_entry_fecha_salida.config(state='disabled')
            self.reserva_entry_hora.config(state='disabled')
            self.reserva_entry_costo.config(state='disabled')
        except Exception as e:
            messagebox.showerror('Error', f'Error al crear reservación: {str(e)}')

    def actualizarCosto(self):
        self.calculaCosto()
        self.after(1000, self.actualizarCosto)  # Actualiza cada segundo para reflejar cambios en fechas o habitación
    def calculaCosto(self):

        if not hasattr(self, 'reserva_entry_fecha_reserva') or not hasattr(self, 'reserva_entry_fecha_salida') or not hasattr(self, 'reserva_entry_habitacion_id'):
            return  # Asegura que los widgets existan antes de intentar acceder a ellos
        fecha_reserva = self.reserva_entry_fecha_reserva.get_date()
        fecha_salida = self.reserva_entry_fecha_salida.get_date()
        habitacion_id = self.reserva_entry_habitacion_id.get().strip()
        if not habitacion_id:
            return
        precio_por_noche = 100

        dias = (fecha_salida - fecha_reserva).days
        costo_total = dias * float(precio_por_noche)
        self.reserva_entry_costo.delete(0, tk.END)
        self.reserva_entry_costo.insert(0, str(costo_total))
        self.costo_aux = costo_total
    
    def reserva_cancelar(self):
        self.reserva_entry_busqueda.delete(0, tk.END)
        self.reserva_entry_id.config(state='normal')
        self.reserva_entry_cliente_id.config(state='normal')
        self.reserva_entry_habitacion_id.config(state='normal')
        self.reserva_entry_fecha_reserva.config(state='normal')
        self.reserva_entry_fecha_salida.config(state='normal')
        self.reserva_entry_hora.config(state='normal')
        self.reserva_entry_costo.config(state='normal')

        if self.estadoActual in [self.ESTADO_EDITANDO, self.ESTADO_SINGUARDAR]:
            if messagebox.askyesno('Cancelar', '¿Deseas cancelar los cambios?'):
                self.reserva_entry_id.delete(0, tk.END)
                self.reserva_entry_cliente_id.delete(0, tk.END)
                self.reserva_entry_habitacion_id.delete(0, tk.END)
                self.reserva_entry_fecha_reserva.delete(0, tk.END)
                self.reserva_entry_fecha_salida.delete(0, tk.END)
                self.reserva_entry_hora.delete(0, tk.END)
                self.reserva_entry_costo.delete(0, tk.END)
                self.estadoActual = self.ESTADO_VACIO
                print(f"Estado actual al cancelar reservacion: {self.estadoActual}")
        else:
            self.reserva_entry_id.delete(0, tk.END)
            self.reserva_entry_cliente_id.delete(0, tk.END)
            self.reserva_entry_habitacion_id.delete(0, tk.END)
            self.reserva_entry_fecha_reserva.delete(0, tk.END)
            self.reserva_entry_fecha_salida.delete(0, tk.END)
            self.reserva_entry_hora.delete(0, tk.END)
            self.reserva_entry_costo.delete(0, tk.END)
            self.estadoActual = self.ESTADO_VACIO
            print(f"Estado actual al cancelar reservacion sin confirmar: {self.estadoActual}")

    def eliminarReservacion(self):
        self.reserva_entry_id.config(state='normal')
        self.reserva_entry_cliente_id.config(state='normal')
        self.reserva_entry_habitacion_id.config(state='normal')
        self.reserva_entry_fecha_reserva.config(state='normal')
        self.reserva_entry_fecha_salida.config(state='normal')
        self.reserva_entry_hora.config(state='normal')
        self.reserva_entry_costo.config(state='normal')
        id_reservacion = self.reserva_entry_id.get().strip()

        for reservacion in self.reservaciones:
            if str(reservacion.id_reservacion) == id_reservacion:
                habitacion_id = reservacion.id_habitacion
                for habitacion in self.habitaciones:
                    if str(habitacion.id_habitacion) == str(habitacion_id):
                        habitacion.estado = 'Libre'
                        break
                self.guardar_habitaciones()  # Guardar cambios en habitaciones para reflejar la liberación de la habitación
                break

        if not id_reservacion:
            messagebox.showerror('Error', 'No se ha seleccionado una reservación para eliminar.')
            return

        if messagebox.askyesno('Confirmar Eliminación', f'¿Estás seguro de que deseas eliminar la reservación con ID: {id_reservacion}?'):
            # Eliminar del archivo de datos
            ruta_archivo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "reservaciones.txt")
            try:
                with open(ruta_archivo, 'r', encoding='utf-8') as f:
                    lineas = f.readlines()
                
                with open(ruta_archivo, 'w', encoding='utf-8') as f:
                    for linea in lineas:
                        if not linea.startswith(f"{id_reservacion}|"):
                            f.write(linea)
                
                # Limpiar los campos de entrada
                self.reserva_entry_id.delete(0, tk.END)
                self.reserva_entry_cliente_id.delete(0, tk.END)
                self.reserva_entry_habitacion_id.delete(0, tk.END)
                self.reserva_entry_fecha_reserva.delete(0, tk.END)
                self.reserva_entry_fecha_salida.delete(0, tk.END)
                self.reserva_entry_hora.delete(0, tk.END)
                self.reserva_entry_costo.delete(0, tk.END)

                messagebox.showinfo('Éxito', f'Reservación con ID {id_reservacion} eliminada correctamente.')
            except Exception as e:
                messagebox.showerror('Error', f'Error al eliminar la reservación: {str(e)}')

############################################## LOGICA PARA HABITACIONES ############################################

    def nuevaHabitacion(self):
        self.habitacion_entry_numero.config(state='normal')
        self.habitacion_combo_estado.config(state='readonly')
        self.habitacion_entry_id.config(state='normal')
        print(f"Estado actual al iniciar nueva habitacion: {self.estadoActual}")
        try:
            self.id_habitacion = self.habitacion_entry_id.get().strip()
            numero = self.habitacion_entry_numero.get().strip()
            estado = self.habitacion_combo_estado.get().strip()

            if not self.id_habitacion or not numero or not estado:
                messagebox.showerror('Error', 'Todos los campos son obligatorios para crear una habitación.')
                return
            
            nueva_habitacion = Room(self.id_habitacion, numero, estado)
            
            self.habitaciones.append(nueva_habitacion)
            ruta_archivo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "habitaciones.txt")
            with open(ruta_archivo, 'a', encoding='utf-8') as f:
                f.write(f"{self.id_habitacion}|{numero}|{estado}\n")
                print(f"Habitación {numero} guardada en archivo.")
            self.actualizarComboHabitacionId()  # Actualizar combo de habitaciones en reservaciones
            messagebox.showinfo('Éxito', f'Habitación {numero} creada correctamente.')
            self.habitacion_entry_id.delete(0, tk.END)
            self.habitacion_entry_numero.delete(0, tk.END)
            self.habitacion_combo_estado.set('')
            self.estadoActual = self.ESTADO_GUARDADO
            print(f"Estado actual al finalizar nueva habitacion: {self.estadoActual}")
        
        except Exception as e:
            messagebox.showerror('Error', f'Error al crear habitación: {str(e)}')

    def buscarHabitacion(self):
        numero = self.habitacion_entry_busqueda.get().strip()
        try:
            if not numero:
                messagebox.showerror('Error', 'Ingrese un número de habitación para buscar.')
                return
            
            habitacion_encontrada = None
            for habitacion in self.habitaciones:
                if habitacion.numero == numero:
                    habitacion_encontrada = habitacion
                    break
            self.estadoActual = self.ESTADO_GUARDADO
            print(f"Estado actual al buscar habitacion: {self.estadoActual}")
            
            if habitacion_encontrada:
                self.habitacion_entry_id.delete(0, tk.END)
                self.habitacion_entry_numero.delete(0, tk.END)
                self.habitacion_combo_estado.set('')
                
                self.habitacion_entry_id.insert(0, str(habitacion_encontrada.id_habitacion))
                self.habitacion_entry_numero.insert(0, habitacion_encontrada.numero)
                self.habitacion_combo_estado.set(habitacion_encontrada.estado)

                self.habitacion_entry_id.config(state='disabled')
                self.habitacion_entry_numero.config(state='disabled')
                self.habitacion_combo_estado.config(state='disabled')
            else:
                messagebox.showinfo('No Encontrado', f'No se encontró una habitación con número {numero}.')
        except Exception as e:
                messagebox.showerror('Error', f'Error al buscar habitación: {str(e)}')
    def editarHabitacion(self):
        self.estadoActual = self.ESTADO_EDITANDO
        print(f"Estado actual al iniciar edición de habitacion: {self.estadoActual}")
        self.habitacion_combo_estado.config(state='readonly')
        self.habitacion_combo_estado.focus()
        self.habitacion_combo_estado.bind("<<ComboboxSelected>>", self.actualizarEstadoHabitacion)
        



############################################## FUNCIONES AUXILIARES ##############################################
    def actualizarComboClienteId(self):
        if hasattr(self, 'reserva_entry_cliente_id'):
            valores = [str(cliente.id_cliente) for cliente in self.clientes]
            self.reserva_entry_cliente_id['values'] = valores

    def actualizarComboHabitacionId(self):
        if hasattr(self, 'reserva_entry_habitacion_id'):
            valores = [str(habitacion.id_habitacion) for habitacion in self.habitaciones]
            self.reserva_entry_habitacion_id['values'] = valores

        self.after(100, lambda: print(f"Estado actualizado: {self.estadoActual}"))
        print(f"Estado actualizado: {self.estadoActual}")
    def actualizarEstadoHabitacion(self, event=None):

        habitacion_id = self.habitacion_entry_id.get().strip()
        nuevo_estado = self.habitacion_combo_estado.get().strip()
        for habitacion in self.habitaciones:
            if str(habitacion.id_habitacion) == habitacion_id:
                habitacion.estado = nuevo_estado
                break
        self.habitaciones = [h for h in self.habitaciones if str(h.id_habitacion) != habitacion_id] + [habitacion]  # Actualizar lista en memoria
        self.guardar_habitaciones()  # Guardar cambios en el archivo

    def habilitar_campos_reservacion(self):
        self.reserva_entry_cliente_id.config(state='normal')
        self.reserva_entry_habitacion_id.config(state='normal')
        self.reserva_entry_fecha_reserva.config(state='normal')
        self.reserva_entry_fecha_salida.config(state='normal')
        self.reserva_entry_hora.config(state='normal')
        # El costo podría ser calculado automáticamente
        self.reserva_entry_costo.config(state='normal')

    def bloquear_campos_reservacion(self):
        self.reserva_entry_cliente_id.config(state='disabled')
        self.reserva_entry_habitacion_id.config(state='disabled')
        self.reserva_entry_fecha_reserva.config(state='disabled')
        self.reserva_entry_fecha_salida.config(state='disabled')
        self.reserva_entry_hora.config(state='disabled')
        self.reserva_entry_costo.config(state='disabled')
        # El ID puede quedar visible pero no editable
        self.reserva_entry_id.config(state='disabled')
    
    def actualizar_habitaciones_libres(self):
        if hasattr(self, 'reserva_entry_habitacion_id'):
            habitaciones_libres = [str(h.id_habitacion) for h in self.habitaciones if h.estado == 'Libre']
            self.reserva_entry_habitacion_id['values'] = habitaciones_libres

    def buscar_cliente_por_id(self, id_cliente):
        for cliente in self.clientes:
            if str(cliente.id_cliente) == str(id_cliente):
                return cliente
        return None

    def buscar_habitacion_por_id(self, id_habitacion):
        for habitacion in self.habitaciones:
            if str(habitacion.id_habitacion) == str(id_habitacion):
                return habitacion
        return None
    
    def buscar_reservacion_por_id(self, id_reservacion):
        for reservacion in self.reservaciones:
            if str(reservacion.id_reservacion) == str(id_reservacion):
                return reservacion
        return None
    
    def get_reservaciones_ativas(self):
        from datetime import datetime
        hoy = datetime.now().date()
        reservaciones_activas = [r for r in self.reservaciones if r.fecha_salida >= hoy]
        return reservaciones_activas
    
    def guardar_datos(self):
        self.guardar_clientes()
        self.guardar_habitaciones()
        self.guardar_reservaciones()
        print('Datos guardados')
    def guardar_habitaciones(self):
        with open("src/Data/habitaciones.txt", 'w', encoding='utf-8') as f:
            for habitacion in self.habitaciones:
                f.write(f"{habitacion.id_habitacion}|{habitacion.numero}|{habitacion.estado}\n")

    
    def guardar_reservaciones(self):
        with open("src/Data/reservaciones.txt", 'w', encoding='utf-8') as f:
            for reservacion in self.reservaciones:
                f.write(f"{reservacion.id_reservacion}|{reservacion.clienteID}|{reservacion.id_habitacion}|{reservacion.costo}|{reservacion.fecha_reservacion}|{reservacion.fecha_salida}|{reservacion.hora_reserva}\n")

    def iniciar_monitoreo_cliente(self):
        """Inicia un monitoreo periódico de los campos"""
        self.monitorear_campos_cliente()
        
    def monitorear_campos_cliente(self):
        """Verifica cambios cada 500ms"""
        try:
            valores_actuales = {
                'id': self.cliente_entry_id.get(),
                'nombre': self.cliente_entry_nombre.get(),
                'direccion': self.cliente_entry_direccion.get(),
                'telefono': self.cliente_entry_telefono.get(),
                'email': self.cliente_entry_email.get()
            }
            
            # Si hay cambios, actualizar estado
            if valores_actuales != self.ultimos_valores:
                self.ultimos_valores = valores_actuales.copy()
                self.actualizarEstadoCliente()
                
        except Exception as e:
            print(f"Error en monitoreo: {e}")
        
        # Programar siguiente verificación
        self.after(500, self.monitorear_campos_cliente)
    def actualizarEstadoCliente(self):
        id_cliente = self.cliente_entry_id.get()
        nombre = self.cliente_entry_nombre.get()
        direccion = self.cliente_entry_direccion.get()
        telefono = self.cliente_entry_telefono.get()
        email = self.cliente_entry_email.get()
        if id_cliente and nombre and direccion and telefono and email:
            if self.estadoActual == self.ESTADO_EDITANDO:
                self.estadoActual = self.ESTADO_EDITANDO
                print(f"Dentro de actualizarEstadoCliente Estado: {self.estadoActual}")
            else:
                self.estadoActual = self.ESTADO_VACIO
                print(f"Dentro de actualizarEstadoCliente Estado: {self.estadoActual}")
        else:
            self.estadoActual = self.ESTADO_SINGUARDAR
            print(f"Dentro de actualizarEstadoCliente Estado: {self.estadoActual}")

    def cargarDatos(self):
        archivo_cliente = Archivo("src/Data/clientes.txt")
        archivo_habitacion = Archivo("src/Data/habitaciones.txt")
        archivo_reservacion = Archivo("src/Data/reservaciones.txt")
        import os
        if os.path.exists("src/Data/clientes.txt"):
            print("Archivo de clientes encontrado, cargando datos...")
        else:          print("Archivo de clientes no encontrado, se creará uno nuevo al guardar.")
        self.clientes = archivo_cliente.cargar_datos_cliente()
        self.habitaciones = archivo_habitacion.cargar_datos_habitacion()
        self.reservaciones = archivo_reservacion.cargar_datos_reservacion()
        self.id_cliente = max((c.id_cliente for c in self.clientes), default=0)  # Actualizar ID para nuevos clientes
        self.id_habitacion = max((h.id_habitacion for h in self.habitaciones), default=0)  # Actualizar ID para nuevas habitaciones
        
        print(f"Clientes cargados: {len(self.clientes)}, Habitaciones cargadas: {len(self.habitaciones)}, Reservaciones cargadas: {len(self.reservaciones)}")
        for i in self.clientes:
            print(f"[{i.id_cliente}, {i.nombre}, {i.direccion}, {i.correo}, {i.telefono}]")
        print("===========================================")
        for i in self.habitaciones:
            print(f"[{i.id_habitacion}, {i.numero}, {i.estado}]")
        print("===========================================")
        for i in self.reservaciones:
            print(f"[{i.id_reservacion}, {i.clienteID}, {i.id_habitacion}, {i.costo}, {i.fecha_reservacion}, {i.fecha_salida}, {i.hora_reserva}]")

    def sincronizarDatos(self):
        # Aquí podrías implementar la lógica para sincronizar los datos con un servidor o base de datos
        for habitacion in self.habitaciones:
            habitacion.estado = 'Libre'  # Ejemplo: marcar todas las habitaciones como libres al sincronizar

        from datetime import datetime
        hoy = datetime.now().date()
        for reservacion in self.reservaciones:
            if reservacion.fecha_salida >= hoy:
                reservacion.habitacion.ocupar()

        print('Estados sincronizados.')

    def deleteEntryClient(self):
        self.cliente_entry_busqueda.config(state='normal')
        self.cliente_entry_id.config(state='normal')
        self.cliente_entry_nombre.config(state='normal')
        self.cliente_entry_direccion.config(state='normal')
        self.cliente_entry_telefono.config(state='normal')
        self.cliente_entry_email.config(state='normal')
        self.cliente_entry_id.delete(0, tk.END)
        self.cliente_entry_nombre.delete(0, tk.END)
        self.cliente_entry_busqueda.delete(0, tk.END)
        self.cliente_entry_direccion.delete(0, tk.END)
        self.cliente_entry_telefono.delete(0, tk.END)
        self.cliente_entry_email.delete(0, tk.END)




if __name__ == "__main__":
    app = App()
    
    app.mainloop()