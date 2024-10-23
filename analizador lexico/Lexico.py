import os
import codecs
import re

# Función para buscar archivos en un directorio
def buscarFicheros(directorio):
    """
    Esta función busca archivos dentro del directorio proporcionado.
    Retorna el archivo seleccionado por el usuario.
    """
    ficheros = []
    respuesta = False
    cont = 1
    
    # Recorre el directorio y obtiene los archivos (ignora los subdirectorios)
    for base, dirs, files in os.walk(directorio):
        ficheros = files  # Guardamos solo los archivos del directorio principal
        break  # No necesitamos recorrer más allá del primer nivel
    
    # Si no se encuentran archivos, notificamos al usuario
    if not ficheros:
        print("No se encontraron archivos en el directorio.")
        return None
    
    # Mostrar los archivos disponibles en el directorio
    print("Archivos disponibles:")
    for file in ficheros:
        print(f"{cont}. {file}")
        cont += 1
    
    # Permitir al usuario seleccionar un archivo
    while not respuesta:
        try:
            numArchivo = int(input('\nNúmero del archivo: '))
            if 1 <= numArchivo <= len(ficheros):  # Validar que el número esté en el rango correcto
                archivoSeleccionado = ficheros[numArchivo-1]
                respuesta = True
            else:
                print("Por favor, selecciona un número válido.")
        except ValueError:
            print("Entrada inválida. Por favor, ingresa un número.")
    
    print(f"\nHas escogido \"{archivoSeleccionado}\" \n")
    return archivoSeleccionado

# Función para mostrar el contenido de un archivo y confirmar la selección
def mostrarContenidoYConfirmar(directorio, archivo):
    """
    Esta función muestra el contenido de un archivo y le pregunta al usuario
    si desea continuar trabajando con dicho archivo.
    """
    rutaArchivo = os.path.join(directorio, archivo)
    
    # Abrir y leer el contenido del archivo
    with codecs.open(rutaArchivo, "r", "utf-8") as fp:
        contenido = fp.read()
    
    # Mostrar el contenido del archivo
    print(f"Contenido del archivo \"{archivo}\":\n")
    print(contenido)
    
    # Preguntar al usuario si desea continuar con el archivo
    while True:
        respuesta = input("\n¿Deseas continuar con este archivo? (s/n): ").lower()
        if respuesta == 's':
            return contenido  # Retornamos el contenido del archivo para su procesamiento
        elif respuesta == 'n':
            return None  # Si elige 'n', retornamos None para permitir seleccionar otro archivo
        else:
            print("Respuesta no válida. Por favor, ingresa 's' o 'n'.")

# Función principal que gestiona la selección y procesamiento del archivo
def procesarArchivo(directorio):
    """
    Función que gestiona la selección de un archivo y su procesamiento
    después de la confirmación por parte del usuario.
    """
    while True:
        # Buscar el archivo en el directorio
        archivo = buscarFicheros(directorio)
        if archivo is None:  # Si no se encontraron archivos, salimos del bucle
            break
        
        # Mostrar contenido del archivo y confirmar si el usuario desea continuar
        contenido = mostrarContenidoYConfirmar(directorio, archivo)
        if contenido is not None:
            # Si el usuario confirma, salimos del bucle y procesamos el archivo
            return contenido
        else:
            print("\nPor favor, selecciona otro archivo.\n")

# Definir la ruta del directorio donde se encuentran los archivos
directorio = 'C:\\Users\\_\\Desktop\\analizador lexico\\test'

# Ejecutar el proceso de selección y lectura de archivo
contenidoArchivo = procesarArchivo(directorio)

# Si el archivo ha sido confirmado y leído, proceder al análisis léxico
if contenidoArchivo:
    print("\nAnalizando contenido léxico...\n")
    
    # Definir palabras clave de MiniPascal
    keywords = {
        'begin', 'end', 'var', 'integer', 'real', 'boolean', 'char', 'if', 'then', 'else', 'while', 'do', 
        'program', 'procedure', 'function', 'true', 'false', 'and', 'or', 'not', 'div', 'mod'
    }

    # Definición de los patrones de tokens
    token_specification = [
        ('COMMENT', r'\{.*?\}'),            # Comentarios entre llaves
        ('MULTILINE_COMMENT', r'\(\*.*?\*\)'), # Comentarios multilínea (* ... *)
        ('NUMBER', r'\d+(\.\d*)?'),         # Números enteros o reales
        ('CHAR', r'\'[^\']\''),             # Constante de carácter (e.g., 'a')
        ('STRING', r'\'[^\']*?\''),         # Cadenas de texto (e.g., 'texto')
        ('ASSIGN', r':='),                  # Operador de asignación
        ('COLON', r':'),                    # Dos puntos
        ('SEMICOLON', r';'),                # Punto y coma
        ('COMMA', r','),                    # Coma
        ('DOT', r'\.'),                     # Punto
        ('LPAREN', r'\('),                  # Paréntesis izquierdo
        ('RPAREN', r'\)'),                  # Paréntesis derecho
        ('LBRACKET', r'\['),                # Corchete izquierdo
        ('RBRACKET', r'\]'),                # Corchete derecho
        ('EQ', r'='),                       # Igual
        ('NEQ', r'<>'),                     # No igual
        ('LT', r'<'),                       # Menor que
        ('GT', r'>'),                       # Mayor que
        ('LTE', r'<='),                     # Menor o igual que
        ('GTE', r'>='),                     # Mayor o igual que
        ('PLUS', r'\+'),                    # Suma
        ('MINUS', r'-'),                    # Resta
        ('MUL', r'\*'),                     # Multiplicación
        ('DIV', r'/'),                      # División
        ('ID', r'[A-Za-z_]\w*'),            # Identificadores
        ('WHITESPACE', r'\s+'),             # Espacios en blanco
        ('MISMATCH', r'.'),                 # Cualquier otro carácter no esperado
    ]

    # Compilar patrones de tokens
    token_re = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)

# Construcción de la expresión regular que captura todos los tokens definidos
# `token_specification` es una lista de tuplas donde cada tupla contiene
# el nombre del token y su expresión regular correspondiente.
token_re = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)

class Lexer:
    def __init__(self, code):
        # Inicializa el analizador léxico con el código fuente proporcionado.
        self.code = code  # Almacena el código fuente.
        self.tokens = []  # Lista vacía para almacenar los tokens generados.
        self.tokenize()  # Llama al método tokenize para empezar el proceso.

    def tokenize(self):
        # Método que se encarga de encontrar y generar los tokens.
        for mo in re.finditer(token_re, self.code):
            # `mo` es el objeto de coincidencia que contiene información sobre el token encontrado.
            kind = mo.lastgroup  # Obtiene el nombre del grupo coincidente (tipo de token).
            value = mo.group(kind)  # Extrae el valor del token encontrado.

            # Clasificación y procesamiento del token encontrado.
            if kind == 'NUMBER':
                # Convierte el valor a float o int según corresponda.
                value = float(value) if '.' in value else int(value)
            elif kind == 'ID' and value in keywords:
                # Si es un identificador y está en la lista de palabras clave, cambia su tipo.
                kind = 'KEYWORD'
            elif kind == 'WHITESPACE' or kind == 'COMMENT' or kind == 'MULTILINE_COMMENT':
                # Si es un espacio en blanco o comentario, se ignora.
                continue
            elif kind == 'MISMATCH':
                # Si se encuentra un carácter inesperado, lanza un error.
                raise RuntimeError(f'Error: caracter inesperado "{value}"')

            # Almacena el token como una tupla (tipo, valor) en la lista de tokens.
            self.tokens.append((kind, value))

    def get_tokens(self):
        # Método para obtener la lista de tokens generados.
        return self.tokens

# Crear una instancia del analizador léxico con el contenido del archivo.
lexer = Lexer(contenidoArchivo)
# Obtener los tokens generados por el analizador léxico.
tokens = lexer.get_tokens()

# Mostrar los tokens generados en la consola.
print("Tokens generados:\n")
for token in tokens:
    print(token)  # Imprime cada token en la consola.
