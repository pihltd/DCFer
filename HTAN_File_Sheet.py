import pandas as pd
import sys

#missing_file = r'C:\Users\pihltd\Documents\HTAN Files\a0d4fe90-c639-4339-b295-37275903ac28_file_integrity_results.txt'
missing_file = r'C:\Users\pihltd\Documents\HTAN Files\missing_only.txt'
with open(missing_file, 'r') as mf:
    mf_lines = mf.readlines()
missing_info = {}
#missing = False
for line in mf_lines:
    #if 'Missing' in line:
    #    missing = True
    #elif 'Wrong' in line:
    #    missing = False
    #if missing:
    if '4DFC' in line:
        fileinfo = line.split(':')
        missing_info[fileinfo[0].strip()] = fileinfo[-1].strip()
#print(missing_info)

#dh_file = r'C:\Users\pihltd\Documents\HTAN Files\HTAN image_file_20260805161830.tsv'
dh_file = r'C:\Users\pihltd\Documents\HTAN Files\HTAN image_file_20260806104455.tsv'
dh_df = pd.read_csv(dh_file, sep="\t")

final_df = pd.DataFrame()
missinguuidlist = list(missing_info.keys())
#print(uuidlist)
final_df = dh_df[dh_df['file_id'].isin(missinguuidlist)]
final_df['file_size'] = final_df['file_size'].astype(int)
final_df.insert(loc=0, column='type',value='file')

final_id_list = final_df['file_id'].unique().tolist()

final_sorted = sorted(final_id_list)
missinguuid_sorted = sorted(missinguuidlist)
if missinguuid_sorted == final_sorted:
    print("Lists Match")
else:
    print(f"List mismatch\nFinal length: {len(final_sorted)}\t Missing length: {len(missinguuid_sorted)}")
    for each in missinguuid_sorted:
        if each not in final_sorted:
            print(f"{each}\t{missing_info[each]}")
    

#sys.exit(0)
#Check the UUID and filenames match
for fileid, filename in missing_info.items():
    temp_df = final_df.query("file_id== @fileid")
    namelist = temp_df['file_name'].unique().tolist()
    if len(namelist) > 1:
        print(f"Multiple names: {namelist}")
    elif len(namelist) == 1:
        if filename != namelist[0]:
            print(f"Filename mismatch! Query: {filename}\t Data: {namelist[0]}")
    else:
        print(f"No filename available for Query {filename}")
    #print(f"Test:\t{((final_df.loc['file_id'] == fileid) and (final_df.loc['file_name'] == filename)).any()}")
    #if not ((final_df['file_id'] == fileid) and (final_df['file_name'] == filename)).any():
        #print(f"Mismatch!\t Search ID: {fileid} vs Filename: {filename}")

outfile = r'C:\Users\pihltd\Documents\HTAN Files\HTAN_Missing_Manifest.tsv'
final_df.to_csv(outfile, sep="\t", index=False)
        
    