import os
import argparse
import json
import requests
import pandas as pd

def cargar_configuracion(archivo_config):
    with open(os.path.abspath(archivo_config), 'r') as file:
        config_data = json.load(file)
    return config_data

def cargar_frases(archivo_frases):
    with open(os.path.abspath(archivo_frases), 'r') as file:
        frases = file.read().splitlines()
    return frases

def ejecutar_query(endpoint, query):
    r = requests.post(endpoint, json={"query": query}, verify=False)
    return r

def generar_frases(data, phrases_template):
    phrases = []

    # Iterar sobre los resultados del query principal
    for result in data["data"]["getAllOperon"]["data"]:
        # Iterar sobre las plantillas de frases definidas
        for phrase_template in phrases_template:
            # Generar frases para cada documento resultante del query principal
            generated_phrases = generar_frases_para_plantilla(result, phrase_template)
            phrases.extend(generated_phrases)
    print(phrases)
    return phrases

def generar_frases_para_plantilla(data, phrase_template):
    generated_phrases = []

    # Ejemplo de adaptación para una plantilla específica
    id_placeholder = "{getAllOperon.data.transcriptionUnits.promoter._id}"
    name_placeholder = "{getAllOperon.data.transcriptionUnits.promoter.name}"

    for tu in data["transcriptionUnits"]:
        if tu["promoter"]:
            # Obtener valores específicos del resultado del query
            promoter_id = tu["promoter"]["_id"]
            promoter_name = tu["promoter"]["name"]

            # Reemplazar placeholders en la plantilla
            current_phrase = phrase_template.replace(id_placeholder, promoter_id)
            current_phrase = current_phrase.replace(name_placeholder, promoter_name)

            # Agregar la frase generada a la lista
            generated_phrases.append(current_phrase)
    return generated_phrases

def main():
    parser = argparse.ArgumentParser(description="Generador de frases relacionadas a promotores utilizando RegulonDB")
    parser.add_argument("config", help="Archivo de configuración en formato JSON")
    parser.add_argument("frases", help="Archivo de frases tipo template")
    # parser.add_argument("output", help="Archivo de salida para las frases generadas")
    args = parser.parse_args()

    # Cargar configuración y frases
    config = cargar_configuracion(args.config)
    frases = cargar_frases(args.frases)

    # Conectar a la base de datos RegulonDB
    url = config['db_connection']['URL']
    query_principal  = config['queries']['main']['query']
    r = ejecutar_query(url, query_principal)

    if r.status_code == 200:
        # Generar frases para cada documento resultante
        phrases = generar_frases(r.json(), frases)
        # Guardar frases en un archivo CSV
        # df = pd.DataFrame(phrases, columns=["Phrases"])
        # df.to_csv(args.output, index=False)
    else:
        print(f"Error en la ejecución del query principal. Código de estado: {r.status_code}")

if __name__ == "__main__":
    main()
