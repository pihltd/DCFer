from cdapython import   get_file_data
from urllib.parse import unquote
import pandas as pd
from rich.progress import Progress
import requests
import os
from pathlib import Path


def cdaAPIQuery(fileID):
    apiurl = "https://cda-dev.datacommons.cancer.gov/data/file?limit=100&offset=0"
    headers = {'accept':'applicaiton/json', 'Content-Type':'application/json'}
    
    querycontent = {}
    if type(fileID) == str:
        querycontent["SEARCH_LIST"] = [fileID]
    elif type(fileID) == list:
        querycontent['SEARCH_LIST'] = fileID
    else:
        return None
    querycontent["COLLATE_RESULTS"] = False
    querycontent['EXTERNAL_REFERENCE'] = False
    querycontent['MATCH_ALL'] = []
    querycontent['MATCH_SOME'] = []
    querycontent['ADD_COLUMNS'] = []
    querycontent['EXCLUDE_COLUMNS'] = []
    try:
        res = requests.post(url=apiurl, headers=headers, params=querycontent)
    except requests.exceptions.HTTPError as e:
        print(e)
    if res.status_code == 200:
        print(res)
    else:
        print(res.status_code)

def listChunker(listname, chunksize):
    return (listname[pos:pos + chunksize] for pos in range(0, len(listname), chunksize))


def filePrep(reportfile):
    if os.path.isfile(reportfile):
        os.remove(reportfile)
    Path(reportfile).touch()
        

csvfile = r'C:\Users\pihltd\Documents\DCFUsage\async_waf_audit_revproxy_matched_logs_merged_standard_format_with_geo_with_dc (1) 1.csv'
reportfile = r'C:\Users\pihltd\Documents\DCFUsage\CDA_mapped_files.tsv'
nonefile = r'C:\Users\pihltd\Documents\DCFUsage\CDA_unmapped_drsIDs.tsv'

restart = True



nonelist = []
final_df = pd.DataFrame()

print(f"Reading starting file {csvfile}")
start_df = pd.read_csv(csvfile, sep=",")
print("Getting file ID list")
fileidList = []
tempList = start_df['guid'].unique().tolist()
for entry in tempList:
    fileidList.append(unquote(entry))

if restart:
    print('Restarting dropped process')
    existing_df = pd.read_csv(reportfile, sep="\t")
    mappedlist = existing_df['file_id'].unique().tolist()
    unmappedlist = Path(nonefile).read_text().splitlines()
    print("Cleaning ID list")
    for id in fileidList:
        if id in mappedlist:
            fileidList.remove(id)
        elif id in unmappedlist:
            fileidList.remove(id)
        
else:
 filePrep(reportfile=reportfile)
 filePrep(reportfile=nonefile)

print(f"There are {len(fileidList)} file IDs to process")
counter = 0
chunksize = 10

with Progress() as pb:
    cdatask = pb.add_task("Querying CDA.....", total=len(fileidList))
    for idgroup in listChunker(fileidList, chunksize):
        querygroup = []
        for id in idgroup:
            querygroup.append(f"file_id = {id}")
        #print(idgroup)
        temp_df = get_file_data(match_any = querygroup)
        if counter == 0:
            if temp_df is not None:
                temp_df.to_csv(reportfile, mode='a', sep="\t", index=False)
        else:
            if temp_df is not None:
                temp_df.to_csv(reportfile, mode='a', sep="\t", index=False, header=False)
        with open(nonefile, '+a') as f:
            if 'file_id' in temp_df:
                foundlist = temp_df['file_id'].unique().tolist()
                for id in idgroup:
                    if id not in foundlist:
                        f.write(f"{id}\n")
        
        #print(f"DF Size: {len(temp_df)}\n{temp_df}")
        counter = counter + chunksize
        pb.update(task_id=cdatask, completed= counter + chunksize)
