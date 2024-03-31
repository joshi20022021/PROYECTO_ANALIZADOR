class GeneradorHTML:
    @staticmethod
    def generarHTML(tokens, nombre_archivo):
        codigo_html = '<!DOCTYPE html>\n<html>\n<head>\n<meta charset="UTF-8">\n<title>Analizador Léxico - Tokens</title>\n</head>\n<body>\n'
        for token in tokens:
            codigo_html += f'<p>Token: {token.tipo}, Lexema: {token.lexema}, Línea: {token.linea}, Columna: {token.columna}</p>\n'
        codigo_html += '</body>\n</html>'
        with open(nombre_archivo, 'w') as archivo:
            archivo.write(codigo_html)

    @staticmethod
    def generarReporteErrores(errores, nombre_archivo):
        codigo_html = '<!DOCTYPE html>\n<html>\n<head>\n<meta charset="UTF-8">\n<title>Analizador Léxico - Errores</title>\n</head>\n<body>\n'
        for error in errores:
            codigo_html += f'<p>Error: Carácter no reconocido "{error.caracter}", Línea: {error.linea}, Columna: {error.columna}</p>\n'
        codigo_html += '</body>\n</html>'
        with open(nombre_archivo, 'w') as archivo:
            archivo.write(codigo_html)
