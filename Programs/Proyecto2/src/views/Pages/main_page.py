import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import font
class MainPage(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.frameMain = Frame(master)
        self.frameMain.place(relx=0.5, rely=0.5, anchor="center")
        self.labelInicio = ttk.Label(self.frameMain, text="TALLER MECANICO", font=font.Font(size=20, family="sans-serif"))
        self.labelInicio.pack()