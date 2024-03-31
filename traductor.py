import json
import string

class HTMLGenerator:
    def __init__(self, entrada_json):
        self.entrada_json = entrada_json

    def generar_html(self):
        html = ""
        if isinstance(self.entrada_json, dict) and 'Inicio' in self.entrada_json:
            html += "<!DOCTYPE html>\n<html>\n"
            if isinstance(self.entrada_json['Inicio'], dict) and 'Encabezado' in self.entrada_json['Inicio']:
                html += self.procesar_encabezado(self.entrada_json['Inicio']['Encabezado'])
            if isinstance(self.entrada_json['Inicio'], dict) and 'Cuerpo' in self.entrada_json['Inicio']:
                html += "<body>\n"
                html += self.procesar_cuerpo(self.entrada_json['Inicio']['Cuerpo'])
                html += "</body>\n"
            html += "</html>"
        return html

    def procesar_encabezado(self, encabezado):
        html = "<head>\n"
        if 'TituloPagina' in encabezado:
            html += f"<title>{encabezado['TituloPagina']}</title>\n"
        html += "</head>\n"
        return html

    def procesar_cuerpo(self, cuerpo):
        html = ""
        for elemento in cuerpo:
            for tipo, contenido in elemento.items():
                if tipo == 'Titulo':
                    html += self.procesar_titulo(contenido)
                elif tipo == 'Fondo':
                    html += self.procesar_fondo(contenido)
                elif tipo == 'Parrafo':
                    html += self.procesar_parrafo(contenido)
                elif tipo == 'Texto':
                    html += self.procesar_texto(contenido)
                elif tipo == 'Negrita':
                    html += self.procesar_negrita(contenido)
                elif tipo == 'Subrayado':
                    html += self.procesar_subrayado(contenido)
                elif tipo == 'Tachado':
                    html += self.procesar_tachado(contenido)
                elif tipo == 'Cursiva':
                    html += self.procesar_cursiva(contenido)
                elif tipo == 'Salto':
                    html += self.procesar_salto(contenido)
                elif tipo == 'Tabla':
                    html += self.procesar_tabla(contenido)
        return html

    def procesar_titulo(self, titulo):
        # Validación de posición
        posicion = titulo.get('posicion', 'izquierda')  # Si no se proporciona una posición, se utilizará izquierda por defecto
        if posicion not in ['izquierda', 'derecha', 'centro']:
            posicion = 'izquierda'  # Si la posición no es válida, se usa izquierda por defecto
        
        # Validación de tamaño
        tamaño = titulo.get('tamaño', 't1')
        if tamaño not in ['t1', 't2', 't3', 't4', 't5', 't6']:
            tamaño = 't1'  # Si el tamaño no es válido, se usa t1 por defecto
        
        # Validación de color
        color = titulo.get('color', 'black')  # Si no se proporciona un color, se utilizará negro por defecto
        if color not in ['rojo', 'amarillo', 'azul']:
            # Si no es un color predefinido, se considera un código hexadecimal
            if not (color.startswith('#') and len(color) == 7 and all(c in string.hexdigits for c in color[1:])):
                color = 'black'  # Si el color no es válido, se utiliza negro por defecto
        
        html = f"<h1 style=\"text-align: {posicion}; font-size: {self.obtener_tamaño(tamaño)}; color: {color};\">{titulo['texto']}</h1>\n"
        return html



    def procesar_fondo(self, fondo):
        html = f"<body style=\"background-color: {fondo['color']};\">\n"
        return html

    def procesar_parrafo(self, parrafo):
        html = f"<p style=\"text-align: {parrafo['posicion']};\">{parrafo['texto']}</p>\n"
        return html

    def procesar_texto(self, texto):
        fuente = texto.get('fuente', 'valor_por_defecto_fuente')
        tamaño = texto.get('tamaño', 'valor_por_defecto_tamaño')
        color = texto.get('color', 'valor_por_defecto_color')
        contenido = texto.get('texto', 'valor_por_defecto_contenido')

        html = f"<p style=\"font-family: {fuente}; font-size: {self.obtener_tamaño(tamaño)}; color: {color};\">{contenido}</p>\n"
        return html

    def procesar_negrita(self, negrita):
        html = f"<strong>{negrita['texto']}</strong>\n"
        return html

    def procesar_subrayado(self, subrayado):
        html = f"<u>{subrayado['texto']}</u>\n"
        return html

    def procesar_tachado(self, tachado):
        html = f"<strike>{tachado['texto']}</strike>\n"
        return html

    def procesar_cursiva(self, cursiva):
        html = f"<em>{cursiva['texto']}</em>\n"
        return html

    def procesar_salto(self, salto):
        html = "<br>\n" * int(salto['cantidad'])
        return html

    def procesar_tabla(self, tabla):
        html = "<table style=\"border-collapse: collapse; border: 1px solid black;\">\n"  # Agregamos estilos de bordes
        for fila in range(int(tabla['filas'])):
            html += "<tr>\n"
            for columna in range(int(tabla['columnas'])):
                # Buscamos el contenido de la celda correspondiente
                contenido_celda = ""
                for elemento in tabla['elementos']:
                    if elemento['fila'] == str(fila + 1) and elemento['columna'] == str(columna + 1):
                        contenido_celda = elemento.get(f"Texto mostrado en fila {fila + 1} columna {columna + 1}", "")
                        break
                # Agregamos el contenido de la celda a la tabla con estilos de celda
                html += f"<td style=\"border: 1px solid black; padding: 8px;\">{contenido_celda}</td>\n"  # Estilos de celda
            html += "</tr>\n"
        html += "</table>\n"
        return html




    def obtener_tamaño(self, tamaño):
        tamaños = {
            't1': '24px',
            't2': '20px',
            't3': '16px',
            't4': '14px',
            't5': '12px',
            't6': '10px'
        }
        return tamaños.get(tamaño, '16px')

def generar_json(texto):
    # Intenta cargar el texto como JSON
    try:
        json_data = json.loads(texto)
        return json_data
    except json.JSONDecodeError as e:
        print("Error al decodificar el JSON:", e)
        return None
