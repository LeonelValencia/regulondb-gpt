import requests
import re
import pandas as pd
from utils import find_relative_position, clean_text

endpoint = "https://regulondb.ccg.unam.mx/graphql"

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
        genes{
          name
        }
        name
        promoter{      
          _id
          name
          bindsSigmaFactor{ 
            name 
            citations{
              evidence{
                name
              }
            }
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

phrases = []
r = requests.post(endpoint, json={"query": query}, verify=False)
if r.status_code == 200:
    if r.json().get("data"):
        for data in r.json()["data"]["getAllOperon"]["data"]:
            for tu in data["transcriptionUnits"]:
                if tu["promoter"]:
                    # 1. The name of the promoter with the identifier of 
                    # RegulonBB database [PROMOTER_ID] is  [PROMOTER_NAME]
                    phrases.append(f"The name of the promoter with the "
                        f"identifier of RegulonBB database {tu['promoter']['_id']} "
                        f"is {tu['promoter']['name']}")
                    # 2. The promoter [PROMOTER_NAME] is located in the 
                    # [reverse/forward] strand of the genome of Escherichia 
                    # coli K-12
                    phrases.append(f"The promoter {tu['promoter']['name']} is "
                        f"located in the {data['operon']['strand']} strand of the "
                        f"genome of Escherichia coli K-12")
                    for citation in tu["promoter"]["citations"]:
                        if citation["evidence"]:
                            if citation["publication"] and citation["publication"]["pmid"]:
                                #3. The promoter [PROMOTER_NAME] of Escherichia 
                                # coli K-12 has the evidence ["EVIDENCE"] 
                                # linked to the reference [PMID:REFERENCE_ID]
                                phrases.append(f"The promoter {tu['promoter']['name']} "
                                    f"of Escherichia coli K-12 has the evidence "
                                    f"'{citation['evidence']['name']}' linked to "
                                    f"the reference {citation['publication']['pmid']}")
                            
                        if citation["publication"] and citation["publication"]["pmid"]:
                            # 4. The promoter [PROMOTER_NAME] of  Escherichia 
                            # coli K-12 has the reference [citations]
                            phrases.append(f"The promoter {tu['promoter']['name']} "
                                f"of Escherichia coli K-12 has the reference " 
                                f"PMID:{citation['publication']['pmid']}")
                    # 5. The Transcription Start Site (TSS) of the 
                    # promoter [PROMOTER_NAME] of Escherichia coli 
                    # K-12 is located at genome position [transcriptionStartSite]
                    if tu["promoter"]["transcriptionStartSite"]:
                        phrases.append(f"The Transcription Start Site (TSS) of "
                            f"the promoter {tu['promoter']['name']} of Escherichia "
                            f"coli K-12 is located at genome position "
                            f"{tu['promoter']['transcriptionStartSite']['leftEndPosition']}")
                        # 6. The promoter [PROMOTER_NAME] of Escherichia coli 
                        # K-12 has a TSS located at [Position relative to 
                        # start of first gene] relative position from the 
                        # gene [first gene of the TU linked to the promoter]
                    # strand = '-' if data['operon']['strand'] == "reverse" else ''
                    if tu["firstGene"] and tu["firstGene"]["distanceToPromoter"]:
                        if tu["firstGene"]["distanceToPromoter"] and tu["firstGene"]["name"]:
                            phrases.append(f"The promoter {tu['promoter']['name']} of "
                                f"Escherichia coli K-12 has a TSS located at "
                                f"-{tu['firstGene']['distanceToPromoter']} "
                                f"relative position from the gene {tu['firstGene']['name']}")
                    # 7. The promoter [PROMOTER_NAME] of Escherichia 
                    # coli K-12 has a TSS at a [A,T,G,C] nucleotide
                    if tu["promoter"]["sequence"]:
                        sequence = tu['promoter']['sequence']
                        nucleotide = re.findall(r'[A|T|G|C]', sequence)
                        phrases.append(f"The promoter {tu['promoter']['name']} of "
                            f"Escherichia coli K-12 has a TSS at a {nucleotide[0]} "
                            f"nucleotide")
                        if tu["promoter"]["boxes"]:
                            # 10. The -10 box of the [PROMOTER_NAME] promoter 
                            # of Escherichia coli K-12 is located at [relative 
                            # position of the end of the -10 box regarding to 
                            # the TSS] position relative to the TSS 
                            relative_position = find_relative_position(sequence, 
                                tu["promoter"]["boxes"][0]["sequence"], nucleotide[0])
                            if relative_position is not None:
                                phrases.append(f"The -10 box of the {tu['promoter']['name']} "
                                    f"promoter of Escherichia coli K-12 is located at -"
                                    f"{relative_position} position relative to the TSS")
                            
                            if len(tu["promoter"]["boxes"]) == 2:
                                # 11. The -35 box of the [PROMOTER_NAME] promoter 
                                # of Escherichia coli K-12 is located at [relative 
                                # position of the end of the -35 box regarding to 
                                # the TSS] position relative to the TSS 
                                relative_position = find_relative_position(sequence, 
                                    tu["promoter"]["boxes"][1]["sequence"], nucleotide[0])
                                if relative_position is not None:
                                    phrases.append(f"The -35 box of the {tu['promoter']['name']} "
                                        f"promoter of Escherichia coli K-12 is located at -"
                                        f"{relative_position} position relative to the TSS")
                                
                    if tu["promoter"]["boxes"]:
                        # 8. The -10 box of the [PROMOTER_NAME] of 
                        # Escherichia coli K-12 is located at genome 
                        # positions [1 star position in the genome of the 
                        # -10 box] and [2 end position in the genome of the -10 box]
                        phrases.append(f"The -10 box of the {tu['promoter']['name']} "
                            f"of Escherichia coli K-12 is located at genome positions "
                            f"{tu['promoter']['boxes'][0]['rightEndPosition']} "
                            f"and {tu['promoter']['boxes'][0]['leftEndPosition']}") 
                           
                        if len(tu["promoter"]["boxes"]) == 2:
                            # 9. The -35 box of the [PROMOTER_NAME] promoter 
                            # of  Escherichia coli K-12 is located at genome
                            # positions [star position in the genome of the 
                            # -10 box] and [end position in the genome of the -35 box]
                            phrases.append(f"The -35 box of the {tu['promoter']['name']} "
                                f"promoter of Escherichia coli K-12 is located at "
                                f"genome positions {tu['promoter']['boxes'][1]['rightEndPosition']} "
                                f"and {tu['promoter']['boxes'][1]['leftEndPosition']}")
                            # 13. The sequence of the -35 box of the promoter 
                            # [PROMOTER_NAME] of  Escherichia coli K-12 is 
                            # [sequence of the -35 box of the [PROMOTER_NAME] ]
                            phrases.append(f"The sequence of the -35 box of the "
                                f"promoter {tu['promoter']['name']} of Escherichia coli "
                                f"K-12 is {tu['promoter']['boxes'][1]['sequence']}")
                        # 12. The sequence of the -10 box of the promoter 
                        # [PROMOTER_NAME] of  Escherichia coli K-12 is 
                        # [sequence of the -10 box of the [PROMOTER_NAME] ]
                        phrases.append(f"The sequence of the -10 box of the "
                            f"promoter {tu['promoter']['name']} of Escherichia "
                            f"coli K-12 is {tu['promoter']['boxes'][0]['sequence']}")
                    if tu["promoter"]["bindsSigmaFactor"] and tu["promoter"]["bindsSigmaFactor"]["citations"]:
                        for citation in tu["promoter"]["bindsSigmaFactor"]["citations"]:
                            if citation["evidence"]:
                            # 14. The -10 and -35 boxes of the 
                            # [PROMOTER_NAME] of  Escherichia coli K-12 
                            # has the evidence ["EVIDENCE"]
                                phrases.append(f"The -10 and -35 boxes of the "
                                    f"{tu['promoter']['name']} of Escherichia coli "
                                    f"K-12 has the evidence '{citation['evidence']['name']}'")
                                if tu["promoter"]["bindsSigmaFactor"]["name"]:
                                    # 16. The [Sigma_factor] transcribing 
                                    # the [PROMOTER_NAME] of  Escherichia 
                                    # coli K-12 has the evidence related to 
                                    # the promoter ["EVIDENCE"]
                                    phrases.append(f"The {tu['promoter']['bindsSigmaFactor']['name']} "
                                        f"transcribing the {tu['promoter']['name']} "
                                        f"of Escherichia coli K-12 has the evidence "
                                        f"related to the promoter '{citation['evidence']['name']}'")
                    # 15. The promoter [PROMOTER_NAME] of  Escherichia 
                    # coli K-12 is transcribed by the [Sigma_Factor_name]
                    if tu["promoter"]["bindsSigmaFactor"] and tu["promoter"]["bindsSigmaFactor"]["name"]:
                        phrases.append(f"The promoter {tu['promoter']['name']} "
                            f"of Escherichia coli K-12 is transcribed by the "
                            f"{tu['promoter']['bindsSigmaFactor']['name']}")
                    
                    if tu["promoter"]["sequence"]:
                        # 17. The sequence of the promoter [PROMOTER_NAME] 
                        # of  Escherichia coli K-12  is [sequence of the promoter]
                        phrases.append(f"The sequence of the promoter "
                            f"{tu['promoter']['name']} of Escherichia coli K-12 is "
                            f"{tu['promoter']['sequence']}")
                    # 18. The transcription of the transcription unit 
                    # (TU) [TU_name] is started at the promoter 
                    # [PROMOTER_NAME] of  Escherichia coli K-12
                    if tu["name"]:
                        phrases.append(f"The transcription of the transcription "
                            f"unit (TU) {tu['name']} is started at the promoter "
                            f"{tu['promoter']['name']} of Escherichia coli K-12")
                    if tu["genes"]:
                        for gene in tu["genes"]:
                            if ["name"]:
                                # 19. The transcription of the gene [gene_name] is 
                                # started at the promoter [PROMOTER_NAME] of Escherichia coli K-12
                                phrases.append(f"The transcription of the gene "
                                    f"{gene['name']} is started at the promoter "
                                    f"{tu['promoter']['name']} of Escherichia coli K-12")
                    if tu["promoter"]["regulatorBindingSites"]:
                        for regulatorBindingS in tu["promoter"]["regulatorBindingSites"]:
                            for regulatoryInteraction in regulatorBindingS["regulatoryInteractions"]:
                                if regulatoryInteraction["relativeCenterPosition"] and regulatorBindingS['function']:
                                    # 23. The transcription factor 
                                    # [TF_NAME] binds at positions [CENTER_POSITION]
                                    # relative to the transcriptional 
                                    # start site of the  promoter [PROMOTER_NAME] 
                                    # of  Escherichia coli K-12  to [activate/repress] it
                                    function = "activate" if regulatorBindingS["function"] == "activator" else "repress"
                                    phrases.append(f"The transcription factor "
                                        f"{regulatorBindingS['regulator']['name']} binds "
                                        f"at positions {regulatoryInteraction['relativeCenterPosition']} "
                                        f"relative to the transcriptional start "
                                        f"site of the promoter {tu['promoter']['name']} "
                                        f"of Escherichia coli K-12 to {function} it")
                            if regulatorBindingS["function"] == "activator":
                                # 20. The transcription factor  [TF_NAME] 
                                # activates the transcription of the 
                                # promoter [PROMOTER_NAME] of  Escherichia coli K-12
                                phrases.append(f"The transcription factor "
                                    f"{regulatorBindingS['regulator']['name']} "
                                    f"activates the transcription of the promoter "
                                    f"{tu['promoter']['name']} of Escherichia coli K-12")
                            elif regulatorBindingS["function"] == "repressor":
                                # 21. The transcription factor 
                                # [TF_NAME] represses the transcription 
                                # of the  promoter [PROMOTER_NAME] of Escherichia coli K-12
                                phrases.append(f"The transcription factor "
                                    f"{regulatorBindingS['regulator']['name']} "
                                    f"represses the transcription of the promoter "
                                    f"{tu['promoter']['name']} of Escherichia coli K-12")
                    if tu["promoter"]["note"]:
                        # 22. "The comment related to the [PROMOTER_NAME] 
                        # promoter of  Escherichia coli K-12 is "[NOTE] "
                        note = clean_text(tu["promoter"]["note"])
                        phrases.append(f"The comment related to the "
                            f"{tu['promoter']['name']} promoter of Escherichia "
                            f"coli K-12 is '{note}'")
              
    df = pd.DataFrame(phrases, columns=["Phrases"])
    df.to_csv("phrases.csv", index=False)
    # print(phrases)
else:
    raise Exception(f"Query failed to run with a {r.status_code}.")
    