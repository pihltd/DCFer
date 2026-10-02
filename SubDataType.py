from crdclib import crdclib
import pandas as pd
import argparse

def main(args):
  
  if args.verbose >= 1:
    print(f"Reading config file {args.configfile}")
    
  configs = crdclib.readYAML(args.configfile)
  
  query = """
  {
    listSubmissions(status:["All"]){
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
  if args.verbose >= 1:
    print("Obtaining credentials")
  creds = crdclib.dhAPICreds(tier=configs['tier'])
  
  if args.verbose >= 1:
    print("Running query for study information")
  res = crdclib.dhApiQuery(creds['url'], creds['token'], query=query)

  if args.verbose >= 1:
    print("Creating Dataframe")
  df = pd.json_normalize(res['data']['listSubmissions']['submissions'])
  
  

  if args.verbose >= 2:
    print(df)
    
  if args.verbose >= 1:
    print("Creating list of study name and abbreviations")
  big_kahuna = []
  for index, row in df.iterrows():
    big_kahuna.append({row['study.studyName']:row['study.studyAbbreviation']})
    
  big_kahuna = [dict(t) for t in {tuple(d.items()) for d in big_kahuna}]

  studylist = df['study.studyName'].unique().tolist()
  abbrevlist = df['study.studyAbbreviation'].unique().tolist()
  if args.verbose >= 2:
    print(f"List of all studies:\n{studylist}\n")
    print(f"List of all abbreviations:\n{abbrevlist}\n")

  #outputfile = r'C:\Users\pihltd\Documents\VMShare\studyNames.tsv'
  if args.verbose >= 1:
    print(f"Writing list of study names to file {configs['outputfiles']['studynamesFile']}")
  with open(configs['outputfiles']['studynamesFile'], 'wt') as f:
    f.write("\n".join(studylist))
    
  #outputfile = r'C:\Users\pihltd\Documents\VMShare\studyAbbrevs.tsv'
  if args.verbose >= 1:
      print(f"Writing list of study abbreviations to file {configs['outputfiles']['studyabbrevFile']}")
  with open(configs['outputfiles']['studyabbrevFile'], 'wt') as f:
    f.write("\n".join(abbrevlist))

  #outputfile = r'C:\Users\pihltd\Documents\VMShare\studycomplete.tsv'
  if args.verbose >= 1:
      print(f"Writing list of names and abbreviations to file {configs['outputfiles']['comboFile']}")
  with open(configs['outputfiles']['comboFile'],"wt") as f:
    f.write("Study Name\tStudyAbbreviation\n")
    for entry in big_kahuna:
      for name, abbrev in entry.items():
        f.write(f"{name}\t{abbrev}\n")
  if args.full_data:
    #outputfile = r'C:\Users\pihltd\Documents\VMShare\submission_type.tsv'
    if args.verbose >= 1:
      print(f"Writing full query output to {configs['outputfiles']['queryresultsFile']}")
    df.to_csv(configs['outputfiles']['queryresultsFile'], sep='\t', index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--configfile", required=True,  help="Configuration file containing all the input info")
    parser.add_argument('-v', '--verbose', action='count', default=0, help=("Verbosity: -v main section -vv subroutine messages -vvv data returned shown"))
    parser.add_argument('-f', '--full_data', action='store_true', help="Store the full query output to a file")

    args = parser.parse_args()

    main(args)