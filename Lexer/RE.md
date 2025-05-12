# Expresiones Regulares para Tokens

### 1. **Comentario**
- **Regex:** `r'(//[^\n]*|/\*[\s\S]*?\*/)'`
- **Descripción:** Coincide con comentarios de una sola línea (`//...`) y comentarios multilínea (`/*...*/`).

### 2. **Espacios en Blanco**
- **Regex:** `r'\s+'`
- **Descripción:** Coincide con uno o más espacios en blanco, saltos de línea o tabulaciones.

### 3. **Tipos de Datos (int, float, char, double)**
- **Regex:** `r'\b(int|float|char|double)\b'`
- **Descripción:** Coincide con los tipos de datos básicos: `int`, `float`, `char`, y `double`.

### 4. **Estructuras de Control (if, else, for, while)**
- **Regex:** `r'\b(if|else|for|while)\b'`
- **Descripción:** Coincide con las estructuras de control: `if`, `else`, `for`, y `while`.

### 5. **Tipos de Almacenamiento (static, auto, const)**
- **Regex:** `r'\b(static|auto|const)\b'`
- **Descripción:** Coincide con las palabras clave de almacenamiento: `static`, `auto`, y `const`.

### 6. **Tipos de Funciones (void, main, return)**
- **Regex:** `r'\b(void|main|return)\b'`
- **Descripción:** Coincide con los tipos de funciones comunes: `void`, `main`, y `return`.

### 7. **Identificadores**
- **Regex:** `r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'`
- **Descripción:** Coincide con identificadores válidos, comenzando con una letra o guion bajo, seguido de letras, números o guiones bajos.

### 8. **Cadenas de Texto**
- **Regex:** `r'\"([^\\\"]|\\.)*\"'`
- **Descripción:** Coincide con cadenas de texto entre comillas dobles, permitiendo caracteres escapados dentro de la cadena.

### 9. **Caracteres**
- **Regex:** `r'\'([^\\\']|\\.)\''`
- **Descripción:** Coincide con caracteres entre comillas simples, permitiendo caracteres escapados dentro del carácter.

### 10. **Números**
- **Regex:** `r'\b\d+(\.\d+)?(e[+-]?\d+)?\b'`
- **Descripción:** Coincide con números enteros, decimales o notación científica.

### 11. **Operadores Aritméticos**
- **Regex:** `r'[+\-*/%]'`
- **Descripción:** Coincide con los operadores aritméticos: `+`, `-`, `*`, `/`, `%`.

### 12. **Operadores Relacionales**
- **Regex:** `r'(<=|>=|==|!=|<|>)'`
- **Descripción:** Coincide con los operadores relacionales: `<=`, `>=`, `==`, `!=`, `<`, `>`.

### 13. **Operadores Lógicos**
- **Regex:** `r'(&&|\|\||!)'`
- **Descripción:** Coincide con los operadores lógicos: `&&`, `||`, `!`.

### 14. **Operadores de Asignación**
- **Regex:** `r'([+\-*/%]?=)'`
- **Descripción:** Coincide con los operadores de asignación: `=`, `+=`, `-=`, `*=`, `/=`, `%=`.

### 15. **Operadores de Puntuación**
- **Regex:** `r'[;,.(){}[\]]'`
- **Descripción:** Coincide con los operadores de puntuación: `;`, `,`, `.`, `()`, `{}`, `[]`.
