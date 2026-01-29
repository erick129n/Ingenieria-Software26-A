def dec_bin(numero):
    binario = ''
    cociente = 0
    residuo= 0
    while numero > 0:
        cociente = int(numero/2)
        residuo = int(numero)%2
        numero = cociente
        binario = str(residuo) + binario

    return binario

def Hexa(valor):
    hex_= ""
    if valor == 10:
        hex_ = 'A'
    elif valor == 11:
        hex_ = 'B'
    elif valor == 12:
        hex_ = 'C'
    elif valor == 13:
        hex_ = 'D'
    elif valor == 14:
        hex_ ='E'
    elif valor == 15:
        hex_ = 'F'
    else:
        hex_ = str(valor)
    return hex_

def dec_hex(numero):
    if numero == 0:
        return "0"
    
    hex_ = ''
    numero = int(numero)
    
    while numero > 0:
        residuo = numero % 16
        hex_ = Hexa(residuo) + hex_
        numero = numero // 16 
    
    return hex_

def dec_oct(numero):
    octal = ''
    cociente = 0
    residuo= 0
    while numero > 0:
        cociente = int(numero/8)
        residuo = int(numero)%8
        numero = cociente
        octal = str(residuo) + octal

    return octal
