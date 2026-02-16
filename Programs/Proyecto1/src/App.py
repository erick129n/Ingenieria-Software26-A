import tkinter as tk
from tkinter import ttk
import tkcalendar as tkcal
from tkcalendar import DateEntry
from tkinter import messagebox

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

        self.notaClientes()
        self.notaReservaciones()
        self.notaHabitacion()


    def notaClientes(self):
        #configure grid
        #configure rows
        #configuracion de los frames

        frame_busqueda = ttk.Frame(self.client_frame)
        frame_datos = ttk.Frame(self.client_frame)
        frame_botones = ttk.Frame(self.client_frame)

        ###################################configuracion del frame de clientes###########################
        self.client_frame.columnconfigure(0, weight=0, uniform='columns')
        self.client_frame.rowconfigure(1, weight=1, uniform='rows')
        self.client_frame.columnconfigure(2, weight=0, uniform='columns')

        frame_busqueda.grid(row=0, column=0, sticky='ew', padx=20, pady=5)
        frame_datos.grid(row=1, column=0, padx=50, pady=15, sticky='nsew')
        frame_botones.grid(row=2, column=0, sticky='nsew',padx=50, pady=15)

        ############################configuracion de los elementos de frame_busqueda####################
        labelNombreCliente = ttk.Label(frame_busqueda, text='Ingrese el nombre del cliente:')
        searchButton = tk.Button(frame_busqueda, text="Buscar", width=10) # asignarle funcion
        entry_nombreCliente = ttk.Entry(frame_busqueda, width=30)

        entry_nombreCliente.grid(row=0, column=3, padx=10, pady=20, sticky='w')

        labelNombreCliente.grid(row=0, column=0, columnspan=3,padx=10, pady=20, sticky='e')
        searchButton.grid(row=0, column=4, padx=10, pady=20, sticky='nsew', )

        ##########################################configuracion de los frame_datos#######################
        labelID = tk.Label(frame_datos, text='ID:')
        labelNombreToEntry = tk.Label(frame_datos, text='Nombre:')
        labelDireccion = tk.Label(frame_datos, text='Direccion:')
        labelTelefono = tk.Label(frame_datos, text='Telefono:')
        labelEmail = tk.Label(frame_datos, text='Email:')

        labelID.grid(row=0, column=1, padx=0, pady=0, sticky='e')
        labelNombreToEntry.grid(row=1, column=1, padx=0, pady=0, sticky='e')
        labelDireccion.grid(row=2, column=1, padx=0, pady=0, sticky='e')
        labelTelefono.grid(row=3, column=1, padx=0, pady=0, sticky='e')
        labelEmail.grid(row=1, column=3, padx=10, pady=10, sticky='e')

        #entrys de clientes
        entry_ID = ttk.Entry(frame_datos, width=10)
        entry_nombreToEntry = ttk.Entry(frame_datos, width=30)
        entry_direccion = ttk.Entry(frame_datos, width=30)
        entry_telefono = tk.Spinbox(frame_datos, width=30)
        entry_email = ttk.Entry(frame_datos, width=30)

        #posiciones de los entrys

        entry_ID.grid(row=0, column=2, padx=10, pady=10, sticky='w')
        entry_nombreToEntry.grid(row=1, column=2, padx=10, pady=10,sticky='w')
        entry_direccion.grid(row=2, column=2, padx=10, pady=10, sticky='w')
        entry_telefono.grid(row=3, column=2, padx=10, pady=10, sticky='w')
        entry_email.grid(row=1, column=4, padx=10, pady=10, sticky='w')

        ####################################botones de clientes de frame_botones######################
        buttonNewClient = tk.Button(frame_botones, text="Nuevo", width=10, height=3) #asignarle la funcion de nuevo cliente
        buttonSaveClient = tk.Button(frame_botones, text="Salvar", width=10, height=3)
        buttonCancelClient = tk.Button(frame_botones, text="Cancelar", width=10, height=3)
        buttonEditClient = tk.Button(frame_botones, text="Editar", width=10, height=3)
        buttonDeleteClient = tk.Button(frame_botones, text="Eliminar", width=10, height=3)
        #posiciones de los botones

        buttonNewClient.grid(row=0, column=2, padx=10, pady=10)
        buttonSaveClient.grid(row=0, column=3, padx=10, pady=10, sticky='w')
        buttonCancelClient.grid(row=0, column=4, padx=10, pady=10, sticky='w')
        buttonEditClient.grid(row=0, column=5, padx=10, pady=10, sticky='w')
        buttonDeleteClient.grid(row=0, column=6, padx=10, pady=10,sticky='nsew')

    def notaReservaciones(self):
        #######################configuracion de los frames################
        frame_busqueda = ttk.Frame(self.reservations_frame)
        frame_datos = ttk.Frame(self.reservations_frame)
        frame_botones = ttk.Frame(self.reservations_frame)

        frame_busqueda.grid(row=0, column=0, sticky='ew')
        frame_datos.grid(row=1, column=0, sticky='nsew')
        frame_botones.grid(row=2, column=0, sticky='nsew')

        self.reservations_frame.columnconfigure(0, weight=0, uniform='columns')
        self.reservations_frame.rowconfigure(1, weight=1, uniform='rows')
        self.reservations_frame.columnconfigure(2, weight=0, uniform='rows')

        ######################## configuracion frame busqueda #############
        labelIdReservacion = ttk.Label(frame_busqueda, text='Ingrese el ID de la habitacion:')
        entryIDReservacion = ttk.Entry(frame_busqueda, width=30)
        buttonBuscar = ttk.Button(frame_busqueda, text="Buscar Reservacion", width=20)

        labelIdReservacion.grid(row=0, column=0)
        entryIDReservacion.grid(row=0, column=1)
        buttonBuscar.grid(row=0, column=2)

        ##################### configuracion de frame de datos ###########

        labelID = tk.Label(frame_datos, text='Reservacion ID:')
        labelID_Cliente = ttk.Label(frame_datos, text='Cliente ID:')
        labelID_habitacion = ttk.Label(frame_datos, text='Habitacion ID:')
        label_costo = ttk.Label(frame_datos, text='Costo:')
        label_fecha_reservacion = ttk.Label(frame_datos, text='Fecha Reservacion:')
        label_fecha_salida = ttk.Label(frame_datos, text='Fecha Salida:')
        label_hora_reservacion = ttk.Label(frame_datos, text='Hora Reservacion:')

        entry_ID = ttk.Entry(frame_datos, width=10)
        entry_ID_Cliente = ttk.Entry(frame_datos, width=30)
        entry_ID_habitacion = ttk.Entry(frame_datos, width=30)
        entry_costo = ttk.Entry(frame_datos, width=20)
        entry_fecha_reservacion = ttk.Entry(frame_datos, width=30)
        entry_fecha_salida = ttk.Entry(frame_datos, width=30)
        entry_hora_reservacion = ttk.Entry(frame_datos, width=30)

        labelID.grid(row=0, column=0,sticky='e')
        entry_ID.grid(row=0, column=1, sticky='w')

        labelID_Cliente.grid(row=1, column=0, sticky='e')
        entry_ID_Cliente.grid(row=1, column=1, sticky='w')

        labelID_habitacion.grid(row=2, column=0, sticky='e')
        entry_ID_habitacion.grid(row=2, column=1, sticky='w')

        label_costo.grid(row=3, column=0, sticky='e')
        entry_costo.grid(row=3, column=1,sticky='w')

        label_fecha_reservacion.grid(row=0, column=2, sticky='e')
        entry_fecha_reservacion.grid(row=0, column=3,sticky='w')

        label_fecha_salida.grid(row=1, column=2, sticky='e')
        entry_fecha_salida.grid(row=1, column=3, sticky='w')

        label_hora_reservacion.grid(row=1, column=2, sticky='e')
        entry_hora_reservacion.grid(row=1, column=3,sticky='w')

    ########################## Configuracion de los botones ##############
        buttonNewReservation = ttk.Button(frame_botones, text='Nueva Reservacion')
        buttonReservate = ttk.Button(frame_botones, text='Reservar')
        buttonCancelReservation = ttk.Button(frame_botones, text='Cancelar Reservacion')
        buttonEditReservation = ttk.Button(frame_botones, text='Editar')

        buttonNewReservation.grid(row=0, column=1)
        buttonReservate.grid(row=0, column=2)
        buttonCancelReservation.grid(row=0, column=3)
        buttonEditReservation.grid(row=0, column=4)

        for widget in frame_datos.winfo_children():
            widget.grid_configure(padx=10, pady=10)

    def notaHabitacion(self):
        #configuracion de los frames
        frame_busqueda = ttk.Frame(self.rooms_frame)
        frame_datos = ttk.Frame(self.rooms_frame)
        frame_botones = ttk.Frame(self.rooms_frame)

        frame_busqueda.grid(row=0, column=0,sticky='ew')
        frame_datos.grid(row=1, column=0,sticky='nsew')
        frame_botones.grid(row=2, column=0,sticky='ew')

        self.rooms_frame.columnconfigure(0, weight=0, uniform='columns')
        self.rooms_frame.rowconfigure(1, weight=1, uniform='rows')
        self.rooms_frame.columnconfigure(2, weight=0, uniform='columns')

        ################# configuracion de busqueda ####################
        labelNumberRoom = tk.Label(frame_busqueda, text='Ingrese Numero de Habitacion:')
        entryNumberRoom = ttk.Entry(frame_busqueda, width=10)
        buttonBusqueda = ttk.Button(frame_busqueda, text='Buscar')

        labelNumberRoom.grid(row=0, column=0,sticky='e')
        entryNumberRoom.grid(row=0, column=1,sticky='w')
        buttonBusqueda.grid(row=0, column=2,sticky='w')

        ########################### configuraicon de datos #################
        labelIdRoom = tk.Label(frame_datos, text='Habitacion ID:')
        entryIdRoom = ttk.Entry(frame_datos, width=10)
        labelNumeroRoom = ttk.Label(frame_datos, text='Numero:')
        entryNumeroRoom = ttk.Entry(frame_datos, width=10)
        labelStateRoom = ttk.Label(frame_datos, text='Seleccione el estado de la habitacion:')
        comboStateRoom = ttk.Combobox(frame_datos, state='readonly', values=['Libre', 'Reservado', 'Cancelado'])

        labelIdRoom.grid(row=0, column=0,sticky='e')
        entryIdRoom.grid(row=0, column=1,sticky='w')

        labelNumeroRoom.grid(row=1, column=0,sticky='e')
        entryNumeroRoom.grid(row=1, column=1,sticky='w')

        labelStateRoom.grid(row=0, column=2,sticky='e')
        comboStateRoom.grid(row=1, column=2,sticky='w')

        ############################ configuracion botones ################
        buttonNewRoom = ttk.Button(frame_botones, text='Nueva Habitacion')
        buttonEditRoom = ttk.Button(frame_botones, text='Editar')

        buttonNewRoom.grid(row=0, column=1)
        buttonEditRoom.grid(row=0, column=2)

        for widget in frame_datos.winfo_children():
            widget.grid_configure(padx=10, pady=10)



if __name__ == "__main__":
    app = App()
    app.mainloop()