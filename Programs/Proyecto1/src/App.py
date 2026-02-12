import tkinter as tk
from tkinter import ttk
import tkcalendar as tkcal
from tkcalendar import DateEntry
from tkinter import messagebox

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Reservaciones')
        self.geometry('600x400')
        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True)
        self.reservations_frame = ttk.Frame(notebook) #es la hija de la padre notebook, es decir, el contenedor de las reservaciones
        notebook.add(ttk.Frame(notebook), text='Clientes')
        notebook.add(self.reservations_frame, text='Reservaciones')
        notebook.add(ttk.Frame(notebook), text='Habitaciones')

        label_nombre = ttk.Label(self.reservations_frame, text='Nombre del cliente:')
        label_nombre.grid(row=0, column=0, padx=10, pady=10)


if __name__ == "__main__":
    app = App()
    app.mainloop()