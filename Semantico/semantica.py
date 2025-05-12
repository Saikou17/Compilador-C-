#Importamos las librerias necesarias
from globalTypes import *
from parser import *

class stackST():
    def __init__(self):
        #Creamos una pila que guarde elementos de tipo symbolTable
        self.stack = []
        self.current = None
    #Definimos los metodo de una pila de stack los cuales son:
    # enterSymbol : Agrega un nuevo simbolo a la tabla de simbolos que se encuentra en el top de la pila
    # localLookup : Busca un simbolo en la tabla de simbolos que se encuentra en el top de la pila
    # globalLookup : Busca un simbolo en la tabla de simbolos que se encuentra en la pila
    # updateSymbol : Actualiza un simbolo en la tabla de simbolos luego de buscarlo en la pila
    def enterSymbol(self, name, tipo, line, scope, alcance):
        #Agrega un nuevo simbolo a la tabla de simbolos que se encuentra en el top de la pila
        if self.current == None:
            self.current = symbolTable(name, tipo, line, scope, alcance)
            self.stack.append(self.current)
        else:
            self.current.insertSymbol(name, tipo, line, scope, alcance)
            self.stack.append(self.current)
    def localLookup(self, name):
        #Busca un simbolo en la tabla de simbolos que se encuentra en el top de la pila
        if self.current == None:
            return None
        else:
            return self.current.getSymbol(name)
    def globalLookup(self, name):
        #Busca un simbolo en la tabla de simbolos que se encuentra en la pila
        for i in self.stack:
            if i.getSymbol(name) != None:
                return i.getSymbol(name)
        return None
    def updateSymbol(self, name, tipo, line, scope, alcance):
        #Actualiza un simbolo en la tabla de simbolos luego de buscarlo en la pila
        for i in self.stack:
            if i.setSymbol(name, tipo, line, scope, alcance) == True:
                return True
        return False

class symbolTable():
    #Definimos la tabla de simbolos que se construye de la siguiente manera:
    #Variable de tipo libre| tipo | line of declaration | scope | alcance |
    def __init__ (self, name, tipo, line, scope = None, alcance = None):
        self.name = name
        self.tipo = tipo
        self.line = line
        self.scope = scope
        self.alcance = alcance
        #Creamos un diccionario de simbolos que se guardan en la tabla de simbolos
        self.symbols = {}
    #Metodos de la tabla de simbolos los cuales son:
    # insertSymbol: Inserta un simbolo en la tabla de simbolos
    # getSymbol: Busca un simbolo en la tabla de simbolos
    # setSymbol: Cambia el valor de un simbolo en la tabla de simbolos
    def insertSymbol(self, name, tipo, line, scope, alcance):
        self.name = name
        self.tipo = tipo
        self.line = line
        self.scope = scope
        self.alcance = alcance
    def getSymbol(self, name):
        #Busca un simbolo en la tabla de simbolos
        for i in self.stack:
            if i.name == name:
                return i
        return None
    def setSymbol(self, name, tipo, line, scope, alcance):
        #Cambia el valor de un simbolo en la tabla de simbolos
        for i in self.stack:
            if i.name == name:
                i.tipo = tipo
                i.line = line
                i.scope = scope
                i.alcance = alcance
                return True
        return False

#Recorremos el arbol en preorden y vamos guardando los simbolos en la tabla de simbolos
def tabla(tree, imprime = True):
    #Guardamos el arbol en la variables ast
    AST = parser(True)
    #Inicializamos el stack de la tabla de simbolos
    stack_ST = stackST()
    #Inicializamos la tabla de simbolos
    sTable = symbolTable("Scope0",)



    #Creamos el primer scope o tabla de simbolos
    st = symbolTable("global", "global", 0, None, None)
    #Verificamos si el valor del nodo es un simbolo o una variable
    if tree.valor == "ID":
        #Si el simbolo es una variable, la guardamos en la tabla de simbolos
        if tree.hijosIzq != None:
            st.insertSymbol(tree.hijosIzq.valor, tree.hijosIzq.tipo, tree.hijosIzq.linea, None, None)
        #Si el simbolo es una funcion, la guardamos en la tabla de simbolos
        else:
            st.insertSymbol(tree.valor, tree.tipo, tree.linea, None, None)
