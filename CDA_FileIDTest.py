from cdapython import   get_file_data
from urllib.parse import unquote
import pandas as pd
import requests
import json
import sys

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
        res = requests.post(url=apiurl, headers=headers, data=json.dumps(querycontent))
    except requests.exceptions.HTTPError as e:
        print(e)
    if res.status_code == 200:
        return json.loads(res.content.decode())
        
    else:
        print(res.status_code)
        print(res.content)
#csvfile = r'C:\Users\pihltd\Documents\DCFUsage\async_waf_audit_revproxy_matched_logs_merged_standard_format_with_geo_with_dc (1) 1.csv'
#reportfile = r'C:\Users\pihltd\Documents\DCFUsage\dcf_file_report.tsv'

#dcf_df = pd.read_csv(csvfile, sep=",")
#drslist = dcf_df['guid'].unique().tolist()
#print(f"DRS List lenght: {len(drslist)}")

#drs_df = dcf_df.value_counts('guid').reset_index().rename(columns={'index':'value', 0:'count'})
#print(drs_df)
drs1 = ["768c0d33-e543-4444-9e10-ab400ca25aa1"]
drs2 = ["688c440e-e6c8-412c-ac56-5ad559d3661c"]
drscombo = ["768c0d33-e543-4444-9e10-ab400ca25aa1", "688c440e-e6c8-412c-ac56-5ad559d3661c","dg.4DFC/202ea2f6-349b-47b6-9963-090cf62db87b"]

'''for drs in drscombo:
    drsres = cdaAPIQuery(drs)
    print(drsres['total_row_count'])

drsres = cdaAPIQuery(drscombo)
print(drsres['total_row_count'])'''

#drs = "dg.4DFC%2F9ade52a2-6ca4-5184-a4b8-71d396abc855"
#drs = unquote(drs)

#drs1res = get_file_data(*drs1)
#print(f"DRS1 search : {drs1}\n{drs1res}")

#drs2res = get_file_data(*drs2)
#print(f"DRS2 search : {drs2}\n{drs2res}")
searchlist = []
for fileid in drscombo:
    searchlist.append(f"file_id = {fileid}")

drscombores = get_file_data(match_any = searchlist)

print(f"DRSCombo search: {drscombo}\n{drscombores}")

#print(get_file_data(*("768c0d33-e543-4444-9e10-ab400ca25aa1", "688c440e-e6c8-412c-ac56-5ad559d3661c")))