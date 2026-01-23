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
        elif operador == '/':
            if n2 != 0:
                self.resultado = n1 / n2
            else:
                raise ValueError("No se puede dividir por cero")
        return self.resultado

    def clear(self):
         self.resultado = 0
         return self.resultado
    

    def getResultado(self):
        return self.resultado