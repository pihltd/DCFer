from crdclib import crdclib
import pandas as pd

'''
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
'''

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

#print(df)
big_kahuna = []
for index, row in df.iterrows():
  big_kahuna.append({row['study.studyName']:row['study.studyAbbreviation']})
  
big_kahuna = [dict(t) for t in {tuple(d.items()) for d in big_kahuna}]

studylist = df['study.studyName'].unique().tolist()
abbrevlist = df['study.studyAbbreviation'].unique().tolist()
print(studylist)
print(abbrevlist)

outputfile = r'C:\Users\pihltd\Documents\VMShare\studyNames.tsv'
with open(outputfile, 'wt') as f:
  f.write("\n".join(studylist))
  
outputfile = r'C:\Users\pihltd\Documents\VMShare\studyAbbrevs.tsv'
with open(outputfile, 'wt') as f:
  f.write("\n".join(abbrevlist))

outputfile = r'C:\Users\pihltd\Documents\VMShare\studycomplete.tsv'
with open(outputfile,"wt") as f:
  f.write("Study Name\tStudyAbbreviation\n")
  for entry in big_kahuna:
    for name, abbrev in entry.items():
      f.write(f"{name}\t{abbrev}\n")

#outputfile = r'C:\Users\pihltd\Documents\VMShare\submission_type.tsv'
#df.to_csv(outputfile, sep='\t', index=False)

