from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from dotenv import load_dotenv
import os
import argparse
import json
import pandas as pd
from File_errorLog import revisar_archivo_template
from regulondb_webservices.build_query import main_build_query

def ejecutar_query(endpoint, query):
    # Deshabilitar la verificación del certificado SSL
    transport = RequestsHTTPTransport(
        url=endpoint,
        use_json=True,
        verify=False,  # Agregar esta línea para deshabilitar la verificación del certificado SSL
    )
    
    # Crear un cliente GraphQL con el transporte configurado
    cliente = Client(transport=transport, fetch_schema_from_transport=True)
    consulta_ejemplo = gql(query)
    
    # Ejecutar la consulta y mostrar la respuesta
    try:
        respuesta_graphql = cliente.execute(consulta_ejemplo)
        return respuesta_graphql
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")

def generar_frases(data, phrases_template):
    phrases = []

    # Iterar sobre los resultados del query principal
    for result in data["getAllOperon"]["data"]:
        # Iterar sobre las plantillas de frases definidas
        for phrase_template in phrases_template:
            # Generar frases para cada documento resultante del query principal
            generated_phrases = generar_frases_para_plantilla(result, phrase_template)
            phrases.extend(generated_phrases)
    return phrases

def generar_frases_para_plantilla(data, phrase_template):
    generated_phrases = []

    # Ejemplo de adaptación para una plantilla específica
    id_placeholder = "{getAllOperon.data.transcriptionUnits.promoter._id}"
    name_placeholder = "{getAllOperon.data.transcriptionUnits.promoter.name}"
    sinonimos_placeholder = "{getAllOperon.data.transcriptionUnits.promoter.synonyms}"
    strand_placeholder = "{getAllOperon.data.operon.strand}"
    evidence_placeholder = "{getAllOperon.data.transcriptionUnits.promoter.citations.evidence.name}"
    pmid_placeholder = "{getAllOperon.data.transcriptionUnits.promoter.citations.publication.pmid}"
    leftEndPosition_placeholder = "{getAllOperon.data.transcriptionUnits.promoter.transcriptionStartSite.leftEndPosition}"
    distanceToPromoter_placeholder = "{getAllOperon.data.transcriptionUnits.firstGene.distanceToPromoter}"
    firstGeneName_placeholder = "{getAllOperon.data.transcriptionUnits.firstGene.distanceToPromoter}"
    leftEndPosition0_placeholder = "{getAllOperon.data.transcriptionUnits.promoter.boxes[0].leftEndPosition}"
    rightEndPosition0_placeholder = "{getAllOperon.data.transcriptionUnits.promoter.boxes[0].rightEndPosition}"
    leftEndPosition1_placeholder = "{getAllOperon.data.transcriptionUnits.promoter.boxes[1].leftEndPosition}"
    rightEndPosition1_placeholder = "{getAllOperon.data.transcriptionUnits.promoter.boxes[1].rightEndPosition}"
    sequence10Box_placeholder = "{getAllOperon.data.transcriptionUnits.promoter.boxes[0].sequence}"
    sequence35Box_placeholder = "{getAllOperon.data.transcriptionUnits.promoter.boxes[1].sequence}"
    sigmFactorName_placeholder = "{getAllOperon.data.transcriptionUnits.promoter.bindsSigmaFactor.name}"
    sigmaFactorEvidence_placeholder = "{getAllOperon.data.transcriptionUnits.promoter.bindsSigmaFactor.citations.evidence.name}"
    sequence_placeholder = "{getAllOperon.data.transcriptionUnits.promoter.sequence}"
    TUName_placeholder = "{getAllOperon.data.transcriptionUnits.name}"
    genesName_placeholder = "{getAllOperon.data.transcriptionUnits.genes.name}"
    transcriptionFactorName_placeholder = "{getAllOperon.data.transcriptionUnits.promoter.regulatorBindingSites.regulator.name}"
    comment_placeholder = "{getAllOperon.data.transcriptionUnits.promoter.note}"
    transcriptionFactorCenterPosition_placeholder = "{getAllOperon.data.transcriptionUnits.promoter.regulatorBindingSites.regulatoryInteractions.relativeCenterPosition}"
    transcriptionFactorFunction_placeholder = "{getAllOperon.data.transcriptionUnits.promoter.regulatorBindingSites.function}"
    evidenceOfBinding_placeholder = "{getAllOperon.data.transcriptionUnits.promoter.regulatorBindingSites.regulatoryInteractions.regulatorySite.citations.evidence.name}"
    evidenceOfFunction_placeholder = "{getAllOperon.data.transcriptionUnits.promoter.regulatorBindingSites.regulatoryInteractions.citations.evidence.name}"
    RIId_placeholder = "{getAllOperon.data.transcriptionUnits.promoter.regulatorBindingSites.regulatoryInteractions._id}"

    for tu in data["transcriptionUnits"]:
        if tu["promoter"]:
            # Obtener valores específicos del resultado del query
            promoter_id = tu["promoter"]["_id"]
            promoter_name = tu["promoter"]["name"]
            promoter_synonym = tu["promoter"].get("synonyms", [])

            # Reemplazar placeholders en la plantilla
            if id_placeholder in phrase_template and promoter_id:
                phrase_template = phrase_template.replace(name_placeholder, promoter_name)
                phrase_template = phrase_template.replace(id_placeholder, promoter_id)
            elif sinonimos_placeholder in phrase_template and promoter_synonym:
                phrase_template = phrase_template.replace(name_placeholder, promoter_name)
                phrase_template = phrase_template.replace(sinonimos_placeholder, ", ".join(promoter_synonym))
            else:
                continue  # Skip adding the phrase if it doesn't have synonyms and promoter_synonym is empty
        
            # Agregar la frase generada a la lista
            generated_phrases.append(phrase_template)
    print(generated_phrases)
    return generated_phrases

def main():
    parser = argparse.ArgumentParser(description="Generador de frases relacionadas a promotores utilizando RegulonDB")
    parser.add_argument("frases", help="Archivo de frases tipo template")
    parser.add_argument("output", help="Archivo de salida para las frases generadas")
    parser.add_argument("--error-skip", help="Ignorar errores y continuar con el siguiente documento", action="store_true")
    args = parser.parse_args()
    
    variables_encontradas, frases_sin_errores, n_errores = revisar_archivo_template(args.frases)

    if len(variables_encontradas) == 0 or len(frases_sin_errores) == 0:
        print("Todas las frases tienen errores. Verifique el archivo de error.txt")
        return
    if args.error_skip:
        if len(frases_sin_errores) > 0 and n_errores > 0:
            print("Se encontraron algunas frases con errores pero se ignorarán y se generará el archivo de frases.")
        elif len(frases_sin_errores) > 0 and n_errores == 0:
            print("No tuviste errores en el archivo de frases")
            print("Generando frases...")
    else:
        if n_errores > 0:
            print("Se encontraron errores en el archivo de frases, verifique el archivo de error.txt y como no puso el argumento --error-skip, el programa se detendrá.")
            return
        else:
            print("Generando frases...")
    
    load_dotenv()
    # Conectar a la base de datos RegulonDB
    url = os.environ["DB_CONNECTION_URL"]
    query = main_build_query(list(variables_encontradas))
    r = ejecutar_query(url, query)
    # Generar frases para cada documento resultante
    phrases = generar_frases(r, list(frases_sin_errores))
    # Guardar frases en un archivo CSV
    df = pd.DataFrame(phrases, columns=["Phrases"])
    df.to_csv(args.output, index=False)

if __name__ == "__main__":
    main()
