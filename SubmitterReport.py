# This is a weird one, it tries to summarize how much a submitter has submitted
from crdclib import crdclib
from crdclib import dhqueries as q
import pandas as pd
import sys



tier = 'prod'
dc = 'ICDC'
name = 'Christina Madsen'
#status = ["Completed", "Released", "Submitted"]
status = ["Completed"]
outputfile = r'C:\Users\pihltd\Documents\datadir\c_madsen.tsv'

query = """
query DoneAndDusted(
  $status: [String]!,
  $dc: String!,
  $name: String!
)
{
  listSubmissions(
    status: $status, 
    dataCommons: $dc, 
    submitterName: $name){
    submissions{
      _id
      name
      study{
          _id
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

vars = {"status": status, "dc": dc, "name": name}

creds = crdclib.dhAPICreds(tier=tier)

resjson = crdclib.dhApiQuery(url=creds['url'], apitoken=creds['token'],query=query, variables=vars)

#df = pd.DataFrame(resjson['data']['listSubmissions']['submissions'])
df = pd.json_normalize(resjson['data']['listSubmissions']['submissions'])

print(df)
print(df.columns)
#sys.exit(0)

nodecounts = []
for index, row in df.iterrows():
    vars = {"dc": dc, "studyID": row["study._id"]}
    print(f"id: {row['study._id']}\tName: {row['name']}\tStatus: {row['status']}")
    resjson = crdclib.dhApiQuery(url=creds['url'], apitoken=creds['token'], query=q.node_count_query, variables=vars)
    for entry in resjson['data']['getReleaseNodeTypes']['nodes']:
        nodecounts.append({'name':row['study.studyName'], 'abbreviation':row['study.studyAbbreviation'], 'field':entry['name'], 'count':entry['count']})
    #print(resjson)
    #nodecounts.append(resjson['data']['getReleaseNodeTypes']['nodes'])

count_df = pd.DataFrame(nodecounts)
#print(count_df)
count_df.to_csv(outputfile, sep="\t", index=False)
