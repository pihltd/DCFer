import pandas as pd
import os


startdir = r'C:\Users\pihltd\Documents\VMShare\KF\SRFs'


def dataTyper(df):
    datatypes = []
    headers = ['Clinical', 'Genomics','Imaging', 'Proteomics']
    for header in headers:
        if df[header].unique().tolist()[0] == 'Yes':
            datatypes.append(header)
    
    return ','.join(datatypes)

final = []
for (root, dirs, files) in os.walk(startdir):
    for file in files:
        if 'xlsx' in file:
            ps_df = pd.read_excel(f"{startdir}\{file}", 'Program and Study')
            dad_df = pd.read_excel(f"{startdir}\{file}", 'Data Access and Disease')
            dt_df = pd.read_excel(f"{startdir}\{file}", 'Data Types')
            
            program = ps_df['Program'].unique().tolist()[0]
            program_acronym = ps_df['Program Abbreviation'].unique().tolist()[0]
            study = ps_df['Study Title'].unique().tolist()[0]
            study_acronym = ps_df['Study Abbreviation'].unique().tolist()[0]
            phs = dad_df['If yes, provide dbGaP PHS number with the version number'].unique().tolist()[0]
            gpa = dad_df['GPA Name'].unique().tolist()[0]
            datatypes = dataTyper(dt_df)
            
            final.append({
                'Program Name': program,
                'Program Acronym': program_acronym,
                'Study Name as in dbGaP': study,
                'Study Acronym as in dbGaP': study_acronym,
                'dbGaP id': phs,
                'GPA': gpa,
                'Component': 'GC',
                'SRF Yes/No': 'Yes',
                'Notes': datatypes
                
            })
            
            
            #for index, row in srf_df.iterrows():
            #    final.append({'program':row['Program'], 'program_acronym': row['Program Abbreviation'], 'study':row['Study Title'], 'study_acronym':row['Study Abbreviation']})


printfile = f"{startdir}\consolidated_prog_study.tsv"

final_df = pd.DataFrame(final)
final_df.to_csv(printfile, sep="\t", index=False)