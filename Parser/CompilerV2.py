from parser import *
from globalTypes import *

# Función para imprimir el árbol de sintaxis de manera jerárquica
def printArbol(arbol, nivel=0, prefijo="└── "):
    """ Imprime el árbol de sintaxis en una estructura visual similar a un árbol de directorios """
    if arbol is not None:
        print(" " * (nivel * 4) + prefijo + arbol.valor)
        if arbol.hijosIzq or arbol.hijosDer:
            printArbol(arbol.hijosIzq, nivel + 1, "├── ")
            printArbol(arbol.hijosDer, nivel + 1, "└── ")

# Leemos el archivo de entrada
f = open('sample.c-', 'r')
programa = f.read()
progLong = len(programa)  # Longitud original
programa += '$'  # Agregar EOF
posicion = 0  # Posición inicial
print("Texto fuente:\n", programa)  

# Cargamos las variables globales
globales(programa, posicion, progLong)

# Inicializamos el parser
AST = parser(True)  
print("\nÁrbol de Sintaxis Abstracta:\n")
printArbol(AST)  # Imprimimos el árbol de sintaxis