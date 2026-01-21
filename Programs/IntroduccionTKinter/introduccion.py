import tkinter as tk
from tkinter import END, messagebox, ttk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.id=0
        self.nombre=''
        self.direccion=''
        self.telefono=''
        self.config(width=600, height=400)
        self.title("Practica 1")
        self.label_nombre = ttk.Label(self, text="Nombre")
        self.label_nombre.place(x=10, y=20)
        self.entry_nombre = tk.Entry(self, width=20)
        self.entry_nombre.place(x=100, y=20)
        self.label_direccion = ttk.Label(self, text="Direccion")
        self.label_direccion.place(x=10, y=50)
        self.entry_direccion = tk.Entry(self, width=20)
        self.entry_direccion.place(x=100, y=50)
        self.label_telefono = ttk.Label(self, text="Telefono")
        self.label_telefono.place(x=10, y= 80)
        self.entry_telefono = tk.Entry(self, width=20)
        self.entry_telefono.place(x= 100,  y=80)
        self.button_mostrar = tk.Button(self, text="Mostar", command=lambda:self.mostrar())
        self.button_mostrar.place(x=100, y=150)

    
    def mostrar(self):
        nombre=self.entry_nombre.get()
        direccion = self.entry_direccion.get()
        telefono = self.entry_telefono.get()
        id = str(self.id + 1)
        salida='Hola ' + nombre + '\n' + 'Direccion: ' + direccion + '\n' + 'Telefono: ' + telefono + '\n' + 'ID: ' + id
        messagebox.showinfo(title='Datos', message=salida)
        

if __name__=="__main__":
    app=App()
    app.mainloop()