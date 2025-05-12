# from globalTypes import *
# from lexer import *

# # Abrimos y leemos el archivo fuente
# with open("sample.c-", "r") as f:
#     programa = f.read()

# progLong = len(programa)

# # Inicializamos variables globales del analizador
# globales(programa, 0, progLong)

# # Llamamos a getToken() hasta llegar al final del archivo
# while True:
#     token, tokenString = getToken(True)
#     if token == TokenType.ENDFILE:
#         break
