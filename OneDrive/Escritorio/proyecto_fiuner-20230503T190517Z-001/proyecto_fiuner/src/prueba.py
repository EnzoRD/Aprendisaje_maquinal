import spacy
import re
import pandas as pd
# cargar el modelo de lenguaje en español
nlp = spacy.load("es_core_news_sm")
texto = """
Posiciones a cubrir en empresa multinacional de Equipos Médicos.

- Gerente de Ventas.
Tendrá a su cargo 15 Ejecutivos de Ventas, 1 Analista de Negocios y 1 Especialista de producto. Asimismo llevará adelante proyectos de mejora de procesos interdepartamentales y el desarrollo de competencias de su equipo.

Se orienta a graduados de Bioingeniería, Ing. Biomédica, Farmacia, Bioquímica o Lic. en Comercialización con 5 años de experiencia en empresas de dispositivos médicos, inglés intermedio y disponibilidad para viajar.

Se ofrece auto compañía entre otros beneficios y posibilidades crecimiento en un entorno de primer nivel.

Los interesados pueden enviar CV a selector@intersearch.com.ar con Asunto "Gte. Ventas 04"


- Analista de Asuntos Regulatorios Sr 

Para llevar adelante un proyecto de cambio de registros ante las autoridades sanitarias.

Serán sus funciones:

- Preparar presentaciones para asegurar aprobaciones para el lanzamiento
de productos
- Mantener actualizada la lista de requisitos para el armado del expediente de registro de producto y comunicar los requisitos al equipo de asuntos regulatorios de la unidad de negocios.
- Verificar y revisar la documentación necesaria para cumplir con ANMAT, con la Autoridad Sanitaria de Chile y/o regulaciones corporativas
- Identificar los cambios de producto que representen un impacto en la región y distinguir cuándo un cambio requiere aprobación antes de la comercialización.
- Revisar etiquetado, los materiales promocionales, los cambios del
producto y la documentación de los cambios que requieren la aprobación
de la agencia regulatoria.

Se orienta a graduados de Bioquímica, Farmacia, Biongeniería o carreras afines, con 3 años de experiencia en dispositivos médicos (pref. reactivos de diagnóstico) e inglés avanzado. 

Los interesados pueden enviar CV a selector@intersearch.com.ar con Asunto "Reg. 03"

-  Ingeniero de Servicio Técnico Jr. 

Liderará la instalación y puesta en funcionamiento de los equipos. El puesto incluye la capacitación y atención de los usuarios, por lo que se requieren excelentes habilidades de comunicación y orientación al detalle.
Asimismo será responsable de mantener un nivel adecuado de inventario de
repuestos.

Se requiere graduado de Ing. en Sistemas, Mecánica, Electrónica, Bioingeniería o afines, con 2-3 años de experiencia en la función, inglés intermedio y disponibilidad para viajes al Interior.

Los interesados pueden enviar CV a selector@intersearch.com.ar con
Asunto "Ing. 02"
"""
def limpiar_texto(texto):
    # Eliminar números
    texto = re.sub(r'\d+', '', texto)
    
    # Eliminar signos de puntuación y caracteres especiales
    texto = re.sub(r'[^\w\s]', '', texto)
    
    # Convertir texto a minúsculas
    texto = texto.lower()
    
    # Procesar el texto con spaCy
    doc = nlp(texto)
    
    # Eliminar palabras comunes y sin significado (stopwords) y lematizar
    palabras = [token.lemma_ for token in doc if not token.is_stop]
    
    # Unir las palabras resultantes en un string
    texto_limpiado = ' '.join(palabras)
    
    return texto_limpiado

# limpiar el texto
texto_limpiado = limpiar_texto(texto)
# imprimir el texto resultante
print(texto_limpiado)
doc = nlp(texto_limpiado)
print(doc)
entities = []
for ent in doc.ents:
    entities.append((ent.text, ent.label_))
df = pd.DataFrame(entities, columns=['Entidad', 'Tipo'])
df.to_csv('entidades_v1.0.csv', index=False)
