#Gets a list of studies with data submitted from the DH API and creates the appropriate EDP files.
from crdclib import crdclib
import pandas as pd
import re
import yaml

def writeYAML(filename, jsonobj, sort=False):
    """Takes a filename and JSON object/dictionary and writes out a basic yaml file

    :param filename: A full path to the output file.
    :type filename: String
    :param jsonobj: A dictionary to be written as YAML.
    :type jsonobj: Dictionary
    :param sort: Alphabetically sort keys.  Optional and default is False.
    :type sort: Boolean
    """

    with open(filename, 'w') as f:
        yaml.safe_dump(jsonobj, f, sort_keys=sort)
    f.close()


query = """
{
  listSubmissions(status:"All"){
    submissions{
      _id
      name
      study{
        _id
        studyName
        studyAbbreviation
        dbGaPID
      }
    }
  }
}
"""

tier = 'prod'
creds = crdclib.dhAPICreds(tier=tier)

res = crdclib.dhApiQuery(creds['url'], creds['token'], query=query)

df = pd.json_normalize(res['data']['listSubmissions']['submissions'])
df.astype({"study.studyName":str}).dtypes

model = {}
terms = {}
finalterms = {}

prop_name = 'crdc_studyname_valueset'
description = 'A list of study names used in CRDC'
definition = 'EDP to provide a canonical list of Study Names approved for use in CRDC'
code = 'CRDC0006'
version = 1
value = 'CRDC Long study name'

studylist = df['study.studyAbbreviation'].unique().tolist()

model['PropDefinitions'] = {prop_name:{'Desc': description, 'Ext': 'True', 'Term':[{'Origin': 'CRDC', 'Definition': definition, 'Code': code, 'Version': version, 'Value': value}], 'Enum':studylist }}
model['Nodes'] = {}
model['Relationships'] = {}

for index, row in df.iterrows():
    studyName = row['study.studyName']
    studyName = re.sub(r'[^a-zA-Z0-9]+', ' ', studyName)
    studyName = studyName.rstrip().lstrip()

    terms[row['study.studyAbbreviation']] = {'Origin': 'CRDC', 'Code': row['study.studyAbbreviation'], 'Version': '1', 'Value': studyName, 'Definition': row['study.dbGaPID'] }
        
finalterms['Terms'] = terms

#propfile = r'C:\Users\pihltd\Documents\VMShare\EDPs\edp-props.yml'
#termfile = r'C:\Users\pihltd\Documents\VMShare\EDPs\crdcStudies-terms.yml'
propfile = r'C:\Users\pihltd\Documents\GitHub\bento-edps\model-desc\crdc-studynames-props.yml'
termfile = r'C:\Users\pihltd\Documents\GitHub\bento-edps\model-desc\terms\crdc-studynames-terms.yml'
reportfile = r'C:\Users\pihltd\Documents\VMShare\EDPs\DH_StudyNamess.tsv'
writeYAML(filename=propfile, jsonobj=model)
writeYAML(filename=termfile, jsonobj=finalterms)

df = df.drop(columns=['_id', 'name'])
df.drop_duplicates(inplace=True)
df.to_csv(reportfile, sep="\t", index=False)