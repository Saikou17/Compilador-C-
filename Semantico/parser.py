from globalTypes import TokenType
from lexer import getToken

class ASTNode:
    def __init__(self, tipo, valor=None):
        self.tipo = tipo
        self.valor = valor
        self.hijos = []

    def agregar(self, nodo):
        if nodo is not None:
            self.hijos.append(nodo)

# Variables globales para el token actual
current_token = None
current_lexeme = None

# ---------------------------- PARSER ---------------------------- #

def parser(buffer, imprime=False):
    global current_token, current_lexeme
    current_token, current_lexeme = getToken(buffer, imprime)
    return program(buffer, imprime)

# ---------------------------- UTILIDADES ---------------------------- #

def match(buffer, expected_type, imprime):
    global current_token, current_lexeme
    if current_token == expected_type:
        current_token, current_lexeme = getToken(buffer, imprime)
    else:
        raise SyntaxError(f"Error de sintaxis: se esperaba {expected_type.name}, se encontró {current_token.name}")

def consume(buffer, expected_lexeme, imprime):
    global current_token, current_lexeme
    if current_lexeme == expected_lexeme:
        current_token, current_lexeme = getToken(buffer, imprime)
    else:
        raise SyntaxError(f"Error de sintaxis: se esperaba '{expected_lexeme}', se encontró '{current_lexeme}'")

def is_type_specifier(lexeme):
    return lexeme in ["int", "void"]

def is_control_keyword(lexeme):
    return lexeme in ["if", "else", "while", "for"]

def is_storage_class(lexeme):
    return lexeme in ["static", "auto", "const"]

def is_function_keyword(lexeme):
    return lexeme in ["void", "main", "return"]

# ---------------------------- REGLAS GRAMATICALES ---------------------------- #

def program(buffer, imprime):
    global current_token, current_lexeme
    nodo = ASTNode("program")
    nodo.agregar(declaration_list(buffer, imprime))
    return nodo

def declaration_list(buffer, imprime):
    global current_token, current_lexeme
    nodo = ASTNode("declaration_list")
    while current_token != TokenType.ENDFILE:
        nodo.agregar(declaration(buffer, imprime))
    return nodo

def declaration(buffer, imprime):
    if peek_next_token_is_function(buffer):
        return fun_declaration(buffer, imprime)
    else:
        return var_declaration(buffer, imprime)

def var_declaration(buffer, imprime):
    nodo = ASTNode("var_declaration")
    nodo.agregar(type_specifier(buffer, imprime))
    
    if current_token == TokenType.IDENTIFIER:
        nodo.agregar(ASTNode("ID", current_lexeme))
        match(buffer, TokenType.IDENTIFIER, imprime)
    else:
        raise SyntaxError("Se esperaba un identificador.")

    if current_lexeme == "[":
        consume(buffer, "[", imprime)
        if current_token == TokenType.NUMBER:
            nodo.agregar(ASTNode("NUM", current_lexeme))
            match(buffer, TokenType.NUMBER, imprime)
            consume(buffer, "]", imprime)
            consume(buffer, ";", imprime)
        else:
            raise SyntaxError("Se esperaba un número para tamaño de arreglo.")
    elif current_lexeme == "=":
        nodo.agregar(ASTNode("=", current_lexeme))
        nodo.agregar(expression(buffer, imprime))
        consume(buffer, ";", imprime)
    else:
        consume(buffer, ";", imprime)

    return nodo

def type_specifier(buffer, imprime):
    if current_lexeme in ["int", "void"]:
        nodo = ASTNode("type_specifier", current_lexeme)
        if current_lexeme == "int":
            match(buffer, TokenType.DATA_TYPE_KEY, imprime)
        else:  # void
            match(buffer, TokenType.FUNCTION_TYPE_KEY, imprime)
        return nodo
    raise SyntaxError("Se esperaba 'int' o 'void' como especificador de tipo")

def fun_declaration(buffer, imprime):
    nodo = ASTNode("fun_declaration")
    nodo.agregar(type_specifier(buffer, imprime))
    
    if current_token == TokenType.IDENTIFIER:
        nodo.agregar(ASTNode("ID", current_lexeme))
        match(buffer, TokenType.IDENTIFIER, imprime)
    else:
        raise SyntaxError("Se esperaba un identificador para la función")
    
    consume(buffer, "(", imprime)
    nodo.agregar(params(buffer, imprime))
    consume(buffer, ")", imprime)
    nodo.agregar(compound_stmt(buffer, imprime))
    
    return nodo

def params(buffer, imprime):
    nodo = ASTNode("params")
    if current_lexeme == "void":
        match(buffer, TokenType.FUNCTION_TYPE_KEY, imprime)
        nodo.valor = "void"
    else:
        nodo.agregar(param_list(buffer, imprime))
    return nodo

def param_list(buffer, imprime):
    nodo = ASTNode("param_list")
    nodo.agregar(param(buffer, imprime))
    while current_lexeme == ",":
        consume(buffer, ",", imprime)
        nodo.agregar(param(buffer, imprime))
    return nodo

def param(buffer, imprime):
    nodo = ASTNode("param")
    nodo.agregar(type_specifier(buffer, imprime))
    
    if current_token == TokenType.IDENTIFIER:
        nodo.agregar(ASTNode("ID", current_lexeme))
        match(buffer, TokenType.IDENTIFIER, imprime)
    else:
        raise SyntaxError("Se esperaba un identificador en el parámetro")
    
    if current_lexeme == "[":
        consume(buffer, "[", imprime)
        consume(buffer, "]", imprime)
    
    return nodo

def compound_stmt(buffer, imprime):
    nodo = ASTNode("compound_stmt")
    consume(buffer, "{", imprime)
    
    # Local declarations
    local_decls = local_declarations(buffer, imprime)
    if local_decls.hijos:  # Solo agregar si hay declaraciones
        nodo.agregar(local_decls)
    
    # Statement list
    stmt_list = statement_list(buffer, imprime)
    if stmt_list.hijos:  # Solo agregar si hay statements
        nodo.agregar(stmt_list)
    
    consume(buffer, "}", imprime)
    return nodo

def local_declarations(buffer, imprime):
    nodo = ASTNode("local_declarations")
    while current_lexeme in ["int", "void"]:
        nodo.agregar(var_declaration(buffer, imprime))
    return nodo

def statement_list(buffer, imprime):
    nodo = ASTNode("statement_list")
    while current_lexeme not in ["}", "$"]:
        nodo.agregar(statement(buffer, imprime))
    return nodo

def statement(buffer, imprime):
    if current_lexeme == "{":
        return compound_stmt(buffer, imprime)
    elif current_lexeme == "if":
        return selection_stmt(buffer, imprime)
    elif current_lexeme == "while":
        return iteration_stmt(buffer, imprime)
    elif current_lexeme == "return":
        return return_stmt(buffer, imprime)
    else:
        return expression_stmt(buffer, imprime)

def expression_stmt(buffer, imprime):
    nodo = ASTNode("expression_stmt")
    if current_lexeme != ";":
        nodo.agregar(expression(buffer, imprime))
    consume(buffer, ";", imprime)
    return nodo

def selection_stmt(buffer, imprime):
    nodo = ASTNode("selection_stmt")
    consume(buffer, "if", imprime)
    consume(buffer, "(", imprime)
    nodo.agregar(expression(buffer, imprime))
    consume(buffer, ")", imprime)
    nodo.agregar(statement(buffer, imprime))
    
    if current_lexeme == "else":
        consume(buffer, "else", imprime)
        nodo.agregar(statement(buffer, imprime))
    
    return nodo

def iteration_stmt(buffer, imprime):
    if current_lexeme == "for":
        nodo = ASTNode("iteration_stmt")
        consume(buffer, "for", imprime)
        consume(buffer, "(", imprime)
        nodo.agregar(expression(buffer, imprime))
        consume(buffer, ")", imprime)
        nodo.agregar(statement(buffer, imprime))
        return nodo
    else:
        nodo = ASTNode("iteration_stmt")
        consume(buffer, "while", imprime)
        consume(buffer, "(", imprime)
        nodo.agregar(expression(buffer, imprime))
        consume(buffer, ")", imprime)
        nodo.agregar(statement(buffer, imprime))
        return nodo
    

def return_stmt(buffer, imprime):
    nodo = ASTNode("return_stmt")
    consume(buffer, "return", imprime)
    if current_lexeme != ";":
        nodo.agregar(expression(buffer, imprime))
    consume(buffer, ";", imprime)
    return nodo

# -------------------------------- EXPRESIONES -------------------------------- #

def expression(buffer, imprime):
    global current_token, current_lexeme
    nodo = ASTNode("expression")
    
    # Primero intentamos parsear una asignación (var = expression)
    try:
        # Guardamos la posición actual por si falla
        temp_pos = buffer.posicion
        temp_linea = buffer.linea_actual
        temp_inicio = buffer.inicio_linea
        temp_token, temp_lexeme = current_token, current_lexeme
        
        var_node = var(buffer, imprime)
        if current_lexeme == "=":
            nodo.agregar(var_node)
            consume(buffer, "=", imprime)
            nodo.agregar(expression(buffer, imprime))
            return nodo
        else:
            # Si no es una asignación, retrocedemos
            buffer.posicion = temp_pos
            buffer.linea_actual = temp_linea
            buffer.inicio_linea = temp_inicio
            current_token, current_lexeme = temp_token, temp_lexeme
    except Exception as e:
        # Si falla, continuamos con simple-expression
        pass
    
    # Si no es una asignación, parseamos simple-expression
    return simple_expression(buffer, imprime)

def var(buffer, imprime):
    global current_token, current_lexeme
    nodo = ASTNode("var")
    if current_token == TokenType.IDENTIFIER:
        nodo.agregar(ASTNode("ID", current_lexeme))
        match(buffer, TokenType.IDENTIFIER, imprime)
        
        if current_lexeme == "[":
            consume(buffer, "[", imprime)
            nodo.agregar(expression(buffer, imprime))
            consume(buffer, "]", imprime)
    else:
        raise SyntaxError("Se esperaba un identificador para 'var'")
    
    return nodo

def simple_expression(buffer, imprime):
    global current_token, current_lexeme
    nodo = ASTNode("simple_expression")
    nodo.agregar(additive_expression(buffer, imprime))
    
    if current_token == TokenType.RELATIONAL_OPERATOR:
        nodo.agregar(ASTNode("relop", current_lexeme))
        match(buffer, TokenType.RELATIONAL_OPERATOR, imprime)
        nodo.agregar(additive_expression(buffer, imprime))
    
    return nodo

def additive_expression(buffer, imprime):
    global current_token, current_lexeme
    nodo = ASTNode("additive_expression")
    nodo.agregar(term(buffer, imprime))
    
    while current_token == TokenType.ARITHMETIC_OPERATOR and current_lexeme in ["+", "-"]:
        nodo.agregar(ASTNode("addop", current_lexeme))
        match(buffer, TokenType.ARITHMETIC_OPERATOR, imprime)
        nodo.agregar(term(buffer, imprime))
    
    return nodo

def term(buffer, imprime):
    global current_token, current_lexeme
    nodo = ASTNode("term")
    nodo.agregar(factor(buffer, imprime))
    
    while current_token == TokenType.ARITHMETIC_OPERATOR and current_lexeme in ["*", "/"]:
        nodo.agregar(ASTNode("mulop", current_lexeme))
        match(buffer, TokenType.ARITHMETIC_OPERATOR, imprime)
        nodo.agregar(factor(buffer, imprime))
    
    return nodo

def factor(buffer, imprime):
    global current_token, current_lexeme
    nodo = None
    
    if current_token == TokenType.NUMBER:
        nodo = ASTNode("NUM", current_lexeme)
        match(buffer, TokenType.NUMBER, imprime)
    elif current_token == TokenType.IDENTIFIER:
        id_lexeme = current_lexeme
        match(buffer, TokenType.IDENTIFIER, imprime)
        
        if current_lexeme == "(":  # Llamada a función
            nodo = ASTNode("call", id_lexeme)
            consume(buffer, "(", imprime)
            nodo.agregar(args(buffer, imprime))
            consume(buffer, ")", imprime)
        else:  # Variable simple
            nodo = ASTNode("var", id_lexeme)
            if current_lexeme == "[":  # Acceso a arreglo
                consume(buffer, "[", imprime)
                nodo.agregar(expression(buffer, imprime))
                consume(buffer, "]", imprime)
    elif current_lexeme == "(":
        consume(buffer, "(", imprime)
        nodo = expression(buffer, imprime)
        consume(buffer, ")", imprime)
    else:
        raise SyntaxError(f"Factor no válido: {current_lexeme}")
    
    return nodo

def args(buffer, imprime):
    nodo = ASTNode("args")
    if current_lexeme != ")":
        nodo.agregar(arg_list(buffer, imprime))
    return nodo

def arg_list(buffer, imprime):
    nodo = ASTNode("arg_list")
    nodo.agregar(expression(buffer, imprime))
    
    while current_lexeme == ",":
        consume(buffer, ",", imprime)
        nodo.agregar(expression(buffer, imprime))
    
    return nodo

# ------------------ LOOKAHEAD SIMPLE PARA FUNCIÓN ------------------ #

def peek_next_token_is_function(buffer):
    global current_token, current_lexeme
    original_pos = buffer.posicion
    original_linea = buffer.linea_actual
    original_inicio = buffer.inicio_linea
    
    # Guardar el token actual
    temp_token, temp_lexeme = current_token, current_lexeme
    
    # Obtener los siguientes tokens
    t1, l1 = getToken(buffer)
    t2, l2 = getToken(buffer)
    
    # Restaurar posición del buffer
    buffer.posicion = original_pos
    buffer.linea_actual = original_linea
    buffer.inicio_linea = original_inicio
    
    # Restaurar token actual
    current_token, current_lexeme = temp_token, temp_lexeme
    
    # Verificar si es una declaración de función
    return (current_lexeme in ["int", "void"] and 
            t1 == TokenType.IDENTIFIER and 
            l2 == "(")