from globalTypes import *
from lexer import *
from parser import *

class InputBuffer:
    def __init__(self, programa=""):
        self.programa = programa
        self.posicion = 0
        self.progLong = len(programa)
        self.linea_actual = 1
        self.inicio_linea = 0

def parserInorder(nodo):
    if nodo is None:
        return
    parserInorder(nodo.hijosIzq)
    print(nodo.valor)
    parserInorder(nodo.hijosDer)
    
def main():
    # Abrimos y leemos el archivo fuente
    f = open("sample.c-", "r")
    #Creamos una instancia de la clase globales
    buffer = InputBuffer(f.read()+"$")

    # Llamamos a getToken() hasta llegar al final del archivo
    AST = parser(buffer,True)

    # Imprimimos el AST
    parserInorder(AST)

if __name__ == "__main__":
    main()

