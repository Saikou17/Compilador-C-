#Importamos las librerias necesarias
from globalTypes import *
from parser import *

class StackST:
    def __init__(self):
        self.stack = []

    def push(self, table):
        self.stack.append(table)

    def pop(self):
        return self.stack.pop()

    def peek(self):
        return self.stack[-1] if self.stack else None

    def lookup(self, name):
        # Busca desde el scope actual hacia arriba
        for table in reversed(self.stack):
            if name in table:
                return table.getSymbol(name)
        return None

    def insert(self, name, info):
        # Inserta en el scope actual (tope de la pila)
        return self.peek().insertSymbol(name, info)

    def update(self, name, info):
        # Actualiza en el primer scope donde aparece
        for table in reversed(self.stack):
            if name in table:
                return table.updateSymbol(name, info)
        return False

    def __repr__(self):
        return "\n".join(repr(t) for t in reversed(self.stack))

class SymbolTable:
    def __init__(self, scope_name="global"):
        self.scope_name = scope_name
        self.symbols = {}  # Diccionario de símbolos

    def insertSymbol(self, name, info):
        if name in self.symbols:
            return False  # Símbolo ya existe en este scope
        self.symbols[name] = info
        return True

    def getSymbol(self, name):
        return self.symbols.get(name, None)

    def updateSymbol(self, name, info):
        if name in self.symbols:
            self.symbols[name] = info
            return True
        return False

    def __contains__(self, name):
        return name in self.symbols

    def __repr__(self):
        return f"<SymbolTable {self.scope_name}: {self.symbols}>"

def crearTabla(ast):
    stack = StackST()
    global_scope = SymbolTable("global")
    stack.push(global_scope)

    def visit(node):
        if node is None:
            return

        nodetype = node.tipo

        if nodetype == "fun_declaration":

            func_name = node.hijos[1].valor
            return_type = node.hijos[0].valor

            # Nodo "params"
            params_node = node.hijos[2]
            param_nodes = []

            if params_node and params_node.tipo == "params":
                # Verifica si hay un nodo "param_list" como hijo
                if params_node.hijos and params_node.hijos[0].tipo == "param_list":
                    param_list_node = params_node.hijos[0]
                    param_nodes = param_list_node.hijos
                # Si no hay param_list y es 'void', se omite

            # Mostrar parámetros y agregarlos
            for param in param_nodes:
                if len(param.hijos) >= 2:
                    param_type = param.hijos[0].valor
                    param_name = param.hijos[1].valor

            # Insertar la función en el scope global
            func_info = {
                "type": "function",
                "return_type": return_type,
                "params": [
                    (param.hijos[1].valor, param.hijos[0].valor)
                    for param in param_nodes if len(param.hijos) >= 2
                ]
            }
            stack.insert(func_name, func_info)

            # Crear nuevo scope para la función
            func_scope = SymbolTable(f"function:{func_name}")
            stack.push(func_scope)

            # Insertar parámetros en el nuevo scope
            for param in param_nodes:
                if len(param.hijos) >= 2:
                    param_type = param.hijos[0].valor
                    param_name = param.hijos[1].valor
                    stack.insert(param_name, {"type": "variable", "var_type": param_type})

        elif nodetype == "var_declaration":
            var_type = node.hijos[0].valor
            var_name = node.hijos[1].valor
            stack.insert(var_name, {"type": "variable", "var_type": var_type})

        # Visitar hijos recursivamente
        for child in node.hijos:
            visit(child)

    visit(ast)
    return stack


def analisisSemantico(ast, stack):
    errores = []

    def visit(node, current_func_type=None):
        if node is None:
            return None

        nodetype = node.tipo
        value = node.valor

        # Recorrer hijos (postorden)
        child_types = [visit(child, current_func_type) for child in node.hijos]

        # === CASOS ESPECÍFICOS ===

        if node.hijos and node.hijos[0].tipo == "ID":
            id_node = node.hijos[0]
            var_name = id_node.valor  # Aquí está el lexema
            symbol = stack.lookup(var_name)
            if symbol is None:
                errores.append(f"Error: variable '{var_name}' no declarada.")
                return "error"
            return symbol["var_type"]

        elif nodetype == "NUM":
            return "int"

        elif nodetype == "expression_stmt":
            return child_types[0]

        elif nodetype == "expression":
            if len(node.hijos) == 1:
                return child_types[0]
            elif len(node.hijos) == 2 and node.hijos[1].tipo == "simple_expression":
                return child_types[1]
            elif len(node.hijos) == 3 and node.hijos[1].valor == "=":
                # Asignación: ID = expresión
                var_type = child_types[0]
                expr_type = child_types[2]
                if var_type != expr_type:
                    errores.append(f"[Error: asignación incompatible ({var_type} = {expr_type})")
                return var_type

        elif nodetype == "simple_expression":
            if len(child_types) == 1:
                return child_types[0]
            elif len(child_types) == 3:
                t1, t2 = child_types[0], child_types[2]
                if t1 != t2:
                    errores.append(f"[Error: comparación entre tipos incompatibles ({t1}, {t2})")
                return "int"

        elif nodetype == "additive_expression":
            return child_types[-1]  # Propagamos el tipo del término final

        elif nodetype == "term":
            return child_types[-1]

        elif nodetype == "selection_stmt":
            cond_type = child_types[0]
            if cond_type != "int":
                errores.append(f"[Error: condición en if debe ser de tipo int.")
            return None

        elif nodetype == "iteration_stmt":
            cond_type = child_types[0]
            if cond_type != "int":
                errores.append(f"[Error: condición en while/for debe ser de tipo int.")
            return None

        elif nodetype == "return_stmt":
            if not child_types or child_types[0] is None:
                ret_type = "void"
            else:
                ret_type = child_types[0]
            if current_func_type and ret_type != current_func_type:
                errores.append(f"[Error: retorno incompatible. Esperado '{current_func_type}', se obtuvo '{ret_type}'.")
            return ret_type
        
        elif nodetype == "var":
            # Acceso a una variable (puede ser array o simple)
            var_name = node.valor  # El primer hijo debe ser ID
            symbol = stack.lookup(var_name)
            if symbol is None:
                errores.append(f"[Error: variable '{var_name}' no declarada.")
                return "error"
            return symbol["var_type"]

        elif nodetype == "call":
            func_symbol = stack.lookup(value)
            if func_symbol is None:
                errores.append(f"[Error: función '{value}' no declarada.")
                return "error"
            if func_symbol["type"] != "function":
                errores.append(f"[Error: '{value}' no es una función.")
                return "error"
            expected = func_symbol["params"]
            given = child_types
            if len(expected) != len(given):
                errores.append(f"[Error: función '{value}' espera {len(expected)} argumentos, recibió {len(given)}.")
            else:
                for i, ((_, texp), tgot) in enumerate(zip(expected, given)):
                    if texp != tgot:
                        errores.append(f"[Error: argumento {i+1} de '{value}' debe ser '{texp}', recibió '{tgot}'.")
            return func_symbol["return_type"]

        elif nodetype == "compound_stmt":
            compound_scope = SymbolTable("compound")
            stack.push(compound_scope)
            for child in node.hijos:
                visit(child, current_func_type)
            stack.pop()  # Cerramos el scope
            return None

        elif nodetype == "fun_declaration":
            func_name = node.hijos[1].valor
            func_symbol = stack.lookup(func_name)
            return_type = func_symbol["return_type"] if func_symbol else "void"
            body = node.hijos[-1]
            visit(body, current_func_type=return_type)
            return None

        # Default: propagar primer tipo hijo
        return child_types[0] if child_types else None

    visit(ast)
    return errores

#Funcion para imprimir la tabla de simbolos
def printSymbolTables(stack):
    print("\nTabla de Símbolos (Scope Stack):")
    #Recorremos nuestra pila de tablas de simbolos
    for i, table in enumerate(stack.stack):
        print(f"\nScope {i} - {table.scope_name}")
        for name, info in table.symbols.items():
            print(f"  {name}: {info}")
