import requests
import json
import re
import pandas as pd

endpoint = "https://regulondb.ccg.unam.mx/graphql"

query = """
{
    getAllOperon(limit:5){
    data{
      operon{
        name
        strand
        regulationPositions{
          leftEndPosition
          rightEndPosition
        }
      }
      organism{
        _id
        name
      }
      transcriptionUnits{
        confidenceLevel
        firstGene{
          _id
          distanceToPromoter
          name
        }
        genes{
          _id
          name
          regulatorBindingSites{
            function
            mechanism
            regulator{
              name
            }
          }
        }
        name
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
        regulatorBindingSites{
          function
          mechanism
          regulator{
            name
          }
        }
        statistics{
          genes
          sites
          transcriptionFactors
        }
        synonyms
        terminators{
          _id
          class
          confidenceLevel
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
        for data in r.json()["data"]["getAllOperon"]["data"]:
            for tu in data["transcriptionUnits"]:
                if tu["promoter"]:
                    # 1. The name of the promoter with the identifier of RegulonBB database [PROMOTER_ID] is  [PROMOTER_NAME]
                    phrases.append(f"The name of the promoter with the identifier of RegulonBB database {tu['promoter']['_id']} is {tu['promoter']['name']}")
                    # 2. The promoter [PROMOTER_NAME] is located in the [reverse/forward] strand of the genome of Escherichia coli K-12
                    phrases.append(f"The promoter {tu['promoter']['name']} is located in the {data['operon']['strand']} strand of the genome of Escherichia coli K-12")
                    for citation in tu["promoter"]["citations"]:
                        if citation["evidence"]:
                            #3. The promoter  [PROMOTER_NAME] of  Escherichia coli K-12 has the evidence ["EVIDENCE"] linked to the reference [PMID:REFERENCE_ID]
                            phrases.append(f"The promoter {tu['promoter']['name']} of Escherichia coli K-12 has the evidence '{citation['evidence']['name']}' linked to the reference {citation['publication']['pmid']}")
                            # 14. The -10 and -35 boxes of the [PROMOTER_NAME] of  Escherichia coli K-12 has the evidence ["EVIDENCE"]
                            phrases.append(f"The -10 and -35 boxes of the {tu['promoter']['name']} of Escherichia coli K-12 has the evidence '{citation['evidence']['name']}'")
                            if tu["promoter"]["bindsSigmaFactor"]["name"]:
                                # 16. The [Sigma_factor] transcribing the [PROMOTER_NAME] of  Escherichia coli K-12 has the evidence related to the promoter ["EVIDENCE"]
                                phrases.append(f"The {tu['promoter']['bindsSigmaFactor']['name']} transcribing the {tu['promoter']['name']} of Escherichia coli K-12 has the evidence related to the promoter '{citation['evidence']['name']}'")
                        # 4. The promoter [PROMOTER_NAME] of  Escherichia coli K-12 has the reference [REFERENCE_ID]
                        phrases.append(f"The promoter {tu['promoter']['name']} of Escherichia coli K-12 has the reference {citation['publication']['pmid']}")
                        # 5. The Transcription Start Site (TSS) of the promoter [PROMOTER_NAME] of Escherichia coli K-12 is located at genome position [transcriptionStartSite]
                        phrases.append(f"The Transcription Start Site (TSS) of the promoter {tu['promoter']['name']} of Escherichia coli K-12 is located at genome position {tu['promoter']['transcriptionStartSite']['leftEndPosition']}")
                    # 6. The promoter [PROMOTER_NAME] of Escherichia coli K-12 has a TSS located at [Position relative to start of first gene] relative position from the gene [first gene of the TU linked to the promoter]
                    strand = '-' if {data['operon']['strand']} == "reverse" else ''
                    phrases.append(f"The promoter {tu['promoter']['name']} of Escherichia coli K-12 has a TSS located at {strand}{tu['firstGene']['distanceToPromoter']} relative position from the gene {tu['firstGene']['name']}")
                    # 7. The promoter [PROMOTER_NAME] of Escherichia coli K-12 has a TSS at a [A,T,G,C] nucleotide
                    sequence = tu['promoter']['sequence']
                    uppercase_letters = re.findall(r'[A|T|G|C]', sequence)
                    phrases.append(f"The promoter {tu['promoter']['name']} of Escherichia coli K-12 has a TSS at a {uppercase_letters[0]} nucleotide")
                    if tu["promoter"]["boxes"]:
                      # 8. The -10 box of the [PROMOTER_NAME] of  Escherichia coli K-12 is located at genome positions [1 star position in the genome of the -10 box] and [2 end position in the genome of the -10 box]
                      phrases.append(f"The -10 box of the {tu['promoter']['name']} of Escherichia coli K-12 is located at genome positions {tu['promoter']['boxes'][0]['rightEndPosition']} and {tu['promoter']['boxes'][0]['leftEndPosition']}")    
                      # 9. The -35 box of the [PROMOTER_NAME] promoter 
                      # of  Escherichia coli K-12 is located at genome
                      # positions [star position in the genome of the 
                      # -10 box] and [end position in the genome of the -35 box]
                      phrases.append(f"The -35 box of the {tu['promoter']['name']} \
                                    promoter of Escherichia coli K-12 is located at genome positions {tu['promoter']['boxes'][1]['rightEndPosition']} and {tu['promoter']['boxes'][1]['leftEndPosition']}")
                      # 10. The -10 box of the [PROMOTER_NAME] promoter of Escherichia coli K-12 is located at [relative position of the end of the -10 box regarding to the TSS] position relative to the TSS 
                      # 12. The sequence of the -10 box of the promoter [PROMOTER_NAME] of  Escherichia coli K-12 is [sequence of the -10 box of the [PROMOTER_NAME] ]
                      phrases.append(f"The sequence of the -10 box of the promoter {tu['promoter']['name']} of Escherichia coli K-12 is {tu['promoter']['boxes'][0]['sequence']}")
                      # 13. The sequence of the -35 box of the promoter [PROMOTER_NAME] of  Escherichia coli K-12 is [sequence of the -35 box of the [PROMOTER_NAME] ]
                      phrases.append(f"The sequence of the -35 box of the promoter {tu['promoter']['name']} of Escherichia coli K-12 is {tu['promoter']['boxes'][1]['sequence']}")
                    # 15. The promoter [PROMOTER_NAME] of  Escherichia coli K-12 is transcribed by the [Sigma_Factor_name]
                    if tu["promoter"]["bindsSigmaFactor"]["name"]:
                      phrases.append(f"The promoter {tu['promoter']['name']} of Escherichia coli K-12 is transcribed by the {tu['promoter']['bindsSigmaFactor']['name']}")
                    # 17. The sequence of the promoter [PROMOTER_NAME] of  Escherichia coli K-12  is [sequence of the promoter]
                    phrases.append(f"The sequence of the promoter {tu['promoter']['name']} of Escherichia coli K-12 is {tu['promoter']['sequence']}")
                    # 18. The transcription of the transcription unit (TU) [TU_name] is started at the promoter  [PROMOTER_NAME] of  Escherichia coli K-12
                    phrases.append(f"The transcription of the transcription unit (TU) {tu['name']} is started at the promoter {tu['promoter']['name']} of Escherichia coli K-12")
                    # 19. The transcription of the gene  [gene_name] is started at the promoter [PROMOTER_NAME] of Escherichia coli K-12
                    phrases.append(f"The transcription of the gene {tu['firstGene']['name']} is started at the promoter {tu['promoter']['name']} of Escherichia coli K-12")
                    if tu["promoter"]["regulatorBindingSites"]:
                      for regulatorBindingS in tu["promoter"]["regulatorBindingSites"]:
                        for regulatoryInteraction in regulatorBindingS["regulatoryInteractions"]:
                            if regulatoryInteraction["relativeCenterPosition"]:
                                # 23. The transcription factor  [TF_NAME] binds at positions  [CENTER_POSITION] relative to the transcriptional start site of the  promoter [PROMOTER_NAME] of  Escherichia coli K-12  to [activate/repress] it
                                phrases.append(f"The transcription factor {regulatorBindingS['regulator']['name']} binds at positions {regulatoryInteraction['relativeCenterPosition']} relative to the transcriptional start site of the promoter {tu['promoter']['name']} of Escherichia coli K-12 to {regulatorBindingS['function']} it")
                        if regulatorBindingS["function"] == "activator":
                          # 20. The transcription factor  [TF_NAME] activates the transcription of the  promoter [PROMOTER_NAME] of  Escherichia coli K-12
                          phrases.append(f"The transcription factor {regulatorBindingS['regulator']['name']} activates the transcription of the promoter {tu['promoter']['name']} of Escherichia coli K-12")
                        elif regulatorBindingS["function"] == "repressor":
                          # 21. The transcription factor  [TF_NAME] represses the transcription of the  promoter [PROMOTER_NAME] of  Escherichia coli K-12
                          phrases.append(f"The transcription factor {regulatorBindingS['regulator']['name']} represses the transcription of the promoter {tu['promoter']['name']} of Escherichia coli K-12")
                    if tu["promoter"]["note"]:
                      # 22. "The comment related to the [PROMOTER_NAME] promoter of  Escherichia coli K-12 is "[NOTE] "
                      phrases.append(f"The comment related to the {tu['promoter']['name']} promoter of Escherichia coli K-12 is '{tu['promoter']['note']}'")
              
    df = pd.DataFrame(phrases, columns=["Phrases"])
    df.to_csv("phrases.csv", index=False)
    print(df)
else:
    raise Exception(f"Query failed to run with a {r.status_code}.")
    