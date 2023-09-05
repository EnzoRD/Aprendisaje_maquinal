from bs4 import BeautifulSoup 
import csv
import spacy
from spacy.matcher import Matcher
from spacy.tokens import Span
import json
#import pandas as pd
# Cargar el modelo pre-entrenado de Spacy en español
nlp = spacy.load('es_core_news_sm')
# Cargar el texto de la oferta laboral desde un archivo
with open(r"./ofertas-2021-02-08.html","r", encoding="utf8") as f:
    # leer el archivo HTML
    html = f.read()
    # analizar el HTML con BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    # extraer el texto del HTML
    text = soup.get_text()
#--------------------------------------------------------
#----------------------------------------------------------------
# Cargar los patrones de reglas desde el archivo JSON
ruta =  "datos\data_patrones.json"
with open(ruta, 'r' ) as f:
    patrones = json.load(f)

#----------------------------------------------------------------
# Definir una función de callback para procesar el resultado del Matcher
def procesar_entidad(matcher, doc, i, matches):
    # Crear un objeto Span para representar la entidad encontrada
    start, end = matches[i][1], matches[i][2]
    entidad = Span(doc, start, end, label="MI_ENTIDAD")

    # Agregar la entidad al documento
    doc.ents = list(doc.ents) + [entidad]

# Agregar los patrones al Matcher
matcher = Matcher(nlp.vocab)
for patron in patrones:
    matcher.add(patron["nombre"], patron["patron"], on_match=procesar_entidad)
#----------------------------------------------------------------
# Procesar el texto con el modelo de Spacy
doc = nlp(text)

# Imprimir las entidades nombradas
# for ent in doc.ents:
#     print(ent.text, ent.start_char, ent.end_char, ent.label_)
entities = []
for ent in doc.ents:
    entities.append((ent.text, ent.label_))
df = pd.DataFrame(entities, columns=['Entidad', 'Tipo'])
df.to_csv('entidades.csv', index=False)