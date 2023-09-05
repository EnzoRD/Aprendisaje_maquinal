import tkinter as tk
import re
from tkinter import messagebox, filedialog
from bs4 import BeautifulSoup
import csv

def extraer_palabras_clave(nombre_archivo, keywords):
    with open(nombre_archivo, "r", encoding="utf8") as f:
        # leer el archivo HTML
        html = f.read()

        # analizar el HTML con BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # extraer el texto del HTML
        text = soup.get_text()

        # buscar las palabras clave en el texto
        keywords_encontradas = {}
        for keyword in keywords:
            # buscar la palabra clave en el texto utilizando una expresión regular
            matches = re.findall(keyword, text, re.IGNORECASE)
            if matches:
                # si la palabra clave se encuentra en el texto, contar cuántas veces se encontró
                count = len(matches)
                keywords_encontradas[keyword] = count

        # si se encontraron palabras clave, imprimir la palabra clave, el archivo y la cantidad de veces encontrada
        if keywords_encontradas:
            for keyword, count in keywords_encontradas.items():
                print(f"Archivo {nombre_archivo}: Palabra clave '{keyword}' encontrada {count} veces en el texto")
            return (nombre_archivo, keywords_encontradas)

def cargar_palabras_clave(nombre_archivo):
    keywords = []
    with open(nombre_archivo, "r", encoding="utf8") as f:
        reader = csv.reader(f)
        next(reader)  # saltar la primera fila (encabezados)
        for row in reader:
            keywords.append(row[0])
    return keywords

def buscar_palabras_clave():
    # obtener la lista de palabras clave
    keywords = cargar_palabras_clave("palabras_clave.csv")

    # abrir un cuadro de diálogo para seleccionar los archivos HTML
    archivos_html = filedialog.askopenfilenames(filetypes=[("Archivos HTML", "*.html")])

    # procesar cada archivo HTML
    keywords_encontradas = []
    for archivo in archivos_html:
        resultado = extraer_palabras_clave(archivo, keywords)
        if resultado:
            keywords_encontradas.append(resultado)

    # guardar las palabras clave encontradas en un archivo CSV
    guardar_palabras_clave(keywords_encontradas)

def actualizar_palabras_clave():
    # obtener la lista de palabras clave actual
    keywords = cargar_palabras_clave("palabras_clave.csv")

    # abrir un cuadro de diálogo para que el usuario ingrese las nuevas palabras clave
    nueva_keywords = messagebox.askstring("Actualizar palabras clave", "Ingrese las nuevas palabras clave separadas por coma:")

    # si el usuario ingresó nuevas palabras clave, agregarlas a la lista de palabras clave
    if nueva_keywords:
        nuevas_palabras_clave = [k.strip() for k in nueva_keywords.split(",")]
        keywords += nuevas_palabras_clave

        # guardar las palabras clave actualizadas en el archivo CSV
        with open("palabras_clave.csv", 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Palabra clave"])
            for keyword in keywords:
                writer.writerow([keyword])

    keywords_entry.delete(0, tk.END)
    keywords_entry.insert(0, ", ".join(keywords))

def guardar_palabras_clave(keywords_encontradas):
    # abrir un cuadro de diálogo para guardar el archivo CSV
    nombre_archivo = filedialog.asks

# crear la ventana principal
root = tk.Tk()
root.title("Buscador de palabras clave")

# crear los widgets de la interfaz de usuario
titulo_label = tk.Label(root, text="Ingrese las palabras clave:")
keywords_entry = tk.Entry(root)
buscar_button = tk.Button(root, text="Buscar", command=buscar_palabras_clave)
actualizar_button = tk.Button(root, text="Actualizar palabras clave", command=actualizar_palabras_clave)

# colocar los widgets en la ventana
titulo_label.pack()
keywords_entry.pack()
buscar_button.pack()
actualizar_button.pack()

# iniciar el bucle de eventos de la interfaz de usuario
root.mainloop()