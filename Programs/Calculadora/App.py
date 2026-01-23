import tkinter as tk
from tkinter import END, messagebox, ttk
import Calculadora as calc

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.config(width=600, height=400)
        self.title("Calculadora")
        self.display = tk.Entry(self, width=50)
        self.display.place(x=5, y=5)
        self.button1 = tk.Button(self, text="1", command=lambda:self.button_1())
        self.button2 = tk.Button(self, text="2", command=lambda:self.button_2())
        self.button3 = tk.Button(self, text="3", command=lambda:self.button_3())
        self.button4 = tk.Button(self, text="4", command=lambda:self.button_4())
        self.button5 = tk.Button(self, text="5", command=lambda:self.button_5())
        self.button6 = tk.Button(self, text="6", command=lambda:self.button_6())
        self.button7 = tk.Button(self, text="7", command=lambda:self.button_7())
        self.button8 = tk.Button(self, text="8", command=lambda:self.button_8())
        self.button9 = tk.Button(self, text="9", command=lambda:self.button_9())
        self.button0 = tk.Button(self, text="0", command=lambda:self.button_0())
        self.button4 = tk.Button(self, text="4", command=lambda:self.button_4())
        self.buttonSuma = tk.Button(self, text="+", command=lambda:self.button_suma())
        self.buttonResta = tk.Button(self, text="-", command=lambda:self.button_resta())
        self.buttonMultiplicacion = tk.Button(self, text="*", command=lambda:self.button_multiplicacion())
        self.buttonDivision = tk.Button(self, text="/", command=lambda:self.button_division())
        self.buttonIgual = tk.Button(self, text="=", command=lambda:self.button_igual())
        self.buttonClear = tk.Button(self, text="CR", command=lambda:self.button_clear())
        self.button1.place(x=20, y=50)
        self.button2.place(x=80, y=50)
        self.button3.place(x=140, y=50)
        self.button4.place(x=20, y=90)
        self.button5.place(x=80, y=90)
        self.button6.place(x=140, y=90)
        self.button7.place(x=20, y=130)
        self.button8.place(x=80, y=130)
        self.button9.place(x=140, y=130)
        self.button0.place(x=80, y=170)
        self.buttonSuma.place(x=200, y=50)
        self.buttonResta.place(x=140, y=170)
        self.buttonMultiplicacion.place(x=200, y=130)
        self.buttonDivision.place(x=200, y=90)
        self.buttonIgual.place(x=200, y=170)
        self.buttonClear.place(x=20, y=170)
        
        self.numero_aux = 0
        self.operador = ''

    def button_1(self):
        self.display.config(state='normal')
        self.display.insert(0, "1")
        self.display.config(state='disabled')

    def button_2(self):
        self.display.config(state='normal')
        self.display.insert(0, "2")
        self.display.config(state='disabled')

    def button_3(self):
        self.display.config(state='normal')
        self.display.insert(0, "3")
        self.display.config(state='disabled')   

    def button_4(self):
        self.display.config(state='normal')
        self.display.insert(0, "4")
        self.display.config(state='disabled')   

    def button_5(self):
        self.display.config(state='normal')
        self.display.insert(0, "5")
        self.display.config(state='disabled')   
    
    def button_6(self):
        self.display.config(state='normal')
        self.display.insert(0, "6")
        self.display.config(state='disabled')

    def button_7(self):
        self.display.config(state='normal')
        self.display.insert(0, "7")
        self.display.config(state='disabled')

    def button_8(self):
        self.display.config(state='normal')
        self.display.insert(0, "8")
        self.display.config(state='disabled')   

    def button_9(self):
        self.display.config(state='normal')
        self.display.insert(0, "9")
        self.display.config(state='disabled')

    def button_0(self):
        self.display.config(state='normal')
        self.display.insert(0, "0")
        self.display.config(state='disabled')



    def button_suma(self):
        self.display.config(state='normal')
        self.numero_aux = int(self.display.get())
        self.display.delete(0, END)
        self.display.config(state='disabled')
        self.operando = '+'

    def button_resta(self):
        self.display.config(state='normal')
        self.numero_aux = int(self.display.get())
        self.display.delete(0, END)
        self.display.config(state='disabled')
        self.operando = '-'

    def button_multiplicacion(self):
        self.display.config(state='normal')
        self.numero_aux = int(self.display.get())
        self.display.delete(0, END)
        self.display.config(state='disabled')
        self.operando = '*'

    def button_division(self):
        self.display.config(state='normal')
        self.numero_aux = int(self.display.get())
        self.display.delete(0, END)
        self.display.config(state='disabled')
        self.operando = '/'


    def button_igual(self):
        self.ob = calc.Calculadora()
        self.ob.operacion(self.numero_aux, int(self.display.get()), self.operando)
        self.display.config(state='normal')
        self.display.delete(0, END)
        self.display.insert(0, str(self.ob.getResultado()))
        self.display.config(state='disabled')

    def button_clear(self):
        self.ob = calc.Calculadora()
        self.ob.clear()
        self.display.config(state='normal')
        self.display.delete(0, END)
        self.display.insert(0, str(self.ob.getResultado()))
        self.display.config(state='disabled')

if __name__=="__main__":
    app=App()
    app.mainloop()