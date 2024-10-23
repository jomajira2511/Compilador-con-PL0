import ply.lex as lex  # Importamos la librería PLY para el análisis léxico
import re  # Importamos el módulo de expresiones regulares para manejar patrones

# Definición de palabras reservadas con su representación
reservadas = {
    'begin': 'BEGIN',
    'end': 'END',
    'if': 'IF',
    'then': 'THEN',
    'while': 'WHILE',
    'do': 'DO',
    'call': 'CALL',
    'const': 'CONST',
    'var': 'VAR',
    'procedure': 'PROCEDURE',
    # Se puede eliminar 'OUT', 'IN', 'ELSE' si no son utilizados
}

# Definición de tokens regulares. Aquí incluimos tokens como identificadores (ID),
# operadores matemáticos, comparaciones, paréntesis y otros.
tokens = [
    'ID',       # Identificadores
    'NUMBER',   # Números
    'PLUS',     # Suma (+)
    'MINUS',    # Resta (-)
    'TIMES',    # Multiplicación (*)
    'DIVIDE',   # División (/)
    'ODD',      # Operador especial ODD
    'ASSIGN',   # Asignación (=)
    'NE',       # Desigualdad (<>)
    'LT',       # Menor que (<)
    'LTE',      # Menor o igual que (<=)
    'GT',       # Mayor que (>)
    'GTE',      # Mayor o igual que (>=)
    'LPARENT',  # Paréntesis izquierdo '('
    'RPARENT',  # Paréntesis derecho ')'
    'COMMA',    # Coma ','
    'SEMICOLON',# Punto y coma ';'
    'UPDATE'    # Operador de actualización ':='
] + list(reservadas.values())  # Incluimos las palabras reservadas en la lista de tokens

# Definición de los patrones regulares para los tokens
# Cada token tiene su expresión regular (regex) asociada.

t_PLUS = r'\+'           # Suma
t_MINUS = r'-'           # Resta
t_TIMES = r'\*'          # Multiplicación
t_DIVIDE = r'/'          # División
t_ODD = r'ODD'           # Operador especial ODD
t_ASSIGN = r'='          # Asignación
t_NE = r'<>'             # Desigualdad
t_LT = r'<'              # Menor que
t_LTE = r'<='            # Menor o igual que
t_GT = r'>'              # Mayor que
t_GTE = r'>='            # Mayor o igual que
t_LPARENT = r'\('        # Paréntesis izquierdo
t_RPARENT = r'\)'        # Paréntesis derecho
t_COMMA = r','           # Coma
t_SEMICOLON = r';'       # Punto y coma
t_UPDATE = r':='         # Operador de actualización

# Definimos qué ignorar: espacios en blanco y tabulaciones
t_ignore = '\t '         

# Regla para reconocer identificadores (ID) y palabras reservadas
# Un identificador debe comenzar con una letra o guion bajo y puede contener números
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'  # Expresión regular para un ID
    # Verifica si el identificador es una palabra reservada, de lo contrario, es un ID
    t.type = reservadas.get(t.value.lower(), 'ID')  
    return t

# Regla para reconocer números
def t_NUMBER(t):
    r'\d+'  # Expresión regular para números enteros
    t.value = int(t.value)  # Convierte el valor a entero
    return t

# Regla para manejar errores léxicos: cuando se encuentra un caracter ilegal
def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}'")  # Imprime el carácter no válido
    t.lexer.skip(1)  # Salta el carácter no válido y continúa con el análisis

# Inicialización del analizador léxico
analizador = lex.lex()  # Crea el analizador léxico basado en las reglas definidas
