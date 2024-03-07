import os
from phrase_validator import validar_formato_frase

class ErrorArchivo(Exception):
    def __init__(self, mensaje):
        super().__init__(mensaje)
        
def review_template_file(template_file_directory, error_skip=False):
    total_errors = []
    total_number_phrases_without_errors = 0
    total_number_errors = 0
    template_phrases = []

    # Leer el archivo línea por línea
    with open(os.path.abspath(template_file_directory), 'r') as file:
        lines = file.readlines()

        # Verificar cada línea del archivo
        for i, linea in enumerate(lines, start=1):
            isRigth, errors, paths = validar_formato_frase(linea, i)
            total_errors.extend(errors)
            if isRigth:
                template_phrase = {"id": i,"phrase": linea.strip(), "queries": paths}
                template_phrases.append(template_phrase)

    # Escribir los errores en un archivo de texto
    with open("error.txt", 'w') as errors_file:
        for error in total_errors:
            errors_file.write(f"{error['ErrorType']} | {error['Location']} | {error['Description']}\n")
    
    total_number_phrases_without_errors = len(template_phrases)
    total_number_errors = len(total_errors)
    
    if  total_number_phrases_without_errors == 0:
        raise ErrorArchivo("Todas las frases tienen errores. Verifique el archivo de error.txt")
    if error_skip:
        if total_number_phrases_without_errors > 0 and total_number_errors > 0:
            print("Se encontraron algunas frases con errores pero se ignorarán y se generará el archivo de frases.")
        elif len(total_number_phrases_without_errors) > 0 and total_number_errors == 0:
            print("No tuviste errores en el archivo de frases")
            print("Generando frases...")
    else:
        if total_number_errors > 0:
            raise ErrorArchivo("Se encontraron errores en el archivo de frases, verifique el archivo de error.txt y como no puso el argumento --error-skip, el programa se detendrá.")
        else:
            print("Generando frases...")
            
    return template_phrases

# Ejemplo de uso
frases_sin_errores = review_template_file("templates/promoter_phrases_template.txt")
print("Frases sin errores:", frases_sin_errores)