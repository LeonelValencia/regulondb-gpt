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
