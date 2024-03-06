import os
from phrase_validator import validar_formato_frase

class ErrorArchivo(Exception):
    def __init__(self, mensaje):
        super().__init__(mensaje)
        
def review_template_file(template_file_directory, error_skip=False):
    errores_totales = []
    frases_sin_errores_totales = []
    total_number_phrases_without_errors = 0
    total_number_errors = 0

    # Leer el archivo línea por línea
    with open(os.path.abspath(template_file_directory), 'r') as file:
        lineas = file.readlines()

        # Verificar cada línea del archivo
        for i, linea in enumerate(lineas, start=1):
            isRigth, errores = validar_formato_frase(linea, i)
            errores_totales.extend(errores)
            if isRigth:
                frases_sin_errores_totales.append(linea.strip())

    # Escribir los errores en un archivo de texto
    with open("error.txt", 'w') as errores_file:
        for error in errores_totales:
            errores_file.write(f"{error['ErrorType']} | {error['Location']} | {error['Description']}\n")
    
    total_number_phrases_without_errors = len(frases_sin_errores_totales)
    total_number_errors = len(errores_totales)
    
    if  total_number_phrases_without_errors == 0:
        raise ErrorArchivo("Todas las frases tienen errores. Verifique el archivo de error.txt")
    if error_skip:
        if total_number_phrases_without_errors > 0 and total_number_errors > 0:
            print("Se encontraron algunas frases con errores pero se ignorarán y se generará el archivo de frases.")
        elif len(frases_sin_errores) > 0 and total_number_errors == 0:
            print("No tuviste errores en el archivo de frases")
            print("Generando frases...")
    else:
        if total_number_errors > 0:
            raise ErrorArchivo("Se encontraron errores en el archivo de frases, verifique el archivo de error.txt y como no puso el argumento --error-skip, el programa se detendrá.")
        else:
            print("Generando frases...")
            
    return frases_sin_errores_totales

# Ejemplo de uso
frases_sin_errores = review_template_file("templates\promoter_phrases_template.txt")
print("Frases sin errores:", frases_sin_errores)