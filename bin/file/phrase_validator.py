import re

def validar_formato_frase(frase, linea):
    # Patrón para encontrar variables en el formato {variable_name}
    patron_variables = re.compile(r'\{([^}]*)\}')

    errores = []
    frases_sin_errores = []
    variables = []

    # Buscar todas las variables en la frase
    variables_encontradas = patron_variables.findall(frase)
    
    # Verificar cada variable encontrada
    for variable in variables_encontradas:
        main_query = variable.split('.')[0]
        if not es_variable_valida(main_query):
            errores.append({"ErrorType": "Invalid variable name", "Location": linea,
                            "Description": f"Invalid variable name: {{{variable}}}. Valid variable names: {{getAllGUs}}, {{getAllGenes}}, {{getAllOperon}}, {{getAllRegulon}}"})

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
    if errores == []:
        frases_sin_errores.append(frase)
        variables.extend(variables_encontradas)
        
    return errores, variables, frases_sin_errores

def es_variable_valida(variable):
    # Lista de variables válidas
    variables_validas = ["getAllGUs", "getAllGenes", "getAllOperon", "getAllRegulon"]

    # Verificar si la variable está en la lista de variables válidas
    return variable in variables_validas