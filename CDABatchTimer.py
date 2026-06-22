from cdapython import   get_file_data
from urllib.parse import unquote
from rich.progress import Progress
import requests
import os
import pandas as pd
from pathlib import Path
import time
import random




intervals = [1,5,10,20,50, 60, 70, 80, 90, 100]

csvfile = r'C:\Users\pihltd\Documents\DCFUsage\async_waf_audit_revproxy_matched_logs_merged_standard_format_with_geo_with_dc (1) 1.csv'
reportfile = r'C:\Users\pihltd\Documents\DCFUsage\CDA_timer.tsv'

print(f"Reading starting file {csvfile}")
start_df = pd.read_csv(csvfile, sep=",")
print("Getting file ID list")
fileidList = []
tempList = start_df['guid'].unique().tolist()
for entry in tempList:
    fileidList.append(unquote(entry))

results = []
for interval in intervals:
    tempres = []
    with Progress() as pb:
        cdapythonquery = pb.add_task(f"Querying CDA Python interval {interval}...", total=10)
        for x in range(10):
            querylist = random.sample(fileidList, interval)
            querygroup = []
            for id in querylist:
                querygroup.append(f"file_id = {id}")
            start = time.perf_counter()
            res_df = get_file_data(match_any=querygroup)
            stop = time.perf_counter()
            tempres.append({'interval':interval, 'start':start, 'stop':stop, 'diff':(stop-start)})
            pb.update(task_id=cdapythonquery, advance=1)
            
        temp_df = pd.DataFrame(tempres)
        querymean = temp_df.loc[:,'diff'].mean()
        results.append({'interval': interval, 'mean_time': querymean, 'per_file':(querymean/interval)})

res_df = pd.DataFrame(results)
res_df.to_csv(reportfile, sep="\t", index=False, mode='a')