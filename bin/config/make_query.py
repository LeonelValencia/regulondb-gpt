import json

# Tu consulta GraphQL
query = """
{
    getAllOperon{
    data{
      operon{
        name 
        strand
      }
      transcriptionUnits{
        firstGene{
          distanceToPromoter
          name
        }
        name
        promoter{      
          _id
          name
          bindsSigmaFactor{ 
            name 
          }
          boxes{    
            leftEndPosition
            rightEndPosition
            sequence
          }
          citations{
            evidence{
              name
            }
            publication{
              title 
              pmid
            }
          }
          note
          regulatorBindingSites{
            function 
            regulator{
              name
            }
            regulatoryInteractions{
              relativeCenterPosition  
            }
          }
          sequence
          transcriptionStartSite{ 
            leftEndPosition
          }
        }
      }
    }
  }
}
"""

# Estructura del JSON con la URL y la consulta
json_data = {
    "db_connection": {
        "URL": "https://regulondb.ccg.unam.mx/graphql"
    },
    "queries": {
        "main": {
            "query": query
        }
    }
}

# Convertir el diccionario en JSON y guardarlo en un archivo
with open('config2.json', 'w') as json_file:
    json.dump(json_data, json_file, indent=4)
