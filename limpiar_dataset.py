from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')
import pandas as pd
# Obtener la lista de stopwords en inglés
stop_words = set(stopwords.words('english'))

df = pd.read_csv('phrases.tsv', sep='\t',engine='python')

print(df.head())

# Create a new column to store the filtered phrases
df['filtered_phrase'] = ''

# Iterate over each phrase in the 'phrase' column
for index, row in df.iterrows():
    # Get the original phrase
    query_original = row['phrase']
    
    # Dividir el query en palabras
    palabras = query_original.split()

    # Filtrar las palabras que no están en la lista de stopwords
    palabras_filtradas = [palabra for palabra in palabras if palabra.lower() not in stop_words]

    # Unir las palabras filtradas en una cadena nuevamente
    query = ' '.join(palabras_filtradas)
    
    # Store the filtered phrase in the 'filtered_phrase' column
    df.at[index, 'filtered_phrase'] = query
    
df.drop(columns=['phrase'], inplace=True)    
df.to_csv("clean_phrases.tsv", index=False, sep="\t")