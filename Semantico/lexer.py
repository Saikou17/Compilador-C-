#Importamos las librerías necesarias
import re
import sys
from globalTypes import TokenType

# Diccionario de patrones de expresiones regulares para los tokens
#Este diccionario contiene los patrones de expresiones regulares para cada tipo de token.
token_patterns = {
    TokenType.COMMENT: r'(//[^\n]*|/\*[\s\S]*?\*/)',
    TokenType.WHITESPACE: r'\s+',
    TokenType.DATA_TYPE_KEY: r'\b(int|float|char|double)\b',
    TokenType.CONTROL_TYPE_KEY: r'\b(if|else|for|while)\b',
    TokenType.STORAGE_TYPE_KEY: r'\b(static|auto|const)\b',
    TokenType.FUNCTION_TYPE_KEY: r'\b(void|main|return)\b',
    TokenType.IDENTIFIER: r'\b[a-zA-Z_][a-zA-Z0-9_]*\b',
    TokenType.STRING: r'\"([^\\\"]|\\.)*\"',
    TokenType.CHARACTER: r'\'([^\\\']|\\.)\'',
    TokenType.NUMBER: r'\b\d+(\.\d+)?(e[+-]?\d+)?\b',
    TokenType.ARITHMETIC_OPERATOR: r'[+\-*/%]',
    TokenType.RELATIONAL_OPERATOR: r'(<=|>=|==|!=|<|>)',
    TokenType.LOGICAL_OPERATOR: r'(&&|\|\||!)',
    TokenType.ASSIGNMENT_OPERATOR: r'([+\-*/%]?=)',
    TokenType.PUNCTUATION_OPERATOR: r'[;,.(){}[\]]',
    TokenType.ENDFILE: r'\$',
}

# Variables globales
programa = "" # Texto fuente
posicion = 0 # Posición actual en el texto fuente
progLong = 0 # Longitud del texto fuente
linea_actual = 1    # Línea actual en el texto fuente
inicio_linea = 0 # Inicio de la línea actual
imprime = True # Bandera para imprimir tokens

# Inicialización de texto fuente
def globales_lexer(prog, pos, longi):
    global programa, posicion, progLong, linea_actual, inicio_linea
    programa = prog
    posicion = pos
    progLong = longi
    linea_actual = 1
    inicio_linea = 0

# Obtener el siguiente token
def getToken(imprimeFlag=False):
    global posicion, linea_actual, inicio_linea, imprime
    imprime = imprimeFlag # Actualiza la bandera de impresión

    #Revisamos si la posición actual es mayor o igual a la longitud del programa
    if posicion >= len(programa):
        return TokenType.ENDFILE, '$'

    # Resto del código desde la posición actual para revisarla
    restante = programa[posicion:]

    # Compilamos el scanner de patrones
    scanner = re.Scanner([
        #Creamos un tupla que contiene el patrón y la función que se ejecutará al encontrar un token
        (pattern, lambda scanner, token, t=ttype: (t, token))
        # Recorremos el diccionario de patrones de tokens
        for ttype, pattern in token_patterns.items()
    ])

    # Escaneamos el resto del código y obtenemos los tokens
    tokens, remainder = scanner.scan(restante)
    # Si no se encontraron tokens, se considera un error léxico
    for ttype, lexema in tokens:
        if ttype == TokenType.WHITESPACE:
            # Actualizar línea si hay saltos
            saltos = lexema.count('\n')
            if saltos > 0:
                linea_actual += saltos
                inicio_linea = posicion + lexema.rfind('\n') + 1
            posicion += len(lexema)
            continue

        if imprime:
            print(f"siguiente token({ttype.name}, '{lexema}')")

        posicion += len(lexema)
        return ttype, lexema

    # Si hay caracteres no reconocidos
    if remainder.strip():
        #Obtenemos la ubicacion del error 
        error_pos = posicion + len(restante) - len(remainder)
        columna = error_pos - inicio_linea + 1
        linea = programa[inicio_linea:programa.find('\n', inicio_linea)]
        print(f"Línea {linea_actual}: Error en la formación del token:")
        print(linea)
        print(" " * (columna - 1) + "^")

        # Finaliza ejecución inmediatamente
        sys.exit(f"Se encontró un error léxico en la línea {linea_actual}.")

    return TokenType.ENDFILE, '$'
