import tkinter as tk
from tkinter import filedialog, ttk
import json
from traductor import HTMLGenerator, generar_json
from AnalizadorLexico import AnalizadorLexico
import os
import random
import string

class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        """Redraw line numbers"""
        self.delete("all")
        i = self.textwidget.index("@0,0")
        while True:
            dline = self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2,y,anchor="nw", text=linenum)
            i = self.textwidget.index("%s+1line" % i)

class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.line_numbers = TextLineNumbers(self.master, width=30)
        self.line_numbers.attach(self)
        self.bind("<KeyRelease>", self.on_key_release)
        self.bind("<MouseWheel>", self.on_key_release)

    def on_key_release(self, event=None):
        self.line_numbers.redraw()

    def get_line_numbers_widget(self):
        return self.line_numbers

def abrir_archivo():
    filename = filedialog.askopenfilename(initialdir="/", title="Seleccione archivo", 
                                          filetypes=(("JSON files", "*.json"), ("All files", "*.*")))
    if filename:
        with open(filename, 'r') as file:
            contenido = file.read()
            texto_original.delete('1.0', tk.END)
            texto_original.insert(tk.END, contenido)

def traducir():
    # Obtener el texto a traducir del campo de texto original
    texto_a_traducir = texto_original.get('1.0', tk.END)

    # Importar la clase AnalizadorLexico
    from AnalizadorLexico import AnalizadorLexico

    # Crear una instancia de AnalizadorLexico y llamar al método analizarTexto
    analizador = AnalizadorLexico()
    analizador.analizarTexto(texto_a_traducir)

    # Guardar las tablas de tokens y errores en archivos de texto
    analizador.guardarTablaTokens("tabla_tokens.txt")
    analizador.guardarTablaErrores("tabla_errores.txt")
    
    # Convertir el texto a JSON
    json_data = generar_json(texto_a_traducir)

    if json_data:
        # Crear una instancia de la clase HTMLGenerator con el JSON generado
        generator = HTMLGenerator(json_data)

        # Generar el HTML
        html = generator.generar_html()

        # Mostrar el HTML generado en el campo de texto traducido
        texto_traducido.delete('1.0', tk.END)
        texto_traducido.insert(tk.END, html)

        # Generar un nombre de archivo aleatorio
        random_filename = ''.join(random.choices(string.ascii_letters + string.digits, k=8)) + ".html"

        # Guardar el HTML generado en un archivo con el nombre aleatorio
        with open(random_filename, 'w') as f:
            f.write(html)
            print(f"HTML generado y guardado en '{random_filename}'")

        # Realizar el análisis léxico
        analizador = AnalizadorLexico()
        analizador.codigo = html
        analizador.analizar()

        # Generar las tablas de tokens y errores
        tabla_tokens = analizador.generarTablaTokens()
        tabla_errores = analizador.generarTablaErrores()

        # Guardar las tablas en archivos o imprimir en la salida
        with open("tabla_tokens.html", "w") as file_tokens:
            file_tokens.write(tabla_tokens)

        with open("tabla_errores.html", "w") as file_errores:
            file_errores.write(tabla_errores)

        print("Tablas generadas exitosamente.")
    else:
        print("No se pudo traducir el texto debido a un error en el formato JSON.")

def salir():
    root.destroy()

def borrar_contenido():
    texto_original.delete('1.0', tk.END)
    texto_traducido.delete('1.0', tk.END)


root = tk.Tk()
root.title("Traductor HTML")
root.geometry("1080x540")
root.configure(bg='#E0E0E0')

main_frame = ttk.Frame(root, padding="10")
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Títulos de las secciones
label_texto_original = tk.Label(main_frame, text="Texto de Entrada", font=('Arial', 12), bg='#E0E0E0')
label_texto_original.grid(row=0, column=0, sticky="ew")
label_texto_traducido = tk.Label(main_frame, text="Traducción", font=('Arial', 12), bg='#E0E0E0')
label_texto_traducido.grid(row=0, column=1, sticky="ew")

# Configuración del frame y widgets de Texto de Entrada
frame_texto_original = ttk.Frame(main_frame)
frame_texto_original.grid(row=1, column=0, sticky="nsew", padx=(10,5), pady=10)
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_rowconfigure(1, weight=1)

scroll_texto_original = tk.Scrollbar(frame_texto_original)
texto_original = CustomText(frame_texto_original, yscrollcommand=scroll_texto_original.set)
scroll_texto_original.config(command=texto_original.yview)
scroll_texto_original.pack(side="right", fill="y")
texto_original.pack(side="left", fill="both", expand=True)
texto_original.line_numbers.pack(side="left", fill="y")

# Configuración del frame y widgets de Texto Traducido
frame_texto_traducido = ttk.Frame(main_frame)
frame_texto_traducido.grid(row=1, column=1, sticky="nsew", padx=(5,10), pady=10)
main_frame.grid_columnconfigure(1, weight=1)

scroll_texto_traducido = tk.Scrollbar(frame_texto_traducido)
texto_traducido = CustomText(frame_texto_traducido, yscrollcommand=scroll_texto_traducido.set)
scroll_texto_traducido.config(command=texto_traducido.yview)
scroll_texto_traducido.pack(side="right", fill="y")
texto_traducido.pack(side="left", fill="both", expand=True)
texto_traducido.line_numbers.pack(side="left", fill="y")

# Frame para botones
frame_botones = tk.Frame(root, bg='#E0E0E0')
frame_botones.pack(fill='x', pady=5)

# Botones con estilo
boton_abrir = tk.Button(frame_botones, text="Abrir archivo", command=abrir_archivo, bg='black', fg='white', font=('Arial', 10))
boton_abrir.pack(side='left', padx=5)

boton_traducir = tk.Button(frame_botones, text="Traducir", command=traducir, bg='black', fg='white', font=('Arial', 12))
boton_traducir.pack(side='left', padx=5)

boton_borrar = tk.Button(frame_botones, text="Borrar", command=borrar_contenido, bg='gray', fg='white', font=('Arial', 12))
boton_borrar.pack(side='left', padx=5)

boton_salir = tk.Button(frame_botones, text="Salir", command=salir, bg='red', fg='white', font=('Arial', 12))
boton_salir.pack(side='left', padx=5)

root.mainloop()
