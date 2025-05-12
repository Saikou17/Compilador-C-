from lexer import * 
from gramatica import *
from globalTypes import *

# Variables globales
programa = None
posicion = 0
progLong = 0
token = None

def globales(prog, pos, long):
    global programa, posicion, progLong
    programa = prog
    posicion = pos
    progLong = long

dic_producciones = {}

# Clase Nodo para la construcción del AST
class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.hijosIzq = None
        self.hijosDer = None

def NuevoNodo(valor):
    return Nodo(valor)

# Clase para las producciones
class Produccion:
    def __init__(self, nombre, secuencia, terminales, bucle=[]):
        self.nombre = nombre
        self.secuencia = secuencia
        self.terminales = terminales
        self.bucle = bucle  

    # Método de verificación de coincidencia con los terminales
    def verificarMatch(self, parte=None):
        global posicion, progLong, token

        # Verificar fin de archivo antes de continuar
        if token == "$" or posicion >= progLong:
            print("Fin del archivo alcanzado. Terminando el parser.")
            return None

        if token in self.terminales and parte == token:
            n = NuevoNodo(token)
            posicion += 1
            print("Nuevo nodo:", n.valor, "Creando en:" , self.nombre)
            token = obtenerToken() if posicion < progLong else '$'
            return n
        else:
            print(f"Error: Token inesperado '{token}', pero NO avanzamos de inmediato")
            return None  

    # Método de lectura secuencial con manejo correcto de opciones y backtracking
    def lecturaSecuencial(self):
        global token, posicion, progLong
        tokens_match = 0

        # Si ya estamos en fin de archivo, devolver directamente
        if token == "$" or posicion >= progLong:
            print("Fin del archivo en lecturaSecuencial. Devolviendo None.")
            return None

        correct = True
        opcional = False
        temp_nodes = []  
        partes = self.secuencia.split(' ')

        for parte in partes:
            print("Evaluando parte :", parte , " en ", self.nombre)
            print("Token actual:", token, "Correct:" , correct)
            if parte == "[":
                opcional = True
                continue
            elif parte == "]":
                opcional = False
                continue
            elif parte == "|":
                # if temp_nodes:
                #     return self.conectarNodos(temp_nodes)
                correct = True
                # temp_nodes = []
                continue

            if correct:
                sub_nodo = None
                if parte.islower():
                    sub_nodo = dic_producciones[parte].lecturaSecuencial()
                elif (parte.isupper() or not parte.isalpha() ):
                    print("La parte y el token son iguales")
                    sub_nodo = self.verificarMatch(parte)
                elif parte == "{":
                    sub_nodo = self.verificarBucle()
                elif parte == "}":
                    return None

                if sub_nodo:
                    temp_nodes.append(sub_nodo)
                    tokens_match += 1
                else:
                    correct = False 
                    #TODO : Borramos los nodos si hayamos un error en la produccion actual
                    temp_nodes = []
                    #Nos devolvemos a la posicion restando los tokens matcheados
                    if tokens_match > 0:
                        print("Error en la producción. Deshaciendo nodos creados.")
                        posicion -= tokens_match
                        token = obtenerToken() if posicion < progLong else '$'
                        print("Token después de deshacer:", token)
            if opcional and token not in self.terminales:
                continue  

        return self.conectarNodos(temp_nodes) if temp_nodes else None

    # Método para conectar nodos correctamente
    def conectarNodos(self, nodos):
        if not nodos:
            return None
        if len(nodos) == 1:
            return nodos[0]

        actual = nodos[0]
        for sub in nodos[1:]:
            sec = NuevoNodo(self.nombre)
            sec.hijosIzq, sec.hijosDer = actual, sub
            actual = sec
        return actual

    # Método para manejar bucles correctamente
    def verificarBucle(self):
        global token, posicion, progLong
        nodos_bucle = []

        while token in self.bucle:
            sub_arbol = self.lecturaSecuencial()
            if sub_arbol:
                nodos_bucle.append(sub_arbol)

            posicion += 1
            token = obtenerToken() if posicion < progLong else '$'

        return self.conectarNodos(nodos_bucle)

# Construcción del parser y AST
def lecturaProduccion(nombre, producciones):
    loop = False
    terminales, bucle = [], []

    for element in producciones.split():
        if not loop:
            if element.isupper() or not element.isalpha():
                terminales.append(element)
            elif element == "{":
                loop = True
        else:
            if element == "}":
                loop = False
            else:
                bucle.append(element)

    return Produccion(nombre, producciones, terminales, bucle)

def readProducciones(gramatica):
    for produccion in gramatica:
        nombre, producciones = produccion[0], produccion[1]
        dic_producciones[nombre] = lecturaProduccion(nombre, producciones)

def parser(imprime=True):
    global token
    readProducciones(producciones)
    globales_lexer(programa, posicion, progLong)
    token = obtenerToken()

    # Si alcanzamos el fin del archivo antes de procesar, detener la ejecución
    if token == "$" or posicion >= progLong:
        print("Archivo vacío o sin contenido válido. Deteniendo parser.")
        return None

    return dic_producciones["program"].lecturaSecuencial()

def obtenerToken():
    return getToken(imprime)[0].name