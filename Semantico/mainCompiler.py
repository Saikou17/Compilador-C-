from globalTypes import *
from lexer import *
from parser import *
from semantica import *

class InputBuffer:
    def __init__(self, programa=""):
        self.programa = programa
        self.posicion = 0
        self.progLong = len(programa)
        self.linea_actual = 1
        self.inicio_linea = 0

def printAST(nodo, nivel=0):
    """Función para imprimir el AST de manera estructurada"""
    if nodo is None:
        return
    
    # Imprimir el nodo actual con indentación
    indent = "  " * nivel
    node_info = f"{nodo.tipo}"
    if nodo.valor is not None:
        node_info += f" ({nodo.valor})"
    print(indent + node_info)
    
    # Recorrer todos los hijos recursivamente
    for hijo in nodo.hijos:
        printAST(hijo, nivel + 1)

def main():
    # Abrimos y leemos el archivo fuente
    with open("sample.c-", "r") as f:
        buffer = InputBuffer(f.read() + "$")

    # Generamos el AST
    print("\nAnalizando código...")
    AST = parser(buffer, False)  # Cambiar a True para ver tokens

    # Imprimimos el AST
    print("\nÁrbol de Sintaxis Abstracta (AST):")
    printAST(AST)

    # Análisis semántico
    print("\nRealizando análisis semántico...")
    tabla_simbolos = crearTabla(AST)
    errores = analisisSemantico(AST, tabla_simbolos)

    if errores:
        print("\nErrores semánticos encontrados:")
        for e in errores:
            print(e)
    else:
        print("\nEl programa es semánticamente correcto.")

    printSymbolTables(tabla_simbolos)

if __name__ == "__main__":
    main()