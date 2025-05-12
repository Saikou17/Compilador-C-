from enum import Enum

#Creamos una clase para definir los tipos de tokens del lenguaje C-
class TokenType(Enum):
    # Grupo de palabras reservadas
    DATA_TYPE_KEY = "int float char"
    CONTROL_TYPE_KEY = "if else while"
    STORAGE_TYPE_KEY = "static auto const"
    FUNCTION_TYPE_KEY = "void main return"
    # Grupo de operadores
    ARITHMETIC_OPERATOR = "+ - * / %"
    RELATIONAL_OPERATOR = "< > <= >= == !="
    LOGICAL_OPERATOR = "&& ||"
    ASSIGNMENT_OPERATOR = "= += -= *= /= %="
    PUNCTUATION_OPERATOR = "; , . ( ) { } [ ]"
    # Grupo de otros
    IDENTIFIER = "a-zA-Z_"
    STRING = " \".*\" "
    CHARACTER = " \'.\' "
    NUMBER = "0-9"
    WHITESPACE = "\\t\\n\\r"
    COMMENT = "// /* */"
    ERROR = "Error"
    ENDFILE = "$"  # Fin de archivo
