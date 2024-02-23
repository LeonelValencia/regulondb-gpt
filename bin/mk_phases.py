import argparse
import json
import requests

def cargar_configuracion(archivo_config):
    with open(archivo_config, 'r') as file:
        config_data = json.load(file)
    return config_data

def cargar_frases(archivo_frases):
    with open(archivo_frases, 'r') as file:
        frases = file.read().splitlines()
    return frases

def ejecutar_query(url, query):
    data = {'query': query}
    response = requests.post(url, json=data)
    return response.json()

def sustituir_variables(frase, variables):
    for key, value in variables.items():
        variable = "{" + key + "}"
        frase = frase.replace(variable, str(value))
    return frase

def main():
    parser = argparse.ArgumentParser(description="Generador de frases relacionadas a promotores utilizando RegulonDB")
    parser.add_argument("config", help="Archivo de configuración en formato JSON")
    parser.add_argument("frases", help="Archivo de frases tipo template")
    args = parser.parse_args()

    # Cargar configuración y frases
    config = cargar_configuracion(args.config)
    frases = cargar_frases(args.frases)

    # Conectar a la base de datos RegulonDB
    url = config['URL']
    queries = config['queries']

    for frase_template in frases:
        # Ejecutar queries y obtener variables
        variables = {}
        for query_name, query in queries.items():
            response_data = ejecutar_query(url, query)
            variables[query_name] = response_data.get('data', {})

        # Sustituir variables en la frase
        frase_generada = sustituir_variables(frase_template, variables)

        # Imprimir la frase generada
        print(frase_generada)

if __name__ == "__main__":
    main()
