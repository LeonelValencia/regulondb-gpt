import re
from Bio.Seq import Seq
from Bio.SeqFeature import SeqFeature, FeatureLocation

def find_relative_position(main_sequence, sub_sequence, letter):
    sub_sequence = sub_sequence.lower()
    # Buscar la posición de la subsecuencia en la secuencia principal
    sub_position = main_sequence.find(sub_sequence)
    
    if sub_position == -1:
        print(f"La subsecuencia '{sub_sequence}' no se encuentra en la secuencia {main_sequence}.")
        return None
    
    # Encontrar la posición del nucleotido en relación con la subsecuencia
    g_position = main_sequence.find(letter, sub_position)
    
    if g_position == -1:
        print(f"No se encontró la letra {letter} después de la subsecuencia '{sub_sequence}' en la secuancia {main_sequence}.")
        return None
    
    # Calcular la posición relativa
    relative_position = g_position - (sub_position + len(sub_sequence) - 1)
    return relative_position

# Ejemplo de uso
main_sequence = "catatttatgctgtttccgacctgacacctgcgtgagttgttcacgtattttttcactatGtcttactctctgctggcagg"
sub_sequence = "TATTTT"
nucleotide = "G"

def find_relative_position2():

    # Supongamos que esta es tu secuencia principal
    main_sequence = Seq("AUGGCCAUUGUAAUGGGCCGCUGAAAGGGUGCCCGAUAG")

    # Define una ubicación de característica para la subsecuencia
    # sub_feature = SeqFeature(FeatureLocation(2, 5), type="subsecuencia")

    # Extrae la subsecuencia
    # sub_sequence = sub_feature.extract(main_sequence)
    # print(sub_sequence)
    
    # Traduce la secuencia de ARN a proteína
    protein_sequence = main_sequence.translate()
    print(protein_sequence)
    # Encuentra la posición del aminoácido "G" (correspondiente al nucleótido "G")
    g_position = protein_sequence.find("G")
    print(f"La posición relativa del aminoácido 'G' es: {g_position}")

# find_relative_position2()
    
# relative_position = find_relative_position(main_sequence, sub_sequence, nucleotide)
# if relative_position is not None:
#     print(f"La posición relativa de {nucleotide} con respecto a la subsecuencia '{sub_sequence}' es {relative_position}.")

def clean_text(texto):
    # Eliminar etiquetas HTML
    # texto_limpio = re.sub('<.*?>', '', texto)
    
    # Eliminar saltos de línea duplicados
    texto_limpio = re.sub('\n+', '\n', texto)
    texto_limpio = re.sub('\n', ' ', texto_limpio)
    
    return texto_limpio.strip()

texto_original = 'Keener J. and Nomura M. (1996). Regulation of Ribosome Synthesis, in: Neidhardt, F. (Editor in Chief) et al., <i>E. coli</i> and <i>Salmonella</i>. Cellular and Molecular Biology. ASM Press, Washington, D.C.,  p. 1417-31.\n\nAlthough the organization and sequence of the seven major ribosomal RNA (rRNA) P1 promoters are  highly conserved, the upstream region differs considerably in its regulation, with different transcription factor affinities for the individual upstream regions and strikingly different architectures of the resulting DNA-protein complexes that form with the individual rRNA operon upstream regions |CITS:[RDBECOLIPRC06983]|.'

# texto_limpio = clean_text(texto_original)
# print(texto_limpio)

# re.findall(r'[A|T|G|C]', sequence)
def find_nucleotide(secuence):
    # Supongamos que esta es tu secuencia con una letra mayúscula
    mi_secuencia = Seq(secuence)

    # Convertimos toda la secuencia en mayúsculas
    secuencia_mayusculas = mi_secuencia.upper()

    # Ahora puedes buscar la letra mayúscula original comparando las secuencias
    for (original, mayuscula) in zip(mi_secuencia, secuencia_mayusculas):
        if original == mayuscula:
            return original

secuencia = "catatttatgctgtttccgacctgacacctgcgtgagttgttcacgtattttttcactatGtcttactctctgctggcagg"
# nucleotide = find_nucleotide(secuencia)