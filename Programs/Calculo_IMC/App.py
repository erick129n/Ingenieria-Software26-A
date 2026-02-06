import tkinter as tk
from tkinter import ttk
import tkinter.font as font
from tkcalendar import DateEntry # type: ignore
import os
from tkinter import messagebox
import Persona


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
        self.label_talla = tk.Label(self, text="Talla")
        self.label_mts = tk.Label(self, text="(mts)")
        self.entry_nombre = tk.Entry(self)
        self.entry_direccion = tk.Entry(self)
        self.entry_telefono = tk.Entry(self)
        self.genero = tk.StringVar()
        self.entry_genero = ttk.Combobox(self, textvariable=self.genero)
        self.entry_genero["values"] = ['Masculino', 'Femenino', 'No binario']
        self.entry_nacimiento = DateEntry(self, width=12)
        self.entry_talla = tk.Entry(self)


        self.button_Nuevo = tk.Button(self, text='Nuevo')
        self.button_Guardar = tk.Button(self, text='Guardar')
        self.button_Cancelar = tk.Button(self, text='Cancelar')
        self.button_cargar = tk.Button(self, text='Cargar Clientes', command=lambda: self.cargar_clientes())
        self.button_verIMC = tk.Button(self, text='Ver IMC', command=lambda: self.ver_imc())


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

        self.label_talla.grid(row=5, column=0)
        self.entry_talla.grid(row=5, column=1)
        self.label_mts.grid(row=5, column=2, sticky='w')

        # Buttons
        self.button_Nuevo.grid(row=6, column=0, pady=20)
        self.button_Guardar.grid(row=6, column=1, pady=20)
        self.button_Cancelar.grid(row=6, column=2, pady=20)
        self.button_cargar.grid(row=7, column=0, pady=10)
        self.button_verIMC.grid(row=7, column=1, pady=10)

        def ver_imc():
            try:
                talla = float(self.entry_talla.get())
                imc = 25 / (talla ** 2)  # Ejemplo de cálculo de IMC
                tk.messagebox.showinfo("IMC", f"Tu IMC es: {imc:.2f}")
            except ValueError:
                tk.messagebox.showerror("Error", "Por favor, ingresa una talla válida.")
#ver que pedo con estas lineas de codigo. No tengo ni la menor idea de que hacen, 
# pero se que son importantes para cargar los clientes guardados en el txt
        def cargar_clientes():
            clientes = []
            if os.path.exists("clientes.txt"):
                with open("clientes.txt", 'r') as archivo:
                    for linea in archivo:
                        datos = linea.strip().split(',')
                        if len(datos) == 7:
                            cliente = Persona.Cliente(*datos)
                            clientes.append(cliente)
            return clientes
if __name__ == "__main__":
    app = App()
    app.mainloop()