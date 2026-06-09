from cdapython import   get_file_data
from urllib.parse import unquote
import pandas as pd
from rich.progress import Progress

def listChunker(listname, chunksize):
    return (listname[pos:pos + chunksize] for pos in range(0, len(listname), chunksize))

csvfile = r'C:\Users\pihltd\Documents\DCFUsage\async_waf_audit_revproxy_matched_logs_merged_standard_format_with_geo_with_dc (1) 1.csv'
reportfile = r'C:\Users\pihltd\Documents\DCFUsage\CDA_mapped_files.tsv'
nonefile = r'C:\Users\pihltd\Documents\DCFUsage\CDA_unmapped_drsIDs.tsv'

nonelist = []
final_df = pd.DataFrame()

print(f"Reading starting file {csvfile}")
start_df = pd.read_csv(csvfile, sep=",")
print("Getting file ID list")
fileidList = []
tempList = start_df['guid'].unique().tolist()
for entry in tempList:
    fileidList.append(unquote(entry))

print(f"There are {len(fileidList)} file IDs to process")
counter = 0
chunksize = 100

with Progress() as pb:
    cdatask = pb.add_task("Querying CDA.....", total=len(fileidList))
    for idgroup in listChunker(fileidList, chunksize):
        #print(idgroup)
        temp_df = get_file_data(*idgroup)
        print(f"DF Size: {len(temp_df)}\n{temp_df}")
        
        
    '''for drsid in fileidList:
        drsid = unquote(drsid)
        temp_df = get_file_data(drsid)
        #print(f"File ID: {drsid}\n{temp_df}\n")
        #if temp_df is None:
        #    nonelist.append(drsid)
        if temp_df.empty:
            nonelist.append(drsid)
        else:
            final_df = pd.concat([final_df, temp_df])
        counter = counter + 1'''
    pb.update(task_id=cdatask, completed= counter + chunksize)

final_df.to_csv(reportfile, sep="\t")
with open(nonefile, "w") as f:
    f.write("Unmapped DRS IDs\n")
    for id in fileidList:
        f.write(f"{id}\n")
