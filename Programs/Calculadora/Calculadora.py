import conversiones as conv
import math
class Calculadora:
    def __init__(self):
        self.resultado = 0
    
    def operacion(self, n1, n2, operador):
        if operador == '+':
            self.resultado = n1 + n2
        elif operador == '-':
            self.resultado = n1 - n2
        elif operador == '*':
            self.resultado = n1 * n2
        elif operador == '^':
            self.resultado = n1 ** n2
        elif operador == 'x!':
            resultado = 1
            for i in range(1, n1 + 1):
                resultado *= i
            self.resultado = resultado
        elif operador == 'sin':
            self.resultado = math.sin(math.radians(n1))
        elif operador == '%':
            self.resultado = n1 % n2
        elif operador == '√':
            self.resultado = math.sqrt(n1)
        elif operador == '/':
            if n2 != 0:
                self.resultado = n1 / n2
            else:
                raise ValueError("No se puede dividir por cero")
        return self.resultado

    def clear(self):
         self.resultado = 0
         return self.resultado
    
    def factorial(self, n):
        n = int(n)
        if n < 0:
            raise ValueError("El factorial no está definido para números negativos")
        resultado = 1
        for i in range(1, n + 1):
            resultado *= i
        self.resultado = resultado
        return self.resultado

    def sqrt(self, n):
        n = float(n)
        if n < 0:
            raise ValueError("La raíz cuadrada no está definida para números negativos")
        self.resultado = math.sqrt(n)
        return self.resultado
    
    def sin(self, n):
        n = float(n)
        self.resultado = math.sin(math.radians(n))
        return self.resultado

    def getResultado(self):
        return self.resultado