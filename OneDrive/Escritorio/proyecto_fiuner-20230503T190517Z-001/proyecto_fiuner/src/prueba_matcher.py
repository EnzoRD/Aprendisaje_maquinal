import spacy
from spacy.matcher import Matcher
import json

# Cargar el modelo de idioma de Spacy
nlp = spacy.load("es_core_news_sm")

# Crear el objeto Matcher
matcher = Matcher(nlp.vocab)

# Nombre del archivo JSON con los patrones
nombre_archivo = "datos\data_patrones.json"

# Cargar los patrones desde el archivo JSON
with open(nombre_archivo, "r") as archivo:
    patrones = json.load(archivo)

# Agregar los patrones al Matcher
for patron in patrones:
    nombre_entidad = patron["nombre"]
    reglas = patron["patron"]
    
    # Crear una lista de patrones
    lista_patrones = [reglas]
    
    matcher.add(nombre_entidad, lista_patrones)

# Texto de ejemplo para realizar la coincidencia de patrones
texto = "El hospital y la clínica son parte del sistema de salud."

# Procesar el texto con el modelo de Spacy
doc = nlp(texto)

# Realizar la coincidencia de patrones utilizando el Matcher
coincidencias = matcher(doc)

# Iterar sobre las coincidencias encontradas
for nombre_entidad, inicio, fin in coincidencias:
    entidad = doc[inicio:fin]
    print("Entidad encontrada:", entidad.text, "-", nombre_entidad)