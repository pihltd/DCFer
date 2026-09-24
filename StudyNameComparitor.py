#Compares two files of study names.  Done for Ina
import pandas as pd
from fuzzywuzzy import process, fuzz

def mapit (sourcelist, targetlist):
    mappedfinal = []
    unmappedfinal = []
    for source in sourcelist:
        if source in targetlist:
            mappedfinal.append(source)
        else:
            unmappedfinal.append(source)
    return mappedfinal, unmappedfinal

def mapit_df(sourcelist, targetlist, finalmess, sourcetag, targettag):
    for source in sourcelist:
        if source in targetlist:
            finalmess.append({'Source': sourcetag, 'Source field': source, 'Target': targettag, 'Target field': source, 'Mapped': 'Exact'})
            sourcelist.remove(source)
    #Now get best fuzzy search match
    for source in sourcelist:
        bm = process.extractOne(source, targetlist, scorer=fuzz.token_sort_ratio)
        finalmess.append({'Source': sourcetag, 'Source field': source, 'Target': targettag, 'Target field': bm[0], 'Mapped': 'Fuzzy'})
        sourcelist.remove(source)
    #If anything is left, document it....
    if len(sourcelist) >= 1:
        for source in sourcelist:
            finalmess.append({'Source': sourcetag, 'Source field': source, 'Target': targettag, 'Target field':None, 'Mapped': 'No'})
      
            
    return finalmess
            
SRF_file = r'C:\Users\pihltd\Documents\VMShare\StudyNames\study-names-from-srf.csv'
SubPort_file = r'C:\Users\pihltd\Documents\VMShare\StudyNames\DH_StudyNamess.tsv'

srf_df = pd.read_csv(SRF_file, sep=",")
sp_df = pd.read_csv(SubPort_file, sep="\t")

srf_names = srf_df['studyName'].unique().tolist()
sp_names = sp_df['study.studyName'].unique().tolist()

srf_mapped, srf_unmapped = mapit(sourcelist=srf_names, targetlist=sp_names)
sp_mapped, sp_unmapped = mapit(sourcelist=sp_names, targetlist=srf_names)

print(f"Starting SRF: {len(srf_names)}\t Mapped SRF: {len(srf_mapped)}\t Unmapped SRF: {len(srf_unmapped)}")
print(f"Starting SP: {len(sp_names)}\tMapped SP: {len(sp_mapped)}\t Unmapped SP: {len(sp_unmapped)}")

final = []
final = mapit_df(sourcelist=srf_names, targetlist=sp_names, finalmess=final, sourcetag='SRF', targettag='SubPortal')
final = mapit_df(sourcelist=sp_names, targetlist=srf_names, finalmess=final, sourcetag='SubPortal', targettag='SRF')

final_df = pd.DataFrame(final)

reportfile = r'C:\Users\pihltd\Documents\VMShare\StudyNames\StudyNameReport.tsv'

final_df.to_csv(reportfile, sep="\t", index=False)