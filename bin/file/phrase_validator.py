import re
import os
import sys
from dotenv import load_dotenv
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from regulondb_webservices import connection

def validar_formato_frase(phrase, linea):
    phrase = phrase.strip()
    # Patrón para encontrar variables en el formato {variable_name}
    variable_pattern = re.compile(r'\{([a-zA-Z0-9_\.]+)\}')

    errors = []
    isRigth = False
    paths = []

    # Buscar todas las variables en la frase
    variables_found = variable_pattern.findall(phrase)
    if len(variables_found) == 0:
        errors.append({"ErrorType": "missing_variable", "Location": linea,
                        "Description": f"Invalid variable format in the template: {phrase}. Check for missing or unclosed curly brackets."})
        return isRigth, errors, paths
    else:

        # Verificar si hay llaves no cerradas o variables faltantes
        if '{' not in phrase or '}' not in phrase:
            errors.append({"ErrorType": "missing_variable", "Location": linea,
                            "Description": f"Invalid variable format in the template: {phrase}. Check for missing or unclosed curly brackets."})

        # Verificar el orden de las llaves
        key_stack = []
        for character in phrase:
            if character == '{':
                key_stack.append('{')
            elif character == '}':
                if len(key_stack) == 0:
                    errors.append({"ErrorType": "unmatched_bracket", "Location": linea,
                                    "Description": f"Unmatched closing bracket '}}' in the template: {phrase}. Check for missing opening brackets '{{'."})
                else:
                    upper_element = key_stack.pop()
                    if upper_element != '{':
                        errors.append({"ErrorType": "unmatched_bracket", "Location": linea,
                                        "Description": f"Unmatched closing bracket '}}' in the template: {phrase}. Check for missing opening brackets '{{'."})

        if len(key_stack) > 0:
            errors.append({"ErrorType": "unmatched_bracket", "Location": linea,
                            "Description": f"Unmatched opening bracket '{{' in the template: {phrase}. Check for missing closing brackets '}}'."})
        
        if len(errors) > 0:
            return isRigth, errors, paths
        else:
            valid_queries, valid_variables = get_valid_variables()
            # Verificar cada variable encontrada
            for variable in variables_found:
                queries = variable.split('.')
                main_query = queries[0]
                remaining_query = queries[1:]
                if not main_query in valid_queries:
                    errors.append({"ErrorType": "Invalid variable name", "Location": linea,
                                    "Description": f"Invalid variable name: {{{variable}}}. Valid query names: {valid_queries}"})
                for variable in remaining_query:
                    if not variable in valid_variables:
                        errors.append({"ErrorType": "Invalid variable name", "Location": linea,
                                        "Description": f"Invalid variable name: {{{variable}}}. Valid variable names: {set(valid_variables)}"})
            if len(errors) > 0:
                return isRigth, errors, paths
            else:
                isRigth = True
                paths = variables_found
                return isRigth, errors, paths

def get_valid_variables():
    valid_queries = []
    valid_variables = []
    load_dotenv()
    # Conectar a la base de datos RegulonDB
    url = os.environ["DB_CONNECTION_URL"]
    query = "{ __schema { types { name fields { name } } } }"
    data = connection.ejecutar_query(url, query)
    for type in data["__schema"]["types"]:
        if type["name"] in ["Query"]:
            for field in type["fields"]:
                valid_queries.append(field["name"])
        else:
            valid_variables.append(type["name"])
            if type["fields"]:
                for field in type["fields"]:
                    valid_variables.append(field['name'])
    return valid_queries, valid_variables