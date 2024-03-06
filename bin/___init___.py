from dotenv import load_dotenv
import os
import argparse
from regulondb_webservices.build_query import main_build_query

def main():
    parser = argparse.ArgumentParser(description="Generador de frases relacionadas a promotores utilizando RegulonDB")
    parser.add_argument("frases", help="Archivo de frases tipo template")
    parser.add_argument("output", help="Archivo de salida para las frases generadas")
    parser.add_argument("--error-skip", help="Ignorar errores y continuar con el siguiente documento", action="store_true")
    args = parser.parse_args()
    
    # variables_encontradas, frases_sin_errores, n_errores = revisar_archivo_template(args.frases)
    
    load_dotenv()
    # Conectar a la base de datos RegulonDB
    url = os.environ["DB_CONNECTION_URL"]
    # query = main_build_query(list(variables_encontradas))
    # r = ejecutar_query(url, query)
    # Generar frases para cada documento resultante
    # phrases = generar_frases(r, list(frases_sin_errores))
    

if __name__ == "__main__":
    main()
