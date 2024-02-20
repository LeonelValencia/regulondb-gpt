
import requests
import json

endpoint = "https://regulondb.ccg.unam.mx/graphql"

query = """
{
    getAllOperon(limit:5){
    data{
      transcriptionUnits{
        promoter{
          _id
          name
          additiveEvidences{
            category
            code
            type
          }
          bindsSigmaFactor{
            _id
            abbreviatedName
            citations{
              evidence{
                name
              }
              publication{
                title
              }
            }
            name
          }
          boxes{
            leftEndPosition
            rightEndPosition
            sequence
            type
          }
          citations{
            evidence{
              _id
              additiveEvidenceCodeRule
              code
              name
              type
            }
            publication{
              _id
              title
              pmid
            }
          }
          confidenceLevel
          note
          regulatorBindingSites{
            function
            mechanism
            regulator{
              name
            }
            regulatoryInteractions{
              _id
              function
              note
              relativeCenterPosition
            }
          }
          score
          sequence
          synonyms
          transcriptionStartSite{
            leftEndPosition
            range
            rightEndPosition
            type
          }
        }
      }
    }
  }
}
"""

phrases = []
r = requests.post(endpoint, json={"query": query}, verify=False)
if r.status_code == 200:
    # print(json.dumps(r.json(), indent=2))
    if r.json().get("data"):
        for operon in r.json()["data"]["getAllOperon"]["data"]:
            for tu in operon["transcriptionUnits"]:
                if tu["promoter"]:
                  # 1. The name of the promoter with the identifier of RegulonBB database [PROMOTER_ID] is  [PROMOTER_NAME]
                    phrases.append(f"The name of the promoter with the identifier of RegulonBB database {tu['promoter']['_id']} is {tu['promoter']['name']}")
                    for citation in tu["promoter"]["citations"]:
                        if citation["evidence"]:
                            #3. The promoter  [PROMOTER_NAME] of  Escherichia coli K-12 has the evidence ["EVIDENCE"] linked to the reference [PMID:REFERENCE_ID]
                            phrases.append(f"The promoter {tu['promoter']['name']} of  Escherichia coli K-12 has the evidence '{citation['evidence']['name']}' linked to the reference {citation['publication']['pmid']}")
                        # 4. The promoter [PROMOTER_NAME] of  Escherichia coli K-12 has the reference [REFERENCE_ID]
                        phrases.append(f"The promoter {tu['promoter']['name']} of  Escherichia coli K-12 has the reference {citation['publication']['pmid']}")
                    # 5. The Transcription Start Site (TSS) of the promoter [PROMOTER_NAME] of  Escherichia coli K-12 is located at genome position [POS_1]
                    phrases.append(f"The Transcription Start Site (TSS) of the promoter {tu['promoter']['name']} of  Escherichia coli K-12 is located at genome position {tu['promoter']['transcriptionStartSite']['leftEndPosition']}")    
    print(phrases)
else:
    raise Exception(f"Query failed to run with a {r.status_code}.")
    