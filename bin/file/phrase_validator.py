import re
import os
import sys
from dotenv import load_dotenv
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from regulondb_webservices import connection

def validar_formato_frase(frase, linea):
    frase = frase.strip()
    # Patrón para encontrar variables en el formato {variable_name}
    patron_variables = re.compile(r'\{([a-zA-Z0-9_\.]+)\}')

    errores = []
    isRigth = False

    # Buscar todas las variables en la frase
    variables_encontradas = patron_variables.findall(frase)
    if len(variables_encontradas) == 0:
        errores.append({"ErrorType": "missing_variable", "Location": linea,
                        "Description": f"Invalid variable format in the template: {frase}. Check for missing or unclosed curly brackets."})
        return isRigth, errores
    else:

        # Verificar si hay llaves no cerradas o variables faltantes
        if '{' not in frase or '}' not in frase:
            errores.append({"ErrorType": "missing_variable", "Location": linea,
                            "Description": f"Invalid variable format in the template: {frase}. Check for missing or unclosed curly brackets."})

        # Verificar el orden de las llaves
        pila_llaves = []
        for caracter in frase:
            if caracter == '{':
                pila_llaves.append('{')
            elif caracter == '}':
                if len(pila_llaves) == 0:
                    errores.append({"ErrorType": "unmatched_bracket", "Location": linea,
                                    "Description": f"Unmatched closing bracket '}}' in the template: {frase}. Check for missing opening brackets '{{'."})
                else:
                    elemento_superior = pila_llaves.pop()
                    if elemento_superior != '{':
                        errores.append({"ErrorType": "unmatched_bracket", "Location": linea,
                                        "Description": f"Unmatched closing bracket '}}' in the template: {frase}. Check for missing opening brackets '{{'."})

        if len(pila_llaves) > 0:
            errores.append({"ErrorType": "unmatched_bracket", "Location": linea,
                            "Description": f"Unmatched opening bracket '{{' in the template: {frase}. Check for missing closing brackets '}}'."})
        
        if len(errores) > 0:
            return isRigth, errores
        else:
            valid_queries, valid_variables = get_valid_variables()
            # Verificar cada variable encontrada
            for variable in variables_encontradas:
                queries = variable.split('.')
                main_query = queries[0]
                remaining_query = queries[1:]
                if not main_query in valid_queries:
                    errores.append({"ErrorType": "Invalid variable name", "Location": linea,
                                    "Description": f"Invalid variable name: {{{variable}}}. Valid query names: {valid_queries}"})
                for variable in remaining_query:
                    if not variable in valid_variables:
                        errores.append({"ErrorType": "Invalid variable name", "Location": linea,
                                        "Description": f"Invalid variable name: {{{variable}}}. Valid variable names: {set(valid_variables)}"})
            if len(errores) > 0:
                return isRigth, errores
            else:
                isRigth = True
                return isRigth, errores

def get_valid_variables():
    valid_queries = []
    valid_variables = []
    load_dotenv()
    # Conectar a la base de datos RegulonDB
    url = os.environ["DB_CONNECTION_URL"]
    query = "{ __schema { types { name fields { name } } } }"
    data = connection.ejecutar_query(url, query)
    for tipo in data["__schema"]["types"]:
        if tipo["name"] in ["Query"]:
            for campo in tipo["fields"]:
                valid_queries.append(campo["name"])
        else:
            valid_variables.append(tipo["name"])
            if tipo["fields"]:
                for campo in tipo["fields"]:
                    valid_variables.append(campo['name'])
    return valid_queries, valid_variables