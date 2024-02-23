import re

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

# relative_position = find_relative_position(main_sequence, sub_sequence, nucleotide)
# if relative_position is not None:
#     print(f"La posición relativa de {nucleotide} con respecto a la subsecuencia '{sub_sequence}' es {relative_position}.")

def clean_text(texto):
    # Eliminar etiquetas HTML
    texto_limpio = re.sub('<.*?>', '', texto)
    
    # Eliminar saltos de línea duplicados
    texto_limpio = re.sub('\n+', '\n', texto_limpio)
    
    return texto_limpio

texto_original = 'Keener J. and Nomura M. (1996). Regulation of Ribosome Synthesis, in: Neidhardt, F. (Editor in Chief) et al., <i>E. coli</i> and <i>Salmonella</i>. Cellular and Molecular Biology. ASM Press, Washington, D.C.,  p. 1417-31.\n\nAlthough the organization and sequence of the seven major ribosomal RNA (rRNA) P1 promoters are  highly conserved, the upstream region differs considerably in its regulation, with different transcription factor affinities for the individual upstream regions and strikingly different architectures of the resulting DNA-protein complexes that form with the individual rRNA operon upstream regions |CITS:[RDBECOLIPRC06983]|.'

# texto_limpio = clean_text(texto_original)
# print(texto_limpio)
