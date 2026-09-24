#A request from Ina to count cases by submitter/Program
from crdclib import crdclib
import pandas as pd
from rich.progress import Progress

# The Data Explorer uses Data Commons and study IDs to organize things
# Step one is to get released studies

dclist = ["ICDC", "CTDC", "GC"]


releasedQuery = """
query ListReleasedStudies(
  $displayname: [String]!
  $first: Int
){
  listReleasedStudies(
    dataCommonsDisplayNames: $displayname
    first: $first
  ){
    studies{
      _id
      studyName
      studyAbbreviation
      dataCommons
    }
  }
}
"""

releasedvars = {"displayname": dclist, "first": -1}

apistuff = crdclib.dhAPICreds("prod")

# NOTE: This may need to be paginated if it gets much bigger
releasedjson = crdclib.dhApiQuery(url=apistuff['url'],apitoken=apistuff['token'],query=releasedQuery,variables=releasedvars)

studylist = []
with Progress() as sp:
    st = sp.add_task("Processing studies...", total=len(releasedjson['data']['listReleasedStudies']['studies']))
    while not sp.finished:
        for study in releasedjson['data']['listReleasedStudies']['studies']:
            sp.update(st, advance=1)
            studylist.append({'id':study['_id'], 'studyName':study['studyName'], 'studyAbbreviation':study['studyAbbreviation'], 'dc':study['dataCommons'][0]})

study_df = pd.DataFrame(studylist)
print(study_df)

# Now see if we can get the programs that go with the studies
programstudyquery = """
{
  listPrograms{
    programs{
      name
      studies{
        studyAbbreviation
        studyName
      }
    }
  }
}
"""

programjson = crdclib.dhApiQuery(url=apistuff['url'], apitoken=apistuff['token'], query=programstudyquery)

programstuff = {}
for program in programjson['data']['listPrograms']['programs']:
    for study in program['studies']:
        programstuff[study['studyAbbreviation']] = program['name']
    
print(programstuff)


caselabels = {"GC":"participant", "CTDC": "participant", "ICDC": "case", "CDS": "participant"}

nodecountquery = """
query GetReleasedNodes(
  $dc: String!
  $studyID: String!
){
  getReleaseNodeTypes(
    dataCommonsDisplayName: $dc
    studyID: $studyID
  ){
    nodes{
      name
      count
    }
  }
}
"""
countinfo = []
programinfo = []

with Progress() as cp:
    ct = cp.add_task('Getting case counts...', total=len(study_df))
    while not cp.finished:
        for index, row in study_df.iterrows():
            nocase = True
            #print(row)
            cp.update(ct, advance=1)
            vars = {"dc": row['dc'], "studyID": row['id']}
            countjson = crdclib.dhApiQuery(url=apistuff['url'], apitoken=apistuff['token'], query=nodecountquery, variables=vars)
            for entry in countjson['data']['getReleaseNodeTypes']['nodes']:
                if caselabels[row['dc']] == entry['name']:
                    print(f"Adding count {entry['count']} for study {row['studyAbbreviation']}")
                    countinfo.append(entry['count'])
                    nocase = False
            if nocase:
                print(f"Adding 0 for study {row['studyAbbreviation']}")
                countinfo.append(0)
            if row['studyAbbreviation'] in programstuff.keys():
                programinfo.append(programstuff[row['studyAbbreviation']])
            else:
                programinfo.append("No Program Listed")
            

study_df['caseCount'] = countinfo
study_df['program'] = programinfo


summaryfile = r'C:\Users\pihltd\Documents\VMShare\StudyNames\SubmittedCaseCounts.tsv'
study_df.to_csv(summaryfile, sep="\t", index=False)


programlist = study_df['program'].unique().tolist()
programcount = []
for program in programlist:
    program_df = study_df.query('program == @program')
    programcount.append({'program':program, 'count':program_df['caseCount'].sum()})
    
count_df  = pd.DataFrame(programcount)

programcountfile = r'C:\Users\pihltd\Documents\VMShare\StudyNames\ProgramCaseCounts.tsv'
count_df.to_csv(programcountfile, sep="\t", index=False)