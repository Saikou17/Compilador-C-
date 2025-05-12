from globalTypes import *
from lexer import *

class InputBuffer:
    def __init__(self, programa=""):
        self.programa = programa
        self.posicion = 0
        self.progLong = len(programa)
        self.linea_actual = 1
        self.inicio_linea = 0
    
def main():
    # Abrimos y leemos el archivo fuente
    f = open("sample.c-", "r")
    #Creamos una instancia de la clase globales
    buffer = InputBuffer(f.read()+"$")

    # Llamamos a getToken() hasta llegar al final del archivo
    token , tokenString = getToken(buffer,True)
    print(f"Token: {token}, TokenString: {tokenString}")
    while token != TokenType.ENDFILE:
        token , tokenString = getToken(buffer,True)
        if token == TokenType.ERROR:
            print(f"Error: {tokenString}")
            break

if __name__ == "__main__":
    main()

