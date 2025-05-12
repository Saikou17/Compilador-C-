from enum import Enum

#Creamos una clase para definir los tipos de tokens del lenguaje C-
class TokenType(Enum):
    # Grupo de palabras reservadas
    DATA_TYPE_KEY = "int:int, float:flotante, char:carácter, double:doble"
    CONTROL_TYPE_KEY = "if:si, else:sino, for:para, while:mientras"
    STORAGE_TYPE_KEY = "static:estático, auto:automático, const:constante"
    FUNCTION_TYPE_KEY = "void:vacío, main:principal, return:retorno"
    # Grupo de operadores
    ARITHMETIC_OPERATOR = "+:suma, -:resta, *:multiplicación, /:división, %:módulo"
    RELATIONAL_OPERATOR = "<:menor, >:mayor, <=:menor_igual, >=:mayor_igual, ==:igual, !=:diferente"
    LOGICAL_OPERATOR = "&&:y, ||:o"
    BITWISE_OPERATOR = "&:y_bit, |:o_bit, ^:xor_bit, ~:no_bit, <<:desplaza_izquierda, >>:desplaza_derecha"
    ASSIGNMENT_OPERATOR = "=:asignar, +=:asignar_suma, -=:asignar_resta, *=:asignar_multiplicación, /=:asignar_división"
    PUNCTUATION_OPERATOR = ";:punto_y_coma, ,:coma, .:punto, (:paréntesis_abre, ):paréntesis_cierra, {:llave_abre, }:llave_cierra, [:corchete_abre, ]:corchete_cierra"
    # Grupo de otros
    IDENTIFIER = "a-zA-Z_:identificador"
    STRING = "\".*\":cadena"
    CHARACTER = "\'.\':carácter"
    NUMBER = "0-9:número"
    WHITESPACE = "\\t\\n\\r :espacio_blanco"
    COMMENT = "//:comentario_línea, /*:comentario_bloque_inicio, */:comentario_bloque_fin"
    ERROR = "Error:error"
    ENDFILE = "$:fin_archivo"  # Fin de archivo
