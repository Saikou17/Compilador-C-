# Documentacion del Parser (Sintaxis de Lenguaje C -)

## Objetivo

Es un proceso que tiene como objetivo realizar el análisis
sintáctico o gramatical de un programa. En este programa recibiremos una seria de **Tokens** para luego crear un **Arbol Sintatico**.

### Herramientas

- Reglas Sintacticas
- Implementacion de las reglas

### Gramática en forma de reglas de producción

A continuacion vemos una forma de generar las reglas sintacticas a traves de un CFG (Context Free Grammar), el cual expresa un lenguaje implementado y conectado por recursividad. 

```bnf
1.  program           → declaration-list

2.  declaration-list → declaration declaration-list'
    declaration-list' → declaration declaration-list' | ε

3.  declaration      → var-declaration | fun-declaration

4.  var-declaration  → type-specifier ID var-declaration'
    var-declaration' → ; | [ NUM ] ;

     ID: TokenType.IDENTIFIER
     ;, [:, ]: TokenType.PUNCTUATION_OPERATOR
     NUM: TokenType.NUMBER

5.  type-specifier   → int | void

     int: TokenType.DATA_TYPE_KEY
     void: TokenType.FUNCTION_TYPE_KEY

6.  fun-declaration  → type-specifier ID ( params ) compound-stmt

    (:, ): TokenType.PUNCTUATION_OPERATOR

7.  params           → void | param-list

    void: TokenType.FUNCTION_TYPE_KEY

8.  param-list       → param param-list'
    param-list'      → , param param-list' | ε

    ,: TokenType.PUNCTUATION_OPERATOR

9.  param            → type-specifier ID param'
    param'           → [ ] | ε

10. compound-stmt    → { local-declarations statement-list }

    {:, }: TokenType.PUNCTUATION_OPERATOR

11. local-declarations → var-declaration local-declarations | ε

12. statement-list   → statement statement-list | ε

13. statement        → expression-stmt 
                     | compound-stmt 
                     | selection-stmt 
                     | iteration-stmt 
                     | return-stmt

14. expression-stmt  → expression ; | ;

15. selection-stmt   → if ( expression ) statement selection-stmt'
    selection-stmt'  → else statement | ε

    if, else: TokenType.CONTROL_TYPE_KEY

16. iteration-stmt   → while ( expression ) statement

    while: TokenType.CONTROL_TYPE_KEY

17. return-stmt      → return return-stmt'
    return-stmt'     → ; | expression ;

    return: TokenType.FUNCTION_TYPE_KEY

18. expression       → var = expression 
                     | simple-expression

    =: TokenType.ASSIGNMENT_OPERATOR

19. var              → ID var'
    var'             → [ expression ] | ε

20. simple-expression → additive-expression simple-expression'
    simple-expression' → relop additive-expression | ε

21. relop            → <= | < | > | >= | == | !=

    Todos: TokenType.RELATIONAL_OPERATOR

22. additive-expression → term additive-expression'
    additive-expression' → addop term additive-expression' | ε

23. addop            → + | -

    Todos: TokenType.ARITHMETIC_OPERATOR

24. term             → factor term'
    term'            → mulop factor term' | ε

25. mulop            → * | /

    Todos: TokenType.ARITHMETIC_OPERATOR

26. factor           → ( expression ) 
                     | var 
                     | call 
                     | NUM

    NUM: TokenType.NUMBER

27. call             → ID ( args )

28. args             → arg-list | ε

29. arg-list         → expression arg-list'
    arg-list'        → , expression arg-list' | ε

```

```ebnf
(* Programa y declaraciones *)
program = declaration-list ;

declaration-list = declaration { declaration } ;

declaration = var-declaration | fun-declaration ;

(* MODIFICADO: Añadida la inicialización de variables *)
var-declaration = type-specifier ID [ "=" expression ] ";" 
                | type-specifier ID "[" NUM "]" ";" ;

type-specifier = "int" | "void" ;

fun-declaration = type-specifier ID "(" params ")" compound-stmt ;

params = param-list | "void" ;

param-list = param { "," param } ;

param = type-specifier ID 
       | type-specifier ID "[" "]" ;

compound-stmt = "{" local-declarations statement-list "}" ;

local-declarations = { var-declaration } ;

statement-list = { statement } ;

statement = expression-stmt 
          | compound-stmt 
          | selection-stmt 
          | iteration-stmt 
          | return-stmt ;

(* MODIFICADO: Ya existe la opción de expresión vacía *)
expression-stmt = [ expression ] ";" ;

selection-stmt = "if" "(" expression ")" statement 
               | "if" "(" expression ")" statement "else" statement ;

iteration-stmt = "while" "(" expression ")" statement ;

(* AÑADIDO: Soporte para bucles for *)
(* iteration-stmt = "while" "(" expression ")" statement
                | "for" "(" [ expression ] ";" [ expression ] ";" [ expression ] ")" statement ; *)

return-stmt = "return" [ expression ] ";" ;

(* Expressions *)
expression = var "=" expression | simple-expression ;

var = ID 
    | ID "[" expression "]" ;

simple-expression = additive-expression [ relop additive-expression ] ;

relop = "<=" | "<" | ">" | ">=" | "==" | "!=" ;

additive-expression = term { addop term } ;

addop = "+" | "-" ;

term = factor { mulop factor } ;

mulop = "*" | "/" ;

factor = "(" expression ")" | var | call | NUM ;

call = ID "(" args ")" ;

args = [ arg-list ] ;

arg-list = expression { "," expression } ;

```

### Parse Tree vs AST (Arbol Sintactico Abstracto)

Es un arbol que nos describe de manera recursiva la estructura del lenguaje con las reglas antes mencionadas. El recorrido de inorder (hoja izq, padre , hijo der) nos indica la forma en el que el string esta siendo evaluado o recorrido.



### Manejo de errores

En este modulo del compilador vamos a utilizar la estrategia de *modo de panico* el cual consta de la siguiente funcionalidad:

1. Deteccion del error
2. Reporte del error
3. Modo Panico
4. Recuperacion
5. Reanudar analisis
6. Repetir