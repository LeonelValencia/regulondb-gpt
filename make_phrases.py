
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
        }
      }
    }
  }
}
"""

phrases = []
r = requests.post(endpoint, json={"query": query}, verify=False)
if r.status_code == 200:
    print(json.dumps(r.json(), indent=2))
    if r.json().get("data"):
        for operon in r.json()["data"]["getAllOperon"]["data"]:
            for tu in operon["transcriptionUnits"]:
                if tu["promoter"]:
                    phrases.append(f"The name of the promoter with the identifier of RegulonBB database {tu['promoter']['_id']} is {tu['promoter']['name']}")
    print(phrases)
else:
    raise Exception(f"Query failed to run with a {r.status_code}.")
    