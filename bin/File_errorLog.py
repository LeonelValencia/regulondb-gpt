import re
import os

def validar_formato_frase(frase, linea):
    # Patrón para encontrar variables en el formato {variable_name}
    patron_variables = re.compile(r'\{([^}]*)\}')

    errores = []

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

    return errores

def es_variable_valida(variable):
    # Lista de variables válidas
    variables_validas = ["getAllGUs", "getAllGenes", "getAllOperon", "getAllRegulon"]

    # Verificar si la variable está en la lista de variables válidas
    return variable in variables_validas

def revisar_archivo_template(archivo_template):
    errores_totales = []

    # Leer el archivo línea por línea
    with open(os.path.abspath(archivo_template), 'r') as file:
        lineas = file.readlines()

        # Verificar cada línea del archivo
        for i, linea in enumerate(lineas, start=1):
            errores = validar_formato_frase(linea, i)
            errores_totales.extend(errores)

    # Escribir los errores en un archivo de texto
    with open("errores_template.txt", 'w') as errores_file:
        for error in errores_totales:
            errores_file.write(f"{error['ErrorType']} | {error['Location']} | {error['Description']}\n")

# Ejemplo de uso
revisar_archivo_template("templates\promoter_phrases_template.txt")
