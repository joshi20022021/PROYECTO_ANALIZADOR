from Tokens import Tokens
from Error import Error

class AnalizadorLexico:
    def __init__(self):
        self.tokens = []
        self.errores = []
        self.linea = 1
        self.columna = 1
        self.estado = 0
        self.buffer = ''
        self.palabras_clave = {
            'Inicio': 'Inicio',
            'Fin': 'Fin',
            'Encabezado': 'Encabezado',
            'Cuerpo': 'Cuerpo',
            'Titulo': 'Titulo',
            'Fondo': 'Fondo',
            'Parrafo': 'Parrafo',
            'Texto': 'Texto',
            'Negrita': 'Negrita',
            'Subrayado': 'Subrayado',
            'Tachado': 'Tachado',
            'Cursiva': 'Cursiva',
            'Salto': 'Salto',
            'Tabla': 'Tabla',
            'elemento': 'elemento',
            'llave_abierta': '{',
            'llave_cerrada': '}',
            'corchete_abierto': '[',
            'corchete_cerrado': ']',
            'dos_puntos': ':',
            'punto_y_coma': ';',
            'comillas': '"'
        }


    def analizarTexto(self, texto):
        self.codigo = texto
        self.analizar()

    def agregarError(self, caracter):
        self.errores.append(Error(f'Caracter sin reconocer: {caracter}', self.linea, self.columna))

    def agregarToken(self, tipo, token):
        self.tokens.append(Tokens(tipo, token, self.linea, self.columna))

    def analizar(self):
        palabra_reservada = ''
        lexema = ''
        estado = 0
        for caracter in self.codigo:
            if estado == 0:
                if caracter.isalpha() or caracter == '_':
                    lexema += caracter
                    estado = 1
                elif caracter in ['{', '}', '[', ']', ':', ',', '"']:
                    self.agregarToken(caracter, caracter)
                elif caracter in ['\n', ' ', '\t']:
                    if caracter == '\n':
                        self.linea += 1
                        self.columna = 1
                    else:
                        self.columna += 1
                else:
                    self.agregarError(caracter)
            elif estado == 1:
                if caracter.isalnum() or caracter == '_':
                    lexema += caracter
                elif caracter == ':':
                    palabra_reservada = lexema
                    lexema = ''
                    estado = 2
                elif caracter in ['{', '}', '[', ']', ',', '"']:
                    self.agregarToken(palabra_reservada, lexema)
                    lexema = ''
                    estado = 0
                    self.agregarToken(caracter, caracter)
                elif caracter in ['\n', ' ', '\t']:
                    self.agregarToken(palabra_reservada, lexema)
                    lexema = ''
                    estado = 0
                    if caracter == '\n':
                        self.linea += 1
                        self.columna = 1
                    else:
                        self.columna += 1
                else:
                    self.agregarError(caracter)
        if lexema:
            self.agregarToken(palabra_reservada, lexema)

    def obtenerSalidaTokens(self):
        salida = ''
        for token in self.tokens:
            salida += f'Token: {token.tipo}, Lexema: {token.lexema}, Línea: {token.linea}, Columna: {token.columna}\n'
        return salida

    def obtenerSalidaErrores(self):
        salida = ''
        for error in self.errores:
            salida += f'Error: Carácter no reconocido "{error.caracter}", Línea: {error.linea}, Columna: {error.columna}\n'
        return salida
    
    
    def generarTablaTokens(self):
        tabla_tokens = "Token      | Lexema           | Línea | Columna\n"
        tabla_tokens += "-----------|------------------|-------|---------\n"
        for token in self.tokens:
            tipo_token = self.palabras_clave.get(token.lexema, token.lexema)
            tabla_tokens += f"{tipo_token.ljust(10)}| {token.lexema.ljust(17)}| {token.linea}    | {token.columna}\n"
        return tabla_tokens

    def generarTablaErrores(self):
        tabla_errores = "Carácter  | Línea | Columna\n"
        tabla_errores += "----------|-------|---------\n"
        for error in self.errores:
            tabla_errores += f"{error.caracter.ljust(9)}| {error.linea}    | {error.columna}\n"
        return tabla_errores
        
    def guardarTablaTokens(self, nombre_archivo="tabla_tokens.txt"):
        with open(nombre_archivo, "w") as archivo:
            archivo.write(self.generarTablaTokens())

    def guardarTablaErrores(self, nombre_archivo="tabla_errores.txt"):
        with open(nombre_archivo, "w") as archivo:
            archivo.write(self.generarTablaErrores())
