import tkinter as tk
from tkinter import END, messagebox, ttk
import Calculadora as calc
import tkinter.font as font
import conversiones as conv

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora")
        self.fuenteDisplay = tk.font.Font(family="Arial", size=16)
        self.fuente = tk.font.Font(family="Arial", size=14)
        self.frame = tk.Frame(self, borderwidth=5, width=400, height=450)
        self.geometry('400x525')
        self.frame.grid(row=0, column=0, columnspan=5, rowspan=11)
        self.display = tk.Entry(self, font=self.fuenteDisplay, justify='right')
        # campos de conversión
        self.buttonHex = tk.Button(self, text="Hex:", background='lightgray', font= tk.font.Font(family='Arial', size=10), command=
                                    lambda: self.button_Hexa())
        self.buttonDec = tk.Button(self, text="Dec:", background='lightgray', font= tk.font.Font(family='Arial', size=10),
                                    command=lambda: self.button_Decimal())
        self.buttonOct = tk.Button(self, text="Oct:", background='lightgray', font= tk.font.Font(family='Arial', size=10),
                                    command=lambda: self.button_Octal())
        self.buttonBin = tk.Button(self, text="Bin:", background='lightgray', font= tk.font.Font(family='Arial', size=10),
                                    command=lambda: self.button_Binario())

        # Ubicación de los campos de conversión
        self.buttonHex.grid(row=1, column=0, padx=8, pady=8, sticky='w')
        self.buttonDec.grid(row=2, column=0, padx=8, pady=8, sticky='w')
        self.buttonOct.grid(row=3, column=0, padx=8, pady=8, sticky='w')
        self.buttonBin.grid(row=4, column=0, padx=8, pady=8, sticky='w')

        # Campos de conversión
        self.displayHex = tk.Entry(self, font=self.fuente, justify='right')
        self.displayDec = tk.Entry(self, font=self.fuente, justify='right')
        self.displayOct = tk.Entry(self, font=self.fuente, justify='right')
        self.displayBin = tk.Entry(self, font=self.fuente, justify='right')

        # Ubicación de los campos de conversión
        self.display.grid(row=0, column=0, columnspan=5, rowspan=1, padx=10, pady=10, sticky='nswe')
        self.displayHex.grid(row=1, column=1, columnspan=4, rowspan=1, sticky='nswe')
        self.displayDec.grid(row=2, column=1, columnspan=4, rowspan=1, sticky='nswe')
        self.displayOct.grid(row=3, column=1, columnspan=4, rowspan=1, sticky='nswe')
        self.displayBin.grid(row=4, column=1, columnspan=4, rowspan=1, sticky='nswe')

        #botones numeros
        self.button1 = tk.Button(self, text="1", font=self.fuente, command=lambda:self.button_1())
        self.button2 = tk.Button(self, text="2", font=self.fuente, command=lambda:self.button_2())
        self.button3 = tk.Button(self, text="3", font=self.fuente, command=lambda:self.button_3())
        self.button4 = tk.Button(self, text="4", font=self.fuente, command=lambda:self.button_4())
        self.button5 = tk.Button(self, text="5", font=self.fuente, command=lambda:self.button_5())
        self.button6 = tk.Button(self, text="6", font=self.fuente, command=lambda:self.button_6())
        self.button7 = tk.Button(self, text="7", font=self.fuente, command=lambda:self.button_7())
        self.button8 = tk.Button(self, text="8", font=self.fuente, command=lambda:self.button_8())
        self.button9 = tk.Button(self, text="9", font=self.fuente, command=lambda:self.button_9())
        self.button0 = tk.Button(self, text="0", font=self.fuente, command=lambda:self.button_0())
        self.buttonA = tk.Button(self, text="A", font=self.fuente, command=lambda:self.button_A())
        self.buttonB = tk.Button(self, text="B", font=self.fuente, command=lambda:self.button_B())
        self.buttonC = tk.Button(self, text="C", font=self.fuente, command=lambda:self.button_C())
        self.buttonD = tk.Button(self, text="D", font=self.fuente, command=lambda:self.button_D())
        self.buttonE = tk.Button(self, text="E", font=self.fuente, command=lambda:self.button_E())
        self.buttonF = tk.Button(self, text="F", font=self.fuente, command=lambda:self.button_F())


        #operaciones aritmeticas
        self.buttonSuma = tk.Button(self, text="+", font=self.fuente, command=lambda:self.button_suma())
        self.buttonResta = tk.Button(self, text="-", font=self.fuente, command=lambda:self.button_resta())
        self.buttonMultiplicacion = tk.Button(self, text="*", font=self.fuente, command=lambda:self.button_multiplicacion())
        self.buttonDivision = tk.Button(self, text="/", font=self.fuente, command=lambda:self.button_division())
        self.buttonIgual = tk.Button(self, text="=", font=self.fuente, command=lambda:self.button_igual())
        self.buttonClear = tk.Button(self, text="CR", font=self.fuente, command=lambda:self.button_clear())
        self.buttonAbsolute = tk.Button(self, text="+/-", font=self.fuente, command=lambda:self.button_Absolute())
        self.buttonPunto = tk.Button(self, text=".", font=self.fuente, command=lambda:self.button_punto())
        self.buttonDelete = tk.Button(self, text="DEL", font=self.fuente, command=lambda:self.button_delete())
        self.buttonSin = tk.Button(self, text="sin", font=self.fuente, command=lambda:self.button_sin())
        self.buttonUpper = tk.Button(self, text="^", font=self.fuente, command=lambda:self.button_Upper())
        self.buttonFactorial = tk.Button(self, text="x!", font=self.fuente, command=lambda:self.button_factorial())
        self.buttonRaiz = tk.Button(self, text="√", font=self.fuente, command=lambda:self.button_raiz())
        self.buttonModule = tk.Button(self, text="%", font=self.fuente, command=lambda:self.button_modulo())

        # Ubicacion de los botones
        self.button1.grid(row=9, column=1, padx=5, pady=5)
        self.button3.grid(row=9, column=3, padx=5, pady=5)
        self.button2.grid(row=9, column=2, padx=5, pady=5)
        self.button4.grid(row=8, column=1, padx=5, pady=5)
        self.button5.grid(row=8, column=2, padx=5, pady=5)
        self.button6.grid(row=8, column=3, padx=5, pady=5)
        self.button7.grid(row=7, column=1, padx=5, pady=5)
        self.button8.grid(row=7, column=2, padx=5, pady=5)
        self.button9.grid(row=7, column=3, padx=5, pady=5)
        self.button0.grid(row=10, column=2, padx=5, pady=5)
        self.buttonA.grid(row=5, column=0, padx=5, pady=5)
        self.buttonB.grid(row=6, column=0, padx=5, pady=5)
        self.buttonC.grid(row=7, column=0, padx=5, pady=5)
        self.buttonD.grid(row=8, column=0, padx=5, pady=5)
        self.buttonE.grid(row=9, column=0, padx=5, pady=5)
        self.buttonF.grid(row=10, column=0, padx=5, pady=5)

        # Ubicacion de los botones de operaciones
        self.buttonSuma.grid(row=9, column=4, padx=5, pady=5)
        self.buttonResta.grid(row=8, column=4, padx=5, pady=5)
        self.buttonMultiplicacion.grid(row=7, column=4, padx=5, pady=5)
        self.buttonDivision.grid(row=6, column=4, padx=5, pady=5)
        self.buttonIgual.grid(row=10, column=4, padx=5, pady=5)
        self.buttonClear.grid(row=5, column=3, padx=5, pady=5)
        self.buttonAbsolute.grid(row=10, column=1, padx=5, pady=5)
        self.buttonPunto.grid(row=10, column=3, padx=5, pady=5)
        self.buttonDelete.grid(row=5, column=4, padx=5, pady=5)
        self.buttonSin.grid(row=5, column=1, padx=5, pady=5)
        self.buttonUpper.grid(row=5, column=2, padx=5, pady=5)
        self.buttonFactorial.grid(row=6, column=1, padx=5, pady=5)
        self.buttonRaiz.grid(row=6, column=2, padx=5, pady=5)
        self.buttonModule.grid(row=6, column=3, padx=5, pady=5)

        self.numero_aux = 0
        self.operador = ''
        self.Dec = True
        self.Hexa = False
        self.Octa = False
        self.Bin = False

    def dissable_operations(self):
        self.buttonMultiplicacion.config(state='disabled')
        self.buttonDivision.config(state='disabled')
        self.buttonSin.config(state='disabled')
        self.buttonFactorial.config(state='disabled')
        self.buttonUpper.config(state='disabled')
        self.buttonModule.config(state='disabled')
        self.buttonFactorial.config(state='disabled')
        self.buttonRaiz.config(state='disabled')

    def dissable_numHex(self):
        self.buttonA.config(state='disabled')
        self.buttonB.config(state='disabled')
        self.buttonC.config(state='disabled')
        self.buttonD.config(state='disabled')
        self.buttonE.config(state='disabled')
        self.buttonF.config(state='disabled')

    def enable_operations(self):
        self.buttonSuma.config(state='normal')
        self.buttonResta.config(state='normal')
        self.buttonMultiplicacion.config(state='normal')
        self.buttonDivision.config(state='normal')
        self.buttonIgual.config(state='normal')

    def disable_numbers(self):
        self.button2.config(state='disabled')
        self.button3.config(state='disabled')
        self.button4.config(state='disabled')
        self.button5.config(state='disabled')
        self.button6.config(state='disabled')
        self.button7.config(state='disabled')
        self.button8.config(state='disabled')
        self.button9.config(state='disabled')

    def disable_numbers_oct(self):
        self.button9.config(state='disabled')
        self.button8.config(state='disabled')

    def enable_numbers(self):
        self.button2.config(state='normal')
        self.button3.config(state='normal')
        self.button4.config(state='normal')
        self.button5.config(state='normal')
        self.button6.config(state='normal')
        self.button7.config(state='normal')
        self.button8.config(state='normal')
        self.button9.config(state='normal')

    def enable_numHex(self):
        self.buttonA.config(state='normal')
        self.buttonB.config(state='normal')
        self.buttonC.config(state='normal')
        self.buttonD.config(state='normal')
        self.buttonE.config(state='normal')
        self.buttonF.config(state='normal')


    def button_1(self):
        self.display.config(state='normal')
        self.display.insert(tk.END, "1")
        self.display.config(state='disabled')

    def button_2(self):
        self.display.config(state='normal')
        self.display.insert(tk.END, "2")
        self.display.config(state='disabled')

    def button_3(self):
        self.display.config(state='normal')
        self.display.insert(tk.END, "3")
        self.display.config(state='disabled')   

    def button_4(self):
        self.display.config(state='normal')
        self.display.insert(tk.END, "4")
        self.display.config(state='disabled')   

    def button_5(self):
        self.display.config(state='normal')
        self.display.insert(tk.END, "5")
        self.display.config(state='disabled')   
    
    def button_6(self):
        self.display.config(state='normal')
        self.display.insert(tk.END, "6")
        self.display.config(state='disabled')

    def button_7(self):
        self.display.config(state='normal')
        self.display.insert(tk.END, "7")
        self.display.config(state='disabled')

    def button_8(self):
        self.display.config(state='normal')
        self.display.insert(tk.END, "8")
        self.display.config(state='disabled')   

    def button_9(self):
        self.display.config(state='normal')
        self.display.insert(tk.END, "9")
        self.display.config(state='disabled')

    def button_0(self):
        self.display.config(state='normal')
        self.display.insert(tk.END, "0")
        self.display.config(state='disabled')

    def button_A(self):
        self.display.config(state='normal')
        self.displayHex.config(state='normal')
        self.display.insert(tk.END, "A")
        self.displayHex.insert(tk.END, "A")
        self.displayHex.config(state='disabled')
        self.display.config(state='disabled')
    def button_B(self):
        self.display.config(state='normal')
        self.displayHex.config(state='normal')
        self.display.insert(tk.END, "B")
        self.displayHex.insert(tk.END, "B")
        self.displayHex.config(state='disabled')
        self.display.config(state='disabled')
    def button_C(self):
        self.display.config(state='normal')
        self.displayHex.config(state='normal')
        self.display.insert(tk.END, "C")
        self.displayHex.insert(tk.END, "C")
        self.displayHex.config(state='disabled')
        self.display.config(state='disabled')

    def button_D(self):
        self.display.config(state='normal')
        self.displayHex.config(state='normal')
        self.display.insert(tk.END, "D")
        self.displayHex.insert(tk.END, "D")
        self.displayHex.config(state='disabled')
        self.display.config(state='disabled')
    def button_E(self):
        self.display.config(state='normal')
        self.displayHex.config(state='normal')
        self.display.insert(tk.END, "E")
        self.displayHex.insert(tk.END, "E")
        self.displayHex.config(state='disabled')
        self.display.config(state='disabled')
    def button_F(self):
        self.display.config(state='normal')
        self.displayHex.config(state='normal')
        self.display.insert(tk.END, "F")
        self.displayHex.insert(tk.END, "F")
        self.displayHex.config(state='disabled')
        self.display.config(state='disabled')

    def button_Hexa(self):
        self.Hexa = True
        self.Octa = False
        self.Bin = False
        self.displayHex.config(state='normal')
        self.enable_numHex()
        self.enable_numbers()
        self.dissable_operations() #no hace nada
        try:
            self.numero_aux = conv.dec_hex(int(self.display.get()))
        except ValueError:
            self.numero_aux = float(self.display.get())
            if(self.numero_aux != int(self.numero_aux)):
                aux = str(self.numero_aux).split('.')
                self.numero_aux = int(aux[:-2])
            self.numero_aux = conv.dec_hex(int(self.numero_aux))
            self.displayHex.delete(0, END)
            self.displayHex.config(state='disabled')

        self.displayHex.delete(0, END)
        self.displayHex.insert(tk.END, str(self.numero_aux))
        self.displayHex.config(state='disabled')

    def button_Decimal(self):
        self.Dec = True
        self.Hexa = False
        self.Bin = False
        self.Octa = False
        self.display.config(state='normal')
        self.displayDec.config(state='normal')
        self.dissable_numHex()
        self.enable_numbers()
        self.enable_operations()
        try:
            self.numero_aux = float(self.display.get())
        except ValueError:
            messagebox.showerror("Error", "Entrada inválida para conversión a decimal")
            self.displayDec.delete(0, END)
            self.displayDec.config(state='disabled')
            return
        self.displayDec.delete(0, END)
        self.displayDec.insert(0, str(self.numero_aux))
        self.displayDec.config(state='disabled')
        self.display.config(state='disabled')


    def button_Binario(self):
        self.displayBin.config(state='normal')
        self.dissable_operations()
        self.dissable_numHex()
        self.disable_numbers()
        try:
            self.numero_aux = conv.dec_bin(int(self.display.get()))
        except ValueError:
            self.numero_aux = conv.dec_bin(int(self.displayDec.get()))
            self.displayBin.delete(0, END)
            self.display.insert(0, str(0))
        self.displayBin.delete(0, END)
        self.display.insert(0, str(self.numero_aux))
        self.displayBin.insert(0, str(self.numero_aux))
        self.displayBin.config(state='disabled')

    def button_Octal(self):
        self.Octa = True
        self.Bin = False
        self.Hexa = False
        self.displayOct.config(state='normal')
        self.dissable_operations()
        self.dissable_numHex()
        self.disable_numbers_oct()
        try:
            self.numero_aux = conv.dec_oct(int(self.display.get()))
        except ValueError:
            self.numero_aux = conv.dec_oct(int(self.displayDec.get()))
            self.displayOct.delete(0, END)
            self.display.insert(0, str(0))
        self.displayOct.delete(0, END)
        self.displayOct.insert(0, str(self.numero_aux))
        self.displayOct.config(state='disabled')

    def button_Upper(self):
        self.display.config(state='normal')
        try:
            self.numero_aux = int(self.display.get())
            self.display.delete(0, END)
            
        except ValueError:
            messagebox.showerror("Error", "Entrada inválida para operación de potencia")
            self.display.delete(0, END)
            self.display.insert(0, str(0))
            self.display.config(state='disabled')
            return
        self.operando = '^'
        self.display.config(state='disabled')

    def button_modulo(self):
        self.display.config(state='normal')
        self.numero_aux = int(self.display.get())
        self.display.delete(0, END)
        self.display.config(state='disabled')
        self.operando = '%'


    def button_suma(self):
        self.display.config(state='normal')
        try:
            self.numero_aux = (self.display.get())
        except:
            if self.Hexa == True:
                self.mumero_aux = int(self.display.get(), 16)
            elif self.Octa == True:
                self.numero_aux = int(self.display.get(), 8)
            elif self.Bin == True: 
                int(self.display.get(), 2)
            else:
                ValueError
                return
        self.display.delete(0, END)
        self.display.config(state='disabled')
        self.operando = '+'

    def button_resta(self):
        self.display.config(state='normal')
        try:
            self.numero_aux = (self.display.get())
        except:
            if self.Hexa == True:
                self.mumero_aux = int(self.display.get(), 16)
            elif self.Octa == True:
                self.numero_aux = int(self.display.get(), 8)
            elif self.Bin == True: 
                int(self.display.get(), 2)
            else:
                ValueError
                return
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
        self.numero_aux = float(self.display.get())
        self.display.delete(0, END)
        self.display.config(state='disabled')
        self.operando = '/'

    def button_punto(self):
        self.display.config(state='normal')
        self.display.insert(tk.END, ".")
        self.numero_aux = float(self.display.get())
        self.display.config(state='disabled')

    def button_factorial(self):
        self.display.config(state="normal")
        try:
            self.numero_aux = int(self.display.get())
            self.ob = calc.Calculadora()
            self.ob.factorial(self.numero_aux)

        except ValueError:
            messagebox.showerror("Error", "Entrada inválida para factorial")
            self.display.delete(0, END)
            self.display.insert(0, str(0))
            self.display.config(state='disabled')
            return
        self.display.delete(0, END)
        self.display.insert(0, str(self.ob.getResultado()))
        self.display.config(state='disabled')

    def button_Absolute(self):
        self.display.config(state='normal')
        if(self.display.get() == int):
            self.numero_aux = int(self.display.get())
        else:
            self.numero_aux = float(self.display.get())
        if (self.numero_aux)>0:
            self.display.delete(0, END)
            self.display.insert(0, '-'+str(self.numero_aux))
        else:
            self.display.delete(0, END)
            self.display.insert(0, str(self.numero_aux))
        self.display.config(state='disabled')

    def button_raiz(self):
        self.display.config(state='normal')
        self.numero_aux = float(self.display.get())
        self.display.delete(0, END)
        try:
            self.ob= calc.Calculadora()
            self.ob.sqrt(self.numero_aux)
        except ValueError:
            messagebox.showerror("Error", "Entrada inválida para raíz cuadrada")
            self.display.delete(0, END)
            self.display.insert(0, str(0))
            self.display.config(state='disabled')
            return
        self.display.insert(0, str(self.ob.getResultado()))
        self.display.config(state='disabled')


    def button_sin(self):
        self.display.config(state='normal')
        self.numero_aux = float(self.display.get())
        self.display.delete(0, END)
        try:
            self.ob= calc.Calculadora()
            self.ob.sin(self.numero_aux)
        except ValueError:
            messagebox.showerror("Error", "Entrada inválida para función seno")
            self.display.delete(0, END)
            self.display.insert(0, str(0))
            self.display.config(state='disabled')
            return
        self.display.insert(0, str(self.ob.getResultado()))
        self.display.config(state='disabled')

    def button_igual(self):
        self.ob = calc.Calculadora()
        try:
            self.ob.operacion(self.numero_aux, int(self.display.get()), self.operando)
        except ValueError:
            self.ob.operacion(self.numero_aux, float(self.display.get()), self.operando)
            self.ob.operacion(self.numero_aux, 0, '+')
            self.display.delete(0, END)
            self.display.insert(0, str(0))
            self.display.config(state='disabled')
            return
        self.display.config(state='normal')
        self.display.delete(0, END)
        self.display.insert(0, str(self.ob.getResultado()))
        self.display.config(state='disabled')

    def button_delete(self):
        self.display.config(state='normal')
        self.displayDec.config(state='normal')
        self.displayHex.config(state='normal')
        self.displayOct.config(state='normal')
        self.displayBin.config(state='normal')
        try:
            self.display.delete(len(self.display.get())-1, END)
            self.displayDec.delete(len(self.displayDec.get())-1, END)
            self.displayHex.delete(len(self.displayHex.get())-1, END)
            self.displayOct.delete(len(self.displayOct.get())-1, END)
            self.displayBin.delete(len(self.displayBin.get())-1, END)
        except tk.TclError:
            pass
        self.display.config(state='disabled')
        self.displayDec.config(state='disabled')
        self.displayHex.config(state='disabled')
        self.displayOct.config(state='disabled')
        self.displayBin.config(state='disabled')


    def button_clear(self):
        self.ob = calc.Calculadora()
        self.ob.clear()
        self.display.config(state='normal')
        self.displayDec.config(state='normal')
        self.displayHex.config(state='normal')
        self.displayOct.config(state='normal')
        self.displayBin.config(state='normal')
        self.display.delete(0, END)
        self.displayDec.delete(0, END)
        self.displayHex.delete(0, END)
        self.displayOct.delete(0, END)
        self.displayBin.delete(0, END)
        self.display.config(state='disabled')
        self.displayDec.config(state='disabled')
        self.displayHex.config(state='disabled')
        self.displayOct.config(state='disabled')
        self.displayBin.config(state='disabled')

if __name__=="__main__":
    app=App()
    app.dissable_numHex()
    app.mainloop()