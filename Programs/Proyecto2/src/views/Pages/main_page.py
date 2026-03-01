import tkinter as tk
from tkinter import *
from tkinter import ttk

class MainPage(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.labelBienvenida = ttk.Label(master, text="Bienvenido")
        self.labelBienvenida.pack()