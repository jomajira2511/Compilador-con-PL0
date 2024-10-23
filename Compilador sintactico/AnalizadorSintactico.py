import ply.yacc as yacc  # Importamos el módulo yacc de PLY para el análisis sintáctico
import os
import codecs  # Para manejar archivos con codificación
from AnalizadorLexico import tokens  # Importamos los tokens definidos en el analizador léxico

# Precedencia de operadores
precedence = (
    ('right', 'ASSIGN'),    # Operador de asignación, con asociatividad hacia la derecha
    ('right', 'UPDATE'),    # Operador de actualización (:=), con asociatividad hacia la derecha
    ('left', 'NE'),         # Operador de desigualdad (<>)
    ('left', 'LT', 'LTE', 'GT', 'GTE'),  # Operadores de comparación (<, <=, >, >=)
    ('left', 'PLUS', 'MINUS'),  # Suma y resta, con asociatividad hacia la izquierda
    ('left', 'TIMES', 'DIVIDE'),  # Multiplicación y división, también asociativos a la izquierda
    ('right', 'ODD'),        # Operador especial ODD, con asociatividad a la derecha
    ('left', 'LPARENT', 'RPARENT'),  # Paréntesis, para manejar expresiones agrupadas
)

# Reglas de producción para el analizador sintáctico

# La regla principal que define un programa
def p_program(p):
    '''program : block'''
    print("program")

# Regla para un bloque de código (constantes, variables, procedimientos y sentencias)
def p_block(p):
    '''block : constDecl varDecl procDecl statement'''
    print("block")

# Reglas para la declaración de constantes

# Definición de una lista de constantes
def p_constDecl(p):
    '''constDecl : CONST constAssignmentList SEMICOLON'''
    print("constDecl")

# Regla vacía para casos donde no haya declaración de constantes
def p_constDeclEmpty(p):
    '''constDecl : empty'''
    print("nulo")

# Asignación de una constante
def p_constAssignmentList1(p):
    '''constAssignmentList : ID ASSIGN NUMBER'''
    print("constAssignmentList 1")

# Asignación de múltiples constantes separadas por comas
def p_constAssignmentList2(p):
    '''constAssignmentList : constAssignmentList COMMA ID ASSIGN NUMBER'''
    print("constAssignmentList 2")

# Declaración de variables

# Lista de variables separadas por punto y coma
def p_varDecl1(p):
    '''varDecl : VAR identList SEMICOLON'''
    print("varDecl 1")

# Regla vacía para casos donde no haya declaración de variables
def p_varDeclEmpty(p):
    '''varDecl : empty'''
    print("nulo")

# Lista de identificadores de variables

# Un solo identificador
def p_identList1(p):
    '''identList : ID'''
    print("identList 1")

# Lista de identificadores separados por comas
def p_identList2(p):
    '''identList : identList COMMA ID'''
    print("identList 2")

# Declaración de procedimientos

# Definición de un procedimiento con su cuerpo (bloque de código)
def p_procDecl1(p):
    '''procDecl : PROCEDURE ID SEMICOLON block SEMICOLON'''
    print("procDecl 1")

# Regla vacía para casos donde no haya procedimientos
def p_procDeclEmpty(p):
    '''procDecl : empty'''
    print("nulo")

# Sentencias

# Asignación de una expresión a una variable
def p_statement1(p):
    '''statement : ID UPDATE expression'''
    print("statement 1")

# Llamada a un procedimiento
def p_statement2(p):
    '''statement : CALL ID'''
    print("statement 2")

# Bloque de sentencias agrupadas por BEGIN y END
def p_statement3(p):
    '''statement : BEGIN statementList END'''
    print("statement 3")

# Sentencia condicional IF-THEN
def p_statement4(p):
    '''statement : IF condition THEN statement'''
    print("statement 4")

# Sentencia WHILE con condición y cuerpo
def p_statement5(p):
    '''statement : WHILE condition DO statement'''
    print("statement 5")

# Regla vacía para sentencias opcionales
def p_statementEmpty(p):
    '''statement : empty'''
    print("nulo")

# Lista de sentencias

# Una única sentencia
def p_statementList1(p):
    '''statementList : statement'''
    print("statementList 1")

# Múltiples sentencias separadas por punto y coma
def p_statementList2(p):
    '''statementList : statementList SEMICOLON statement'''
    print("statementList 2")

# Condiciones

# Condición ODD (paridad impar)
def p_condition1(p):
    '''condition : ODD expression'''
    print("condition 1")

# Condición de comparación entre dos expresiones
def p_condition2(p):
    '''condition : expression relation expression'''
    print("condition 2")

# Relaciones (comparaciones)

# Relación de asignación
def p_relation1(p):
    '''relation : ASSIGN'''
    print("relation 1")

# Relación de desigualdad (<>)
def p_relation2(p):
    '''relation : NE'''
    print("relation 2")

# Relación menor que (<)
def p_relation3(p):
    '''relation : LT'''
    print("relation 3")

# Relación mayor que (>)
def p_relation4(p):
    '''relation : GT'''
    print("relation 4")

# Relación menor o igual que (<=)
def p_relation5(p):
    '''relation : LTE'''
    print("relation 5")

# Relación mayor o igual que (>=)
def p_relation6(p):
    '''relation : GTE'''
    print("relation 6")

# Expresiones

# Una expresión simple
def p_expression1(p):
    '''expression : term'''
    print("expression 1")

# Expresión con un operador unario (suma o resta)
def p_expression2(p):
    '''expression : addingOperator term'''
    print("expression 2")

# Expresión con un operador binario (suma o resta entre expresiones)
def p_expression3(p):
    '''expression : expression addingOperator term'''
    print("expression 3")

# Operadores de suma/resta

# Operador suma
def p_addingOperator1(p):
    '''addingOperator : PLUS'''
    print("addingOperator 1")

# Operador resta
def p_addingOperator2(p):
    '''addingOperator : MINUS'''
    print("addingOperator 2")

# Términos

# Un término simple
def p_term1(p):
    '''term : factor'''
    print("term 1")

# Un término multiplicado o dividido por otro factor
def p_term2(p):
    '''term : term multiplyingOperator factor'''
    print("term 2")

# Operadores de multiplicación/división

# Operador multiplicación
def p_multiplyingOperator1(p):
    '''multiplyingOperator : TIMES'''
    print("multiplyingOperator 1")

# Operador división
def p_multiplyingOperator2(p):
    '''multiplyingOperator : DIVIDE'''
    print("multiplyingOperator 2")

# Factores

# Un factor puede ser una variable (ID)
def p_factor1(p):
    '''factor : ID'''
    print("factor 1")

# O puede ser un número
def p_factor2(p):
    '''factor : NUMBER'''
    print("factor 2")

# O una expresión agrupada en paréntesis
def p_factor3(p):
    '''factor : LPARENT expression RPARENT'''
    print("factor 3")

# Producción vacía
def p_empty(p):
    '''empty :'''
    pass

# Manejo de errores de sintaxis
def p_error(p):
    if p:
        print(f"Error de sintaxis en '{p.value}' en la línea {p.lineno}")
    else:
        print("Error de sintaxis en EOF")

# Función para buscar archivos de prueba en el directorio
def buscarFicheros(directorio):
    ficheros = []
    cont = 1

    # Obtener los archivos del directorio especificado
    for base, dirs, files in os.walk(directorio):
        ficheros = files
        break

    for file in files:
        print(f"{cont}. {file}")
        cont += 1

    # Solicitar al usuario que seleccione un archivo
    while True:
        try:
            numArchivo = int(input('\nNúmero del test: '))
            if 1 <= numArchivo <= len(files):
                print(f"Has escogido \"{files[numArchivo-1]}\" \n")
                return files[numArchivo-1]
        except (ValueError, IndexError):
            print("Por favor, selecciona un número válido.")

# Selección y apertura del archivo de prueba
directorio = 'C://Users//_//Desktop//Compilador sintactico//test//'
archivo = buscarFicheros(directorio)  # Selecciona un archivo del directorio
test = directorio + archivo
with codecs.open(test, "r", "utf-8") as fp:  # Abrimos el archivo seleccionado en modo lectura
    cadena = fp.read()

# Inicialización del parser
parser = yacc.yacc()
result = parser.parse(cadena)  # Se analiza la cadena del archivo

print(result)  # Imprimir
