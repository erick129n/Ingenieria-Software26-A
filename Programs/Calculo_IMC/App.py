import tkinter as tk
from tkinter import ttk
import tkinter.font as font
from tkcalendar import DateEntry # type: ignore
import os
from tkinter import messagebox
import Persona
import Archivos


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculador de IMC")
        self.frame = tk.Frame(self, borderwidth=5, width=400, height=450)
        self.geometry("400x450")
        self.frame.grid(row=0, column=0, columnspan=4, rowspan=10)
        self.label_nombre = tk.Label(self, text="Nombre")
        self.label_direccion = tk.Label(self, text="Direccion")
        self.label_telefono = tk.Label(self, text="Telefono")
        self.label_genero = tk.Label(self, text="Genero")
        self.label_nacimiento = tk.Label(self, text="Fecha Nacimiento")
        self.label_altura = tk.Label(self, text="Altura")
        self.label_mts = tk.Label(self, text="(mts)")
        self.label_peso = tk.Label(self, text="Peso")
        self.label_kgs = tk.Label(self, text="Kgs")
        self.entry_nombre = tk.Entry(self)
        self.entry_direccion = tk.Entry(self)
        self.entry_telefono = tk.Entry(self)
        self.genero = tk.StringVar()
        self.entry_genero = ttk.Combobox(self, textvariable=self.genero)
        self.entry_genero["values"] = ['Masculino', 'Femenino', 'No binario']
        self.entry_nacimiento = DateEntry(self, width=12)
        self.entry_altura = tk.Entry(self)
        self.entry_peso = tk.Entry(self)

        self.button_Nuevo = tk.Button(self, text='Nuevo', command=lambda: nuevo(self))
        self.button_Guardar = tk.Button(self, text='Guardar', command=lambda: guardar_cliente(self))
        self.button_Cancelar = tk.Button(self, text='Cancelar', command=lambda:cancelar(self))
        self.button_cargar = tk.Button(self, text='Cargar Clientes', command=lambda: cargar_cliente(self))
        self.button_verIMC = tk.Button(self, text='Ver IMC', command=lambda: ver_imc(self))


        self.label_nombre.grid(row=0, column=0)
        self.entry_nombre.grid(row=0, column=1)

        self.label_direccion.grid(row=1, column=0)
        self.entry_direccion.grid(row=1, column=1)

        self.label_telefono.grid(row=2, column=0)
        self.entry_telefono.grid(row=2, column=1)

        self.label_genero.grid(row=3, column=0)
        self.entry_genero.grid(row=3, column=1)

        self.label_nacimiento.grid(row=4, column=0)
        self.entry_nacimiento.grid(row=4, column=1)

        self.label_altura.grid(row=5, column=0)
        self.entry_altura.grid(row=5, column=1)
        self.label_mts.grid(row=5, column=2, sticky='w')

        self.label_peso.grid(row=6, column=0)
        self.entry_peso.grid(row=6, column=1)
        self.label_kgs.grid(row=6, column=2, sticky='w')

        # Buttons
        self.button_Nuevo.grid(row=7, column=0, pady=20)
        self.button_Guardar.grid(row=7, column=1, pady=20)
        self.button_Cancelar.grid(row=7, column=2, pady=20)
        self.button_cargar.grid(row=8, column=0, pady=10)
        self.button_verIMC.grid(row=8, column=1, pady=10)

        self.imc = 0
        self.archivo = Archivos.Archivo("clientes.txt")
        self.cliente = Persona.Cliente
        self.id = -1
        self.cliente_guardado = False
        self.actualizar = True
        self.iniciar_actualizacion()
        def cancelar(self):
            try:
                result = tk.messagebox.askquestion('Advertencia', 'Estas seguro de eliminar estos datos?', )
                if result == 'yes':
                    self.entry_nombre.delete(0, tk.END)
                    self.entry_direccion.delete(0, tk.END)
                    self.entry_telefono.delete(0, tk.END)
                    self.entry_genero.delete(0, tk.END)
                    self.entry_nacimiento.delete(0, tk.END)
                    self.entry_altura.delete(0, tk.END)
                    self.entry_peso.delete(0, tk.END)
                else:
                    return
            except ValueError:
                tk.messagebox.showerror('Error', 'No se pudieron eliminar los datos.')
        def ver_imc(self):
            self.ventana = tk.Toplevel()
            self.ventana.title('IMC')
            self.frame_imc = tk.Frame(self.ventana)
            self.frame_imc.grid(row=0, column=0)
            self.label_show_imc = tk.Label(self.ventana, text='IMC:')
            self.label_show_imc.grid(row=9, column=1)
            try:
                self.show_resultado_imc = tk.Label(self.ventana, text=f'{self.imc:.2f}Kg/m^2')

                self.labl_id = tk.Label(self.ventana, text=f'ID: {self.cliente.id}')
                self.labl_nombre = tk.Label(self.ventana, text=f'Nombre: {self.cliente.nombre}')
                self.labl_direccion = tk.Label(self.ventana, text=f'Direccion: {self.cliente.direccion}')
                self.labl_telefono = tk.Label(self.ventana, text=f'Telefono: {self.cliente.telefono}')
                self.labl_genero = tk.Label(self.ventana, text=f'Genero: {self.cliente.genero}')
                self.labl_nacimiento = tk.Label(self.ventana, text=f'Nacimiento: {self.cliente.nacimiento}')
                self.labl_altura = tk.Label(self.ventana, text=f'Altura: {self.cliente.estatura}')
                self.labl_peso = tk.Label(self.ventana, text=f'Peso: {self.cliente.peso}')
                self.pgb_imc = ttk.Progressbar(self.ventana, orient='horizontal', length=200, mode='determinate', maximum=40, value=self.imc)
                if self.imc <= 18:
                     self.pgb_imc.config(style='red.Horizontal.TProgressbar')
                elif 18 > self.imc <= 24:
                    self.pgb_imc.config(style='green.Horizontal.TProgressbar')
                elif 24 > self.imc <= 29:
                    self.pgb_imc.config(style='yellow.Horizontal.TProgressbar')
                elif 29 > self.imc <=39:
                    self.pgb_imc.config(style='orange.Horizontal.TProgressbar')
                else:
                    self.pgb_imc.config(style='red.Horizontal.TProgressbar')

                estado = ''
                if(self.cliente.imc <= 18):
                    estado = 'infrapeso'
                elif 18 < self.cliente.imc <= 24:
                    estado = 'Normal'
                elif 24 < self.cliente.imc <= 29:
                    estado = 'Sobrepeso'
                elif 29 < self.cliente.imc <=39:
                    estado = 'Obesidad'
                else:
                    estado = 'Obesidad extrema'

                self.label_estado_nutricion = tk.Label(self.ventana, text=f'Tu estado de nutricion es de: {estado}')

                self.labl_id.grid(row=0, column=1)
                self.show_resultado_imc.grid(row=1, column=1)
                self.labl_nombre.grid(row=2, column=1)
                self.labl_direccion.grid(row=3, column=1)
                self.labl_telefono.grid(row=4, column=1)
                self.labl_genero.grid(row=5, column=1)
                self.labl_nacimiento.grid(row=6, column=1)
                self.labl_altura.grid(row=7, column=1)
                self.labl_peso.grid(row=8, column=1)
                self.show_resultado_imc.grid(row=9, column=2)
                self.label_estado_nutricion.grid(row=10, column=1)
                self.pgb_imc.grid(row=11, column=1, pady=10)
            except ValueError:
                tk.messagebox.showerror("Error", "Por favor, ingresa una medida válida.")
        def nuevo(self):
            self.id = self.id+1
            self.cliente.id =self.id
            self.cliente.nombre = ''
            self.cliente.direccion = ''
            self.cliente.telefono = ''
            self.cliente.genero = ''
            self.cliente.nacimiento = ''
            self.cliente.estatura = 0
            self.cliente.peso = 0
            self.entry_nombre.delete(0, tk.END)
            self.entry_direccion.delete(0, tk.END)
            self.entry_telefono.delete(0, tk.END)
            self.entry_genero.delete(0, tk.END)
            self.entry_nacimiento.delete(0, tk.END)
            self.entry_altura.delete(0, tk.END)
            self.entry_peso.delete(0, tk.END)

        def guardar_cliente(self):
            self.actualizar = False
            try:
                self.archivo.guardar_cliente(self.cliente)
                print("Archivo guardado correctamente")
            except ValueError:
                print("Archivo no guardado")
            self.actualizar = True


        def cargar_cliente(self):
            clientes = []
            ventana_clientes = tk.Toplevel()
            ventana_clientes.title('Clientes')
            ventana_clientes.geometry("1000x600")  # Ventana más grande
            ventana_clientes.minsize(800, 400)  # Tamaño mínimo

            # Configurar grid para que se expanda
            ventana_clientes.grid_rowconfigure(1, weight=1)
            ventana_clientes.grid_columnconfigure(0, weight=1)

            # Frame para los botones
            frame_botones = tk.Frame(ventana_clientes)
            frame_botones.grid(row=0, column=0, sticky='ew', padx=5, pady=5)

            buton_close = tk.Button(frame_botones, text='Cerrar', command=ventana_clientes.destroy)
            buton_close.pack(side='left', padx=5)

            buton_seleccionar = tk.Button(frame_botones, text='Seleccionar', command=lambda:seleccionar())
            buton_seleccionar.pack(side='left', padx=5)

            # Frame para la tabla con scrollbars
            frame_tabla = tk.Frame(ventana_clientes)
            frame_tabla.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
            frame_tabla.grid_rowconfigure(0, weight=1)
            frame_tabla.grid_columnconfigure(0, weight=1)

            # Scrollbars
            scrollbar_y = ttk.Scrollbar(frame_tabla, orient='vertical')
            scrollbar_x = ttk.Scrollbar(frame_tabla, orient='horizontal')

            # Configurar la tabla
            table = ttk.Treeview(
                frame_tabla,
                yscrollcommand=scrollbar_y.set,
                xscrollcommand=scrollbar_x.set,
                show='headings'  # Oculta la columna #0 que no usamos
            )

            # Definir columnas
            columns = ['id', 'Nombre', 'Direccion', 'Telefono', 'Genero', 'Nacimiento', 'Altura', 'Peso', 'IMC']
            table['columns'] = columns

            # Configurar encabezados
            for col in columns:
                table.heading(col, text=col)
                # Anchos iniciales
                if col == 'id':
                    table.column(col, width=50, minwidth=50, stretch=False)
                elif col == 'Nombre':
                    table.column(col, width=150, minwidth=100, stretch=True)
                elif col == 'Direccion':
                    table.column(col, width=200, minwidth=150, stretch=True)
                elif col == 'Telefono':
                    table.column(col, width=100, minwidth=80, stretch=False)
                elif col == 'Genero':
                    table.column(col, width=80, minwidth=60, stretch=False)
                elif col == 'Nacimiento':
                    table.column(col, width=100, minwidth=80, stretch=False)
                elif col == 'Altura':
                    table.column(col, width=80, minwidth=60, stretch=False)
                elif col == 'Peso':
                    table.column(col, width=80, minwidth=60, stretch=False)
                elif col == 'IMC':
                    table.column(col, width=80, minwidth=60, stretch=False)

            # Configurar scrollbars
            scrollbar_y.config(command=table.yview)
            scrollbar_x.config(command=table.xview)

            # Posicionar elementos
            table.grid(row=0, column=0, sticky='nsew')
            scrollbar_y.grid(row=0, column=1, sticky='ns')
            scrollbar_x.grid(row=1, column=0, sticky='ew')

            # Configurar tags para filas
            table.tag_configure('oddrow', background='#f0f0f0')
            table.tag_configure('evenrow', background='#e0e0e0')
            def seleccionar():
                valores = []
                seleccionado = table.focus()
                valores = table.item(seleccionado, 'values')
                self.cliente.id = int(valores[0])
                self.cliente.nombre = valores[1]
                self.cliente.direccion = valores[2]
                self.cliente.telefono = valores[3]
                self.cliente.genero = valores[4]
                self.cliente.nacimiento = valores[5]
                self.cliente.estatura = valores[6]
                self.cliente.peso = valores[7]
                self.cliente.imc = valores[8]
                mostrar()
            def mostrar():
                self.entry_nombre.delete(0, 'end')
                self.entry_direccion.delete(0, 'end')
                self.entry_telefono.delete(0, 'end')
                self.entry_genero.delete(0, 'end')
                self.entry_nacimiento.delete(0, 'end')
                self.entry_altura.delete(0, 'end')
                self.entry_peso.delete(0, 'end')
                ventana_clientes.destroy()
                self.entry_nombre.insert(0, self.cliente.nombre)
                self.entry_direccion.insert(0, self.cliente.direccion)
                self.entry_telefono.insert(0, self.cliente.telefono)
                self.entry_genero.insert(0, self.cliente.genero)
                self.entry_nacimiento.insert(0, self.cliente.nacimiento)
                self.entry_altura.insert(0, self.cliente.estatura)
                self.entry_peso.insert(0, self.cliente.peso)
            try:
                if os.path.exists("clientes.txt"):
                    clientes = self.archivo.cargar_clientes()
                    print(f'Archivo cargado correctamente. {len(clientes)} clientes encontrados.')

                    # Insertar datos en la tabla
                    for idx, cliente in enumerate(clientes):
                        # Crear una lista con los valores del cliente
                        # Asumiendo que cliente es un objeto con atributos
                        values = [
                            getattr(cliente, 'id', ''),
                            getattr(cliente, 'nombre', ''),
                            getattr(cliente, 'direccion', ''),
                            getattr(cliente, 'telefono', ''),
                            getattr(cliente, 'genero', ''),
                            getattr(cliente, 'nacimiento', ''),
                            getattr(cliente, 'estatura', ''),
                            getattr(cliente, 'peso', ''),
                            getattr(cliente, 'imc', '')
                        ]

                        # Alternar colores de fila
                        tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                        table.insert(
                            parent='',
                            index='end',
                            values=values,
                            tags=(tag,)
                        )

                    # Ejecutar ajuste después de insertar datos
                    ventana_clientes.after(100)

                else:
                    tk.messagebox.showwarning("Advertencia", "No hay registro de clientes.")

            except Exception as e:
                tk.messagebox.showerror("Error", f"Fallo la extracción de los clientes: {str(e)}")
                print(f"Error: {e}")

            # Hacer que la tabla se expanda con la ventana
            def on_window_resize(event):
                # Actualizar el área de visualización
                table.update_idletasks()

            ventana_clientes.bind('<Configure>', on_window_resize)

    def refresh_data(self):
        if not self.actualizar:
            return

        self.cliente.id = self.id
        self.cliente.nombre = self.entry_nombre.get()
        self.cliente.direccion = self.entry_direccion.get()
        self.cliente.telefono = self.entry_telefono.get()
        self.cliente.genero = self.entry_genero.get()
        self.cliente.nacimiento = self.entry_nacimiento.get()
        try:
            self.cliente.estatura = float(self.entry_altura.get())
        except:
            self.cliente.estatura = 0
        try:
            self.cliente.peso = float(self.entry_peso.get())
        except:
            self.cliente.peso = 0
        try:
            self.imc = self.cliente.peso / (self.cliente.estatura ** 2)
            self.cliente.imc = float(round(self.imc, 2))
        except:
            self.imc = 0
            self.cliente.imc = round(self.imc, 2)
        if self.actualizar:
            self.after(1000, self.refresh_data)

    def iniciar_actualizacion(self):
        self.actualizar = True
        self.refresh_data()
if __name__ == "__main__":
    app = App()
    clientes = app.archivo.cargar_clientes()
    for cliente in clientes:
        app.id = int(cliente.id)
    app.id = int(app.id +1)
    print(app.id)
    app.mainloop()