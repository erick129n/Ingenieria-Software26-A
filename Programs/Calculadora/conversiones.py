def dec_bin(numero):
    if numero == 0:
        return "0"
    is_neg = numero < 0
    numero = abs(int(numero))
    binario = ''
    while numero > 0:
        residuo = numero % 2
        numero = numero // 2
        binario = str(residuo) + binario
    return "-" + binario if is_neg else binario

def Hexa(valor):
    if valor == 10: return 'A'
    if valor == 11: return 'B'
    if valor == 12: return 'C'
    if valor == 13: return 'D'
    if valor == 14: return 'E'
    if valor == 15: return 'F'
    return str(valor)

def dec_hex(numero):
    if numero == 0:
        return "0"
    is_neg = numero < 0
    numero = abs(int(numero))
    hex_ = ''
    while numero > 0:
        residuo = numero % 16
        hex_ = Hexa(residuo) + hex_
        numero = numero // 16
    return "-" + hex_ if is_neg else hex_

def dec_oct(numero):
    if numero == 0:
        return "0"
    is_neg = numero < 0
    numero = abs(int(numero))
    octal = ''
    while numero > 0:
        residuo = numero % 8
        numero = numero // 8
        octal = str(residuo) + octal
    return "-" + octal if is_neg else octal
