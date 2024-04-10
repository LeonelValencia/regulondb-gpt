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
              _id
              citations{
                evidence{
                  name
                }
              }
              relativeCenterPosition 
              regulatorySite{
                sequence
                citations{
                   evidence{
                       name
                   } 
                }
              } 
            }
          }
          sequence
          synonyms
          transcriptionStartSite{ 
            leftEndPosition
          }
        }
      }
    }
  }
}
"""
data = {}
phrases = []
promoter_names = []
promoter_ids = []
synonyms = []
operon_strands = []
transcription_start_sites = []
tu_firstGene_distanceToPromoters = []
tu_firstGene_names = []
promoter_sequences = []
nucleotides = []
relative_positions_minus10 = []
relative_positions_minus35 = []
boxes_minus10_rightEndPosition = []
boxes_minus10_leftEndPosition = []
boxes_minus35_rightEndPosition = []
boxes_minus35_leftEndPosition = []
minus10_sequences = []
minus35_sequences = []
bindsSigmaFactor_names = []
tu_names = []
notes = []
citations_evidence_publications = []
pmids = []
citations_evidence_names = []
genes = []
regulatorBindingS_regulator_names = []
regulatoryInteraction_regulatorySite_sequences = []
regulatoryInteraction_relativeCenterPositions = []
regulatorBindingS_functions = []

r = requests.post(endpoint, json={"query": query}, verify=False)
if r.status_code == 200:
    if r.json().get("data"):
        for data in r.json()["data"]["getAllOperon"]["data"]:
            for tu in data["transcriptionUnits"]:
                if tu["promoter"]:
                    promoter_names.append(tu['promoter']['name'])
                    promoter_ids.append(tu['promoter']['_id'])
                    if tu["promoter"]["synonyms"]:
                        if len(tu["promoter"]["synonyms"]) > 1:
                            synonyms_str = ", ".join(tu["promoter"]["synonyms"])
                        else:
                            synonyms_str = tu["promoter"]["synonyms"][0]
                        synonyms.append(synonyms_str)
                    else:
                        synonyms.append("")
                    operon_strands.append(data["operon"]["strand"])
                    if tu["promoter"]["transcriptionStartSite"]:
                        transcription_start_sites.append(tu["promoter"]["transcriptionStartSite"]["leftEndPosition"])
                    else:
                        transcription_start_sites.append("")
                    if tu["firstGene"] and tu["firstGene"]["distanceToPromoter"]:
                        tu_firstGene_distanceToPromoters.append(tu["firstGene"]["distanceToPromoter"])
                    else:
                        tu_firstGene_distanceToPromoters.append("")
                    if tu["firstGene"] and tu["firstGene"]["name"]:
                        tu_firstGene_names.append(tu["firstGene"]["name"])
                    else:
                        tu_firstGene_names.append("")
                    if tu["promoter"]["sequence"]:
                        promoter_sequences.append(tu["promoter"]["sequence"])           
                        sequence = tu['promoter']['sequence']
                        nucleotide = re.findall(r'[A|T|G|C]', sequence)
                        nucleotides.append(nucleotide[0])
                        if tu["promoter"]["boxes"]:
                            relative_position = find_relative_position(sequence, 
                                tu["promoter"]["boxes"][0]["sequence"], nucleotide[0])
                            if relative_position is not None:
                                relative_positions_minus10.append(relative_position)
                            else:
                                relative_positions_minus10.append("")
                            if len(tu["promoter"]["boxes"]) == 2:
                                relative_position = find_relative_position(sequence, 
                                    tu["promoter"]["boxes"][1]["sequence"], nucleotide[0])
                                if relative_position is not None:
                                    relative_positions_minus35.append(relative_position)
                                else:
                                    relative_positions_minus35.append("")
                            else:
                                relative_positions_minus35.append("")
                        else:
                            relative_positions_minus10.append("")
                            relative_positions_minus35.append("")
                    else:
                        promoter_sequences.append("")
                        nucleotides.append("")
                        relative_positions_minus10.append("")
                        relative_positions_minus35.append("")
                    if tu["promoter"]["boxes"]:
                        boxes_minus10_rightEndPosition.append(tu["promoter"]["boxes"][0]["rightEndPosition"])
                        boxes_minus10_leftEndPosition.append(tu["promoter"]["boxes"][0]["leftEndPosition"])   
                        if len(tu["promoter"]["boxes"]) == 2:
                            boxes_minus35_rightEndPosition.append(tu["promoter"]["boxes"][1]["rightEndPosition"])
                            boxes_minus35_leftEndPosition.append(tu["promoter"]["boxes"][1]["leftEndPosition"])
                            minus35_sequences.append(tu["promoter"]["boxes"][1]["sequence"])
                        else:
                            boxes_minus35_rightEndPosition.append("")
                            boxes_minus35_leftEndPosition.append("")
                            minus35_sequences.append("")
                        minus10_sequences.append(tu["promoter"]["boxes"][0]["sequence"])
                    else:
                        boxes_minus10_rightEndPosition.append("")
                        boxes_minus10_leftEndPosition.append("")
                        boxes_minus35_rightEndPosition.append("")
                        boxes_minus35_leftEndPosition.append("")
                        minus10_sequences.append("")
                        minus35_sequences.append("")
                    if tu["promoter"]["bindsSigmaFactor"] and tu["promoter"]["bindsSigmaFactor"]["name"]:
                        bindsSigmaFactor_names.append(tu["promoter"]["bindsSigmaFactor"]["name"])
                    else:
                        bindsSigmaFactor_names.append("")
                    if tu["name"]:
                        tu_names.append(tu["name"])
                    else:
                        tu_names.append("")
                    if tu["promoter"]["note"]:
                        note = clean_text(tu["promoter"]["note"])
                        notes.append(note)
                    else:
                        notes.append("")

                    citations_evidence_publication_str = []
                    pmid_str = []
                    citations_evidence_name_str = []
                    gene_str = []
                    regulatorBindingS_regulator_name_str = []
                    regulatoryInteraction_regulatorySite_sequence_str = []
                    regulatoryInteraction_relativeCenterPosition_str = []
                    regulatorBindingS_function_str = []
                    for citation in tu["promoter"]["citations"]:
                        if citation["evidence"]:
                            if citation["publication"] and citation["publication"]["pmid"]:
                                citations_evidence_publication_str.append(f"The evidence '{citation['evidence']['name']}' linked to the reference PMID:{citation['publication']['pmid']}")

                        if citation["publication"] and citation["publication"]["pmid"]:
                            pmid_str.append(citation["publication"]["pmid"])

                    if tu["promoter"]["bindsSigmaFactor"] and tu["promoter"]["bindsSigmaFactor"]["citations"]:
                        for citation in tu["promoter"]["bindsSigmaFactor"]["citations"]:
                            if citation["evidence"]:
                                if tu["promoter"]["bindsSigmaFactor"]["name"]:
                                    citations_evidence_name_str.append(f"The evidence '{citation['evidence']['name']}'")
                    if tu["genes"]:
                        for gene in tu["genes"]:
                            gene_str.append(gene["name"])
                    if tu["promoter"]["regulatorBindingSites"]:
                        for regulatorBindingS in tu["promoter"]["regulatorBindingSites"]:
                            for regulatoryInteraction in regulatorBindingS["regulatoryInteractions"]:
                                if regulatoryInteraction["relativeCenterPosition"] and regulatorBindingS['function']:
                                    if regulatoryInteraction['regulatorySite']['sequence']:
                                        # 23. The transcription factor  {getAllOperon.data.transcriptionUnits.promoter.regulatorBindingSites.regulator.name} binds at the sequence {getAllOperon.data.transcriptionUnits.promoter.regulatorBindingSites.regulatoryInteractions.regulatorySite.sequence}, located at position  {getAllOperon.data.transcriptionUnits.promoter.regulatorBindingSites.regulatoryInteractions.relativeCenterPosition} relative to the transcriptional start site of the promoter {getAllOperon.data.transcriptionUnits.promoter.name} of  Escherichia coli K-12,  to {getAllOperon.data.transcriptionUnits.promoter.regulatorBindingSites.function} it 
                                        function = "activate" if regulatorBindingS["function"] == "activator" else "repress"
                                        regulatorBindingS_regulator_name_str.append(regulatorBindingS["regulator"]["name"])
                                        regulatoryInteraction_regulatorySite_sequence_str.append(regulatoryInteraction['regulatorySite']['sequence'])
                                        regulatoryInteraction_relativeCenterPosition_str.append(str(regulatoryInteraction['relativeCenterPosition']))
                                        regulatorBindingS_function_str.append(regulatorBindingS["function"])
                                        phrases.append(f"The transcription factor "
                                            f"{regulatorBindingS['regulator']['name']} binds at the sequence "
                                            f"{regulatoryInteraction['regulatorySite']['sequence']}, located at position "
                                            f"{regulatoryInteraction['relativeCenterPosition']} relative to the transcriptional start site of the promoter "
                                            f"{tu['promoter']['name']} of Escherichia coli K-12, to {function} it")
                            
                                    if regulatoryInteraction["regulatorySite"]["citations"]:
                                        for citation in regulatoryInteraction["regulatorySite"]["citations"]:
                                            if citation["evidence"]:
                                                function = "activate" if regulatorBindingS["function"] == "activator" else "repress"
                                                for pcitation in tu["promoter"]["citations"]:
                                                    if pcitation["publication"] and pcitation["publication"]["pmid"]:
                                                        if citation['evidence']:
                                                            # 24 The evidence {getAllOperon.data.transcriptionUnits.promoter.regulatorBindingSites.regulatoryInteractions.regulatorySite.citations.evidence.name},  linked to the reference {getAllOperon.data.transcriptionUnits.promoter.citations.publication.pmid},  supports  the existing of the Regulatory DNA binding site or  binding of  {getAllOperon.data.transcriptionUnits.promoter.regulatorBindingSites.regulator.name} located at position  {getAllOperon.data.transcriptionUnits.promoter.regulatorBindingSites.regulatoryInteractions.relativeCenterPosition} relative to the transcriptional start site of the  promoter {getAllOperon.data.transcriptionUnits.promoter.name} of  Escherichia coli K-12,   to {getAllOperon.data.transcriptionUnits.promoter.regulatorBindingSites.function} it.
                                                            phrases.append(f"""The evidence {citation['evidence']['name']}, 
                                                                           linked to the reference {pcitation['publication']['pmid']}, 
                                                                           supports the existence of the Regulatory DNA 
                                                                           binding site or binding of {regulatorBindingS['regulator']['name']} 
                                                                           located at position {regulatoryInteraction['relativeCenterPosition']} 
                                                                           relative to the transcriptional start site of the 
                                                                           promoter {tu['promoter']['name']} of Escherichia coli K-12, 
                                                                           to {function} it""")
                                                # 26. The evidence {getAllOperon.data.transcriptionUnits.promoter.regulatorBindingSites.regulatoryInteractions.regulatorySite.citations.evidence.name} supports  the existing of the Regulatory DNA binding site or  binding of  {getAllOperon.data.transcriptionUnits.promoter.regulatorBindingSites.regulator.name} located at position  {getAllOperon.data.transcriptionUnits.promoter.regulatorBindingSites.regulatoryInteractions.relativeCenterPosition} relative to the transcriptional start site of the  promoter {getAllOperon.data.transcriptionUnits.promoter.name} of  Escherichia coli K-12,   to {getAllOperon.data.transcriptionUnits.promoter.regulatorBindingSites.function} it.
                                                phrases.append(f"""The evidence {citation['evidence']['name']} supports 
                                                               the existence of the Regulatory DNA binding site 
                                                               or binding of {regulatorBindingS['regulator']['name']} 
                                                               located at position {regulatoryInteraction['relativeCenterPosition']} 
                                                               relative to the transcriptional start site of the 
                                                               promoter {tu['promoter']['name']} of Escherichia 
                                                               coli K-12, to {function} it""")
                                    if regulatoryInteraction["citations"]:
                                        function = "activate" if regulatorBindingS["function"] == "activator" else "repress"
                                        for citation in regulatoryInteraction["citations"]:
                                            if citation["evidence"]:
                                                for pcitation in tu["promoter"]["citations"]:
                                                    if pcitation["publication"] and pcitation["publication"]["pmid"]:
                                                        if citation['evidence']:
                                                            # 25. The evidence {getAllOperon.data.transcriptionUnits.promoter.regulatorBindingSites.regulatoryInteractions.citations.evidence.name} linked to the reference {getAllOperon.data.transcriptionUnits.promoter.citations.publication.pmid},  supports  the effect caused by   {getAllOperon.data.transcriptionUnits.promoter.regulatorBindingSites.regulator.name} bound at position  {getAllOperon.data.transcriptionUnits.promoter.regulatorBindingSites.regulatoryInteractions.relativeCenterPosition} relative to the transcriptional start site of the  promoter {getAllOperon.data.transcriptionUnits.promoter.name} of  Escherichia coli K-12,  to {getAllOperon.data.transcriptionUnits.promoter.regulatorBindingSites.function} it.
                                                            phrases.append(f"""The evidence {citation['evidence']['name']} 
                                                                           linked to the reference {pcitation['publication']['pmid']}, 
                                                                           supports the effect caused by 
                                                                           {regulatorBindingS['regulator']['name']} 
                                                                           bound at position {regulatoryInteraction['relativeCenterPosition']} 
                                                                           relative to the transcriptional start site 
                                                                           of the promoter {tu['promoter']['name']} 
                                                                           of Escherichia coli K-12, to {function} it""")
                                                # 27. The evidence {getAllOperon.data.transcriptionUnits.promoter.regulatorBindingSites.regulatoryInteractions.citations.evidence.name} supports  the effect caused by {getAllOperon.data.transcriptionUnits.promoter.regulatorBindingSites.regulator.name} bound at position  {getAllOperon.data.transcriptionUnits.promoter.regulatorBindingSites.regulatoryInteractions.relativeCenterPosition} relative to the transcriptional start site of the  promoter {getAllOperon.data.transcriptionUnits.promoter.name} of  Escherichia coli K-12,   to {getAllOperon.data.transcriptionUnits.promoter.regulatorBindingSites.function} it.
                                                phrases.append(f"""The evidence {citation['evidence']['name']} supports 
                                                               the effect caused by {regulatorBindingS['regulator']['name']} 
                                                               bound at position {regulatoryInteraction['relativeCenterPosition']} 
                                                               relative to the transcriptional start site of the 
                                                               promoter {tu['promoter']['name']} of Escherichia coli K-12, 
                                                               to {function} it""")
                                # 28. In the publication with PMID:{getAllOperon.data.transcriptionUnits.promoter.citations.publication.pmid} was reported the regulatory interaction, with the identifier of RegulonDB database {getAllOperon.data.transcriptionUnits.promoter.regulatorBindingSites.regulatoryInteractions._id}, between the transcription Factor (TF) {getAllOperon.data.transcriptionUnits.promoter.regulatorBindingSites.regulator.name}  and the promoter {getAllOperon.data.transcriptionUnits.promoter.name} in which the TF {getAllOperon.data.transcriptionUnits.promoter.regulatorBindingSites.function} to the promoter.
                                for pcitation in tu["promoter"]["citations"]:
                                    if pcitation["publication"] and pcitation["publication"]["pmid"]:
                                        function = "activate" if regulatorBindingS["function"] == "activator" else "repress"
                                        phrases.append(f"""In the publication with PMID:{pcitation['publication']['pmid']} 
                                                       was reported the regulatory interaction, with the identifier of 
                                                       RegulonDB database {regulatoryInteraction['_id']}, between the 
                                                       transcription Factor (TF) {regulatorBindingS['regulator']['name']} 
                                                       and the promoter {tu['promoter']['name']} in which the TF 
                                                       {function} to the promoter""")
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

                    if citations_evidence_publication_str:
                        citations_evidence_publications.append(", ".join(citations_evidence_publication_str))
                    else:
                        citations_evidence_publications.append("")
                    if pmid_str:
                        pmids.append(", ".join(set(pmid_str)))
                    else:
                        pmids.append("")
                    if citations_evidence_name_str:
                        citations_evidence_names.append(", ".join(citations_evidence_name_str))
                    else:
                        citations_evidence_names.append("")
                    if gene_str:
                        genes.append(", ".join(gene_str))
                    else:
                        genes.append("")
                    if regulatorBindingS_regulator_name_str:
                        regulatorBindingS_regulator_names.append(", ".join(set(regulatorBindingS_regulator_name_str)))
                    else:
                        regulatorBindingS_regulator_names.append("")
                    if regulatoryInteraction_regulatorySite_sequence_str:
                        regulatoryInteraction_regulatorySite_sequences.append(", ".join(regulatoryInteraction_regulatorySite_sequence_str))
                    else:
                        regulatoryInteraction_regulatorySite_sequences.append("")
                    if regulatoryInteraction_relativeCenterPosition_str:
                        regulatoryInteraction_relativeCenterPositions.append(", ".join(regulatoryInteraction_relativeCenterPosition_str))
                    else:
                        regulatoryInteraction_relativeCenterPositions.append("")
                    if regulatorBindingS_function_str:
                        regulatorBindingS_functions.append(", ".join(regulatorBindingS_function_str))
                    else:
                        regulatorBindingS_functions.append("")
    
    print(len(promoter_ids), "promoters_ids")
    print(len(promoter_names), "promoter_names")
    print(len(synonyms), "synonyms")
    print(len(operon_strands), "operon_strands")
    print(len(transcription_start_sites), "transcription_start_sites")
    print(len(tu_firstGene_distanceToPromoters), "tu_firstGene_distanceToPromoters")
    print(len(tu_firstGene_names), "tu_firstGene_names")
    print(len(promoter_sequences), "promoter_sequences")
    print(len(nucleotides), "nucleotides")
    print(len(relative_positions_minus10), "relative_positions_minus10")
    print(len(relative_positions_minus35), "relative_positions_minus35")
    print(len(boxes_minus10_rightEndPosition), "boxes_minus10_rightEndPosition")
    print(len(boxes_minus10_leftEndPosition), "boxes_minus10_leftEndPosition")
    print(len(boxes_minus35_rightEndPosition), "boxes_minus35_rightEndPosition")
    print(len(boxes_minus35_leftEndPosition), "boxes_minus35_leftEndPosition")
    print(len(minus10_sequences), "minus10_sequences")
    print(len(minus35_sequences), "minus35_sequences")
    print(len(bindsSigmaFactor_names), "bindsSigmaFactor_name_str")
    print(len(tu_names), "tu_names")
    print(len(notes), "notes")
    print(len(citations_evidence_publications), "citations_evidence_publications")
    print(len(pmids), "pmids")
    print(len(citations_evidence_names), "citations_evidence_names")
    print(len(genes), "genes")
    print(len(regulatorBindingS_regulator_names), "regulatorBindingS_regulator_names")
    print(len(regulatoryInteraction_regulatorySite_sequences), "regulatoryInteraction_regulatorySite_sequences")
    print(len(regulatoryInteraction_relativeCenterPositions), "regulatoryInteraction_relativeCenterPositions")
    print(len(regulatorBindingS_functions), "regulatorBindingS_functions")
                        
    d = {'promoter_id': promoter_ids,
            'promoter_name': promoter_names,
            'synonyms': synonyms,
            'operon_strand': operon_strands,
            'transcription_start_site': transcription_start_sites,
            'tu_firstGene_distanceToPromoter': tu_firstGene_distanceToPromoters,
            'tu_firstGene_name': tu_firstGene_names,
            'promoter_sequence': promoter_sequences,
            'nucleotide': nucleotides,
            'relative_position_minus10': relative_positions_minus10,
            'relative_position_minus35': relative_positions_minus35,
            'boxes_minus10_rightEndPosition': boxes_minus10_rightEndPosition,
            'boxes_minus10_leftEndPosition': boxes_minus10_leftEndPosition,
            'boxes_minus35_rightEndPosition': boxes_minus35_rightEndPosition,
            'boxes_minus35_leftEndPosition': boxes_minus35_leftEndPosition,
            'minus10_sequence': minus10_sequences,
            'minus35_sequence': minus35_sequences,
            'bindsSigmaFactor_name': bindsSigmaFactor_names,
            'tu_name': tu_names,
            'note': notes,
            "citations_evidence_publication": citations_evidence_publications,
            "pmid": pmids,
            "citations_evidence_name": citations_evidence_names,
            "genes": genes,
            "regulatorBindingS_regulator_name": regulatorBindingS_regulator_names,
            "regulatoryInteraction_regulatorySite_sequence": regulatoryInteraction_regulatorySite_sequences,
            # "regulatoryInteraction_relativeCenterPosition": regulatoryInteraction_relativeCenterPositions,
            # "regulatorBindingS_function": regulatorBindingS_functions
         }              
    df = pd.DataFrame(data=d)
    df.to_csv("table.tsv", index=False, sep="\t")
    # with open("phrases.txt", "w") as archivo:
    #     for elemento in phrases:
    #         archivo.write(elemento + "\n")
    # print(phrases)
else:
    raise Exception(f"Query failed to run with a {r.status_code}.")
    