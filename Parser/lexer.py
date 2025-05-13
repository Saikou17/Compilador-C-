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
}


def getToken(buffer, imprime=False):
    if buffer.posicion >= len(buffer.programa):
        return TokenType.ENDFILE, ''

    restante = buffer.programa[buffer.posicion:]

    scanner = re.Scanner([
        (pattern, lambda scanner, token, t=ttype: (t, token))
        for ttype, pattern in token_patterns.items()
    ])

    tokens, remainder = scanner.scan(restante)

    for ttype, lexema in tokens:
        if ttype == TokenType.WHITESPACE:
            saltos = lexema.count('\n')
            if saltos > 0:
                buffer.linea_actual += saltos
                buffer.inicio_linea = buffer.posicion + lexema.rfind('\n') + 1
            buffer.posicion += len(lexema)
            continue

        if imprime:
            print(f"({ttype.name}, '{lexema}')")

        buffer.posicion += len(lexema)
        return ttype, lexema

    if remainder.strip():
        error_pos = buffer.posicion + len(restante) - len(remainder)
        columna = error_pos - buffer.inicio_linea + 1
        linea = buffer.programa[buffer.inicio_linea:buffer.programa.find('\n', buffer.inicio_linea)]
        print(f"Línea {buffer.linea_actual}: Error en la formación del token:")
        print(linea)
        print(" " * (columna - 1) + "^")
        sys.exit(f"Se encontró un error léxico en la línea {buffer.linea_actual}.")

    return TokenType.ENDFILE, ''
