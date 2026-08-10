from crdclib import crdclib
import pandas as pd

query = """
{
  listSubmissions(status:["Completed", "In Progress", "New", "Rejected", "Withdrawn"]){
    submissions{
      _id
      name
      study{
        studyName
        studyAbbreviation
        dbGaPID
      }
      dataCommons
      modelVersion
      nodeCount
      submitterName
      status
      dataType
    }
  }
}
"""

tier = 'prod'
creds = crdclib.dhAPICreds(tier=tier)

res = crdclib.dhApiQuery(creds['url'], creds['token'], query=query)

#df = pd.DataFrame(res['data']['listSubmissions']['submissions'])
df = pd.json_normalize(res['data']['listSubmissions']['submissions'])

print(df)

outputfile = r'C:\Users\pihltd\Documents\VMShare\submission_type.tsv'
df.to_csv(outputfile, sep='\t', index=False)

