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
        
        self.geometry('450x600')
        self.minsize(450, 600)
        
        # Grid config for main window
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frame = tk.Frame(self, borderwidth=5)
        self.frame.grid(row=0, column=0, sticky="nsew")

        # Configure columns and rows for the frame to make buttons uniform
        for i in range(5):
            self.frame.grid_columnconfigure(i, weight=1, minsize=60)
        for i in range(11):
            self.frame.grid_rowconfigure(i, weight=1, minsize=40)

        self.display = tk.Entry(self.frame, font=self.fuenteDisplay, justify='right')
        
        self.buttonHex = tk.Button(self.frame, text="Hex:", background='lightgray', font=tk.font.Font(family='Arial', size=10), command=self.button_Hexa)
        self.buttonDec = tk.Button(self.frame, text="Dec:", background='lightgray', font=tk.font.Font(family='Arial', size=10), command=self.button_Decimal)
        self.buttonOct = tk.Button(self.frame, text="Oct:", background='lightgray', font=tk.font.Font(family='Arial', size=10), command=self.button_Octal)
        self.buttonBin = tk.Button(self.frame, text="Bin:", background='lightgray', font=tk.font.Font(family='Arial', size=10), command=self.button_Binario)

        self.buttonHex.grid(row=1, column=0, padx=2, pady=2, sticky='nsew')
        self.buttonDec.grid(row=2, column=0, padx=2, pady=2, sticky='nsew')
        self.buttonOct.grid(row=3, column=0, padx=2, pady=2, sticky='nsew')
        self.buttonBin.grid(row=4, column=0, padx=2, pady=2, sticky='nsew')

        self.displayHex = tk.Entry(self.frame, font=self.fuente, justify='right')
        self.displayDec = tk.Entry(self.frame, font=self.fuente, justify='right')
        self.displayOct = tk.Entry(self.frame, font=self.fuente, justify='right')
        self.displayBin = tk.Entry(self.frame, font=self.fuente, justify='right')

        self.display.grid(row=0, column=0, columnspan=5, rowspan=1, padx=5, pady=5, sticky='nsew')
        self.displayHex.grid(row=1, column=1, columnspan=4, rowspan=1, sticky='nsew', padx=2, pady=2)
        self.displayDec.grid(row=2, column=1, columnspan=4, rowspan=1, sticky='nsew', padx=2, pady=2)
        self.displayOct.grid(row=3, column=1, columnspan=4, rowspan=1, sticky='nsew', padx=2, pady=2)
        self.displayBin.grid(row=4, column=1, columnspan=4, rowspan=1, sticky='nsew', padx=2, pady=2)

        self.button1 = tk.Button(self.frame, text="1", font=self.fuente, command=lambda: self._insert_text("1"))
        self.button2 = tk.Button(self.frame, text="2", font=self.fuente, command=lambda: self._insert_text("2"))
        self.button3 = tk.Button(self.frame, text="3", font=self.fuente, command=lambda: self._insert_text("3"))
        self.button4 = tk.Button(self.frame, text="4", font=self.fuente, command=lambda: self._insert_text("4"))
        self.button5 = tk.Button(self.frame, text="5", font=self.fuente, command=lambda: self._insert_text("5"))
        self.button6 = tk.Button(self.frame, text="6", font=self.fuente, command=lambda: self._insert_text("6"))
        self.button7 = tk.Button(self.frame, text="7", font=self.fuente, command=lambda: self._insert_text("7"))
        self.button8 = tk.Button(self.frame, text="8", font=self.fuente, command=lambda: self._insert_text("8"))
        self.button9 = tk.Button(self.frame, text="9", font=self.fuente, command=lambda: self._insert_text("9"))
        self.button0 = tk.Button(self.frame, text="0", font=self.fuente, command=lambda: self._insert_text("0"))
        
        self.buttonA = tk.Button(self.frame, text="A", font=self.fuente, command=lambda: self._insert_text("A", hex_only=True))
        self.buttonB = tk.Button(self.frame, text="B", font=self.fuente, command=lambda: self._insert_text("B", hex_only=True))
        self.buttonC = tk.Button(self.frame, text="C", font=self.fuente, command=lambda: self._insert_text("C", hex_only=True))
        self.buttonD = tk.Button(self.frame, text="D", font=self.fuente, command=lambda: self._insert_text("D", hex_only=True))
        self.buttonE = tk.Button(self.frame, text="E", font=self.fuente, command=lambda: self._insert_text("E", hex_only=True))
        self.buttonF = tk.Button(self.frame, text="F", font=self.fuente, command=lambda: self._insert_text("F", hex_only=True))

        self.buttonSuma = tk.Button(self.frame, text="+", font=self.fuente, command=lambda: self.set_operando('+'))
        self.buttonResta = tk.Button(self.frame, text="-", font=self.fuente, command=lambda: self.set_operando('-'))
        self.buttonMultiplicacion = tk.Button(self.frame, text="*", font=self.fuente, command=lambda: self.set_operando('*'))
        self.buttonDivision = tk.Button(self.frame, text="/", font=self.fuente, command=lambda: self.set_operando('/'))
        self.buttonIgual = tk.Button(self.frame, text="=", font=self.fuente, command=self.button_igual)
        self.buttonClear = tk.Button(self.frame, text="CR", font=self.fuente, command=self.button_clear)
        self.buttonAbsolute = tk.Button(self.frame, text="+/-", font=self.fuente, command=self.button_Absolute)
        self.buttonPunto = tk.Button(self.frame, text=".", font=self.fuente, command=self.button_punto)
        self.buttonDelete = tk.Button(self.frame, text="DEL", font=self.fuente, command=self.button_delete)
        self.buttonSin = tk.Button(self.frame, text="sin", font=self.fuente, command=self.button_sin)
        self.buttonUpper = tk.Button(self.frame, text="^", font=self.fuente, command=lambda: self.set_operando('^'))
        self.buttonFactorial = tk.Button(self.frame, text="x!", font=self.fuente, command=self.button_factorial)
        self.buttonRaiz = tk.Button(self.frame, text="√", font=self.fuente, command=self.button_raiz)
        self.buttonModule = tk.Button(self.frame, text="%", font=self.fuente, command=lambda: self.set_operando('%'))

        self.button1.grid(row=9, column=1, padx=2, pady=2, sticky="nsew")
        self.button3.grid(row=9, column=3, padx=2, pady=2, sticky="nsew")
        self.button2.grid(row=9, column=2, padx=2, pady=2, sticky="nsew")
        self.button4.grid(row=8, column=1, padx=2, pady=2, sticky="nsew")
        self.button5.grid(row=8, column=2, padx=2, pady=2, sticky="nsew")
        self.button6.grid(row=8, column=3, padx=2, pady=2, sticky="nsew")
        self.button7.grid(row=7, column=1, padx=2, pady=2, sticky="nsew")
        self.button8.grid(row=7, column=2, padx=2, pady=2, sticky="nsew")
        self.button9.grid(row=7, column=3, padx=2, pady=2, sticky="nsew")
        self.button0.grid(row=10, column=2, padx=2, pady=2, sticky="nsew")
        self.buttonA.grid(row=5, column=0, padx=2, pady=2, sticky="nsew")
        self.buttonB.grid(row=6, column=0, padx=2, pady=2, sticky="nsew")
        self.buttonC.grid(row=7, column=0, padx=2, pady=2, sticky="nsew")
        self.buttonD.grid(row=8, column=0, padx=2, pady=2, sticky="nsew")
        self.buttonE.grid(row=9, column=0, padx=2, pady=2, sticky="nsew")
        self.buttonF.grid(row=10, column=0, padx=2, pady=2, sticky="nsew")

        self.buttonSuma.grid(row=9, column=4, padx=2, pady=2, sticky="nsew")
        self.buttonResta.grid(row=8, column=4, padx=2, pady=2, sticky="nsew")
        self.buttonMultiplicacion.grid(row=7, column=4, padx=2, pady=2, sticky="nsew")
        self.buttonDivision.grid(row=6, column=4, padx=2, pady=2, sticky="nsew")
        self.buttonIgual.grid(row=10, column=4, padx=2, pady=2, sticky="nsew")
        self.buttonClear.grid(row=5, column=3, padx=2, pady=2, sticky="nsew")
        self.buttonAbsolute.grid(row=10, column=1, padx=2, pady=2, sticky="nsew")
        self.buttonPunto.grid(row=10, column=3, padx=2, pady=2, sticky="nsew")
        self.buttonDelete.grid(row=5, column=4, padx=2, pady=2, sticky="nsew")
        self.buttonSin.grid(row=5, column=1, padx=2, pady=2, sticky="nsew")
        self.buttonUpper.grid(row=5, column=2, padx=2, pady=2, sticky="nsew")
        self.buttonFactorial.grid(row=6, column=1, padx=2, pady=2, sticky="nsew")
        self.buttonRaiz.grid(row=6, column=2, padx=2, pady=2, sticky="nsew")
        self.buttonModule.grid(row=6, column=3, padx=2, pady=2, sticky="nsew")

        self.calc = calc.Calculadora() 
        self.numero_aux = 0
        self.operador = ''
        self.Dec = True
        self.Hexa = False
        self.Octa = False
        self.Bin = False
        self.operando = ''

    def _parse_display_to_base10(self):
        val = self.display.get()
        if not val or val == "-" or val == ".":
            return 0
        try:
            if self.Hexa:
                return int(val, 16)
            elif self.Octa:
                return int(val, 8)
            elif self.Bin:
                return int(val, 2)
            else:
                return float(val) if '.' in val else int(val)
        except ValueError:
            return 0

    def _format_value_for_current_mode(self, base10_val):
        try:
            if self.Hexa:
                return conv.dec_hex(int(base10_val))
            elif self.Octa:
                return conv.dec_oct(int(base10_val))
            elif self.Bin:
                return conv.dec_bin(int(base10_val))
            else:
                if isinstance(base10_val, float) and base10_val.is_integer():
                    return str(int(base10_val))
                return str(base10_val)
        except (ValueError, TypeError, OverflowError):
            return "Error"

    def _sync_active_display(self):
        val = self.display.get()
        if self.Hexa:
            self.displayHex.config(state='normal')
            self.displayHex.delete(0, END)
            self.displayHex.insert(tk.END, val)
            self.displayHex.config(state='disabled')
        elif self.Dec:
            self.displayDec.config(state='normal')
            self.displayDec.delete(0, END)
            self.displayDec.insert(tk.END, val)
            self.displayDec.config(state='disabled')
        elif self.Octa:
            self.displayOct.config(state='normal')
            self.displayOct.delete(0, END)
            self.displayOct.insert(tk.END, val)
            self.displayOct.config(state='disabled')
        elif self.Bin:
            self.displayBin.config(state='normal')
            self.displayBin.delete(0, END)
            self.displayBin.insert(tk.END, val)
            self.displayBin.config(state='disabled')

    def _insert_text(self, text, hex_only=False):
        self.display.config(state='normal')
        self.display.insert(tk.END, text)
        self.display.config(state='disabled')
        self._sync_active_display()

    def dissable_operations(self):
        self.buttonMultiplicacion.config(state='disabled')
        self.buttonDivision.config(state='disabled')
        self.buttonSin.config(state='disabled')
        self.buttonFactorial.config(state='disabled')
        self.buttonUpper.config(state='disabled')
        self.buttonModule.config(state='disabled')
        self.buttonRaiz.config(state='disabled')

    def dissable_numHex(self):
        for btn in (self.buttonA, self.buttonB, self.buttonC, self.buttonD, self.buttonE, self.buttonF):
            btn.config(state='disabled')

    def enable_operations(self):
        for btn in (self.buttonSuma, self.buttonResta, self.buttonMultiplicacion, self.buttonDivision, self.buttonIgual):
            btn.config(state='normal')

    def disable_numbers(self):
        for btn in (self.button2, self.button3, self.button4, self.button5, self.button6, self.button7, self.button8, self.button9):
            btn.config(state='disabled')

    def disable_numbers_oct(self):
        self.button8.config(state='disabled')
        self.button9.config(state='disabled')

    def enable_numbers(self):
        for btn in (self.button2, self.button3, self.button4, self.button5, self.button6, self.button7, self.button8, self.button9):
            btn.config(state='normal')

    def enable_numHex(self):
        for btn in (self.buttonA, self.buttonB, self.buttonC, self.buttonD, self.buttonE, self.buttonF):
            btn.config(state='normal')

    def _switch_mode(self, new_mode):
        base10_val = self._parse_display_to_base10()
        
        self.Dec = (new_mode == 'DEC')
        self.Hexa = (new_mode == 'HEX')
        self.Octa = (new_mode == 'OCT')
        self.Bin = (new_mode == 'BIN')
        
        if new_mode == 'HEX':
            self.enable_numHex()
            self.enable_numbers()
            self.dissable_operations() 
        elif new_mode == 'DEC':
            self.dissable_numHex()
            self.enable_numbers()
            self.enable_operations()
        elif new_mode == 'OCT':
            self.dissable_numHex()
            self.enable_numbers()
            self.disable_numbers_oct()
            self.dissable_operations()
        elif new_mode == 'BIN':
            self.dissable_numHex()
            self.enable_numbers()
            self.disable_numbers()
            self.dissable_operations()

        new_text = self._format_value_for_current_mode(base10_val)
        
        self.display.config(state='normal')
        self.display.delete(0, END)
        self.display.insert(tk.END, new_text)
        self.display.config(state='disabled')
        
        self._sync_active_display()

    def button_Hexa(self): self._switch_mode('HEX')
    def button_Decimal(self): self._switch_mode('DEC')
    def button_Octal(self): self._switch_mode('OCT')
    def button_Binario(self): self._switch_mode('BIN')

    def set_operando(self, op):
        self.numero_aux = self._parse_display_to_base10()
        
        self.display.config(state='normal')
        self.display.delete(0, END)
        self.display.config(state='disabled')
        
        self.operando = op
        self._sync_active_display()

    def button_punto(self):
        self.display.config(state='normal')
        if "." not in self.display.get():
            self.display.insert(tk.END, ".")
        self.display.config(state='disabled')
        self._sync_active_display()

    def button_factorial(self):
        try:
            num = int(self._parse_display_to_base10())
            self.calc.factorial(num)
            
            new_text = self._format_value_for_current_mode(self.calc.getResultado())
            self.display.config(state="normal")
            self.display.delete(0, END)
            self.display.insert(0, new_text)
            self.display.config(state='disabled')
            
            self._sync_active_display()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            self.button_clear()

    def button_Absolute(self):
        val = self._parse_display_to_base10()
        new_val = -val
        
        new_text = self._format_value_for_current_mode(new_val)
        self.display.config(state='normal')
        self.display.delete(0, END)
        self.display.insert(0, new_text)
        self.display.config(state='disabled')
        
        self._sync_active_display()

    def button_raiz(self):
        try:
            num = self._parse_display_to_base10()
            self.calc.sqrt(num)
            
            new_text = self._format_value_for_current_mode(self.calc.getResultado())
            self.display.config(state='normal')
            self.display.delete(0, END)
            self.display.insert(0, new_text)
            self.display.config(state='disabled')
            
            self._sync_active_display()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            self.button_clear()

    def button_sin(self):
        try:
            num = self._parse_display_to_base10()
            self.calc.sin(num)
            
            new_text = self._format_value_for_current_mode(self.calc.getResultado())
            self.display.config(state='normal')
            self.display.delete(0, END)
            self.display.insert(0, new_text)
            self.display.config(state='disabled')
            
            self._sync_active_display()
        except ValueError as e:
            messagebox.showerror("Error", "Entrada inválida para función seno")
            self.button_clear()

    def button_igual(self):
        if not self.operando:
            return
            
        val = self.display.get()
        if not val:
            return 
            
        try:
            num2 = self._parse_display_to_base10()
            self.calc.operacion(self.numero_aux, num2, self.operando)
            
            res = self.calc.getResultado()
            new_text = self._format_value_for_current_mode(res)
            
            self.display.config(state='normal')
            self.display.delete(0, END)
            self.display.insert(0, new_text)
            self.display.config(state='disabled')
            
            self.numero_aux = res
            self.operando = '' 
            self._sync_active_display()
            
        except ZeroDivisionError:
            messagebox.showerror("Error", "No se puede dividir por cero")
            self.button_clear()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            self.button_clear()


    def button_delete(self):
        self.display.config(state='normal')
        if len(self.display.get()) > 0:
            self.display.delete(len(self.display.get())-1, END)
        self.display.config(state='disabled')
        
        self._sync_active_display()


    def button_clear(self):
        self.calc.clear()
        self.numero_aux = 0
        self.operando = ''
        
        self.display.config(state='normal')
        self.display.delete(0, END)
        self.display.config(state='disabled')
        
        for d in (self.displayHex, self.displayDec, self.displayOct, self.displayBin):
            d.config(state='normal')
            d.delete(0, END)
            d.config(state='disabled')
            
        self._sync_active_display()

if __name__=="__main__":
    app=App()
    app.dissable_numHex()
    app.mainloop()