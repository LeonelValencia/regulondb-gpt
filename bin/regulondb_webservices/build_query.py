def construir_query(rutas_variables, indentacion=2):

    # Diccionario para agrupar las variables por su raíz y subgrupo
    resultado = {}

    for ruta in rutas_variables:
        segmentos = ruta.split('.')
        actual = resultado

        for segmento in segmentos:
            if segmento not in actual:
                actual[segmento] = {}
            actual = actual[segmento]

    return resultado
   
def build_query_string(data, indent=2):
    query_string = ''
    for key, value in data.items():
        if value == {}:
            query_string += ' ' * indent + f"{key}\n"
            continue
        else:
            query_string += ' ' * indent + f"{key}{{\n"
        if isinstance(value, dict):
            query_string += build_query_string(value, indent + 2)
        query_string += ' ' * indent + '}\n'
    return query_string
 
# Ejemplo de uso
# rutas_variables = [
#     "getAllOperon.data.transcriptionUnits.promoter._id",
#     "getAllOperon.data.transcriptionUnits.promoter.name",
#     "getAllOperon.data.operon.strand",
#     "getAllOperon.data.transcriptionUnits.promoter.citations.evidence.name",
#     "getAllOperon.data.transcriptionUnits.promoter.citations.publication.pmid",
#     "getAllOperon.data.transcriptionUnits.promoter.transcriptionStartSite.leftEndPosition",
# ]

# Inicializar la query con el nombre del tipo actual
def main_build_query(rutas_variables):
    query = f"{{\n"
    resultado = construir_query(rutas_variables)
    query += build_query_string(resultado)
    query += '}'
    return query

# query = main_build_query(rutas_variables)
# print(query)