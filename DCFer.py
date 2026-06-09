import pandas as pd
import requests
from cdapython import get_file_data
from urllib.parse import unquote
import sys

def sstrQuery(phsnumber):
    url = f"https://www.ncbi.nlm.nih.gov/gap/sstr/api/v1/study/{phsnumber}.v1/summary"
    headers = {'accept': 'application/json'}
    
    try:
        sstrinfo = requests.get(url=url, headers=headers)
        if sstrinfo.status_code == 200:
            sstrjson = sstrinfo.json()
            return sstrjson['study']['name']
        else:
            return None
    except requests.exceptions.HTTPError as e:
        return ("HTTP Error: {e}")


def ipTable(ip_df, source_df, reportfile):
    for x in range(10):
        searchip = ip_df.iloc[x]['src_ip']
        search_df = source_df.query('src_ip == @searchip')
        locations = search_df['src_ip_geolocation'].unique().tolist()
        users = search_df['user_name'].unique().tolist()
        reportfile.write(f"{searchip}\t{",".join(locations)}\t{",".join(users)}\t{ip_df.iloc[x]['count']}\n")
    
def geoTable(item_df, source_df, reportfile):
    for x in range(10):
        searchterm = item_df.iloc[x]['src_ip_geolocation']
        search_df = source_df.query('src_ip_geolocation == @searchterm')
        users = search_df['user_name'].unique().tolist()
        ips = search_df['src_ip'].unique().tolist()
        reportfile.write(f"{searchterm}\t{",".join(users)}\t{",".join(ips)}\t{item_df.iloc[x]['count']}\n")

def userTable(item_df, source_df, reportfile):
    for x in range(10):
        searchterm = item_df.iloc[x]['user_name']
        search_df = source_df.query('user_name == @searchterm')
        locaations = search_df['src_ip_geolocation'].unique().tolist()
        ips = search_df['src_ip'].unique().tolist()
        reportfile.write(f"{searchterm}\t{",".join(ips)}\t{",".join(locaations)}\t{item_df.iloc[x]['count']}\n")

        
def studyTable(item_df, source_df, reportfile):
    for x in range(10):
        searchterm = item_df.iloc[x]['associated_study']
        search_df = source_df.query('associated_study== @searchterm')
        studyname = sstrQuery(phsnumber=searchterm)
        ips = search_df['src_ip'].unique().tolist()
        reportfile.write(f"{searchterm}\t{studyname}\t{",".join(ips)}\t{item_df.iloc[x]['count']}\n")


def drsTable(item_df, source_df, reportfile):
    for x in range(10):
        drsid = item_df.iloc[x]['guid']
        drsid = unquote(drsid)
        answer_df = get_file_data(drsid)
        #print(answer_df)
        if answer_df.empty:
            reportfile.write(f"{drsid}\tNone\tNone\tNone\n")
        else:
            if len(answer_df) == 1:
                anatomic = answer_df.iloc[0]['anatomic_site']
                formatlist = answer_df['format'].unique().tolist()
                sources = answer_df.iloc[0]['data_source']
            else:
                anatomic = "Way"
                formatlist = ['To', 'Big', 'A']
                sources = "Dataframe"
            reportfile.write(f"{drsid}\t{anatomic}\t{",".join(formatlist)}\t{sources}\n")


def writeBinFile(df, reportfile):
    #df = df.reindex(sorted(df.columns), axis=1)
    df = df.sort_values(by='bin', ascending=True)
    for index, row in df.iterrows():
        reportfile.write(f"{row['bin']}\t{row['count']}\n")
        

#
#  main
#
csvfile = r'C:\Users\pihltd\Documents\DCFUsage\async_waf_audit_revproxy_matched_logs_merged_standard_format_with_geo_with_dc (1) 1.csv'
reportfile = r'C:\Users\pihltd\Documents\DCFUsage\dcf_report.tsv'
binreportfile = r'C:\Users\pihltd\Documents\DCFUsage\dcf_bin_report.tsv'

dcf_df = pd.read_csv(csvfile, sep=",")


#
#    Top 10 lists
#


ip_df = dcf_df.value_counts('src_ip').reset_index().rename(columns={'index':'value', 0:'count'})
user_df = dcf_df.value_counts('user_name').reset_index().rename(columns={'index':'value', 0:'count'})
geo_df = dcf_df.value_counts('src_ip_geolocation').reset_index().rename(columns={'index':'value', 0:'count'})
study_df =dcf_df.value_counts('associated_study').reset_index().rename(columns={'index':'value', 0:'count'})
drs_df = dcf_df.value_counts('guid').reset_index().rename(columns={'index':'value', 0:'count'})

bins = [1,10,100,1000,10000,100000]
labels = ['0-10', '11-100', '101-1000', '1001-10000', '100001+']
ip_df['bin'] = pd.cut(ip_df['count'], bins=bins, labels=labels)
user_df['bin'] = pd.cut(user_df['count'], bins=bins, labels=labels)
geo_df['bin'] = pd.cut(geo_df['count'], bins=bins, labels=labels)
study_df['bin'] = pd.cut(study_df['count'], bins=bins, labels=labels)
drs_df['bin'] = pd.cut(drs_df['count'], bins=bins, labels=labels)

with open(binreportfile, "w") as br:
    br.write("Bins based on IP address\n")
    bin_ip_df = ip_df.value_counts('bin').reset_index().rename(columns={'index':'value', 0:'count'})
    writeBinFile(bin_ip_df, br)
    br.write("\n")
    br.write("Bin by User\n")
    bin_user_df = user_df.value_counts('bin').reset_index().rename(columns={'index':'value', 0:'count'})
    writeBinFile(bin_user_df, br)
    br.write("\n")
    br.write("Bin by Geolocation\n")
    bin_geo_df = geo_df.value_counts('bin').reset_index().rename(columns={'index':'value', 0:'count'})
    writeBinFile(bin_geo_df, br)
    br.write("\n")
    br.write("Bin by Study\n")
    bin_study_df = study_df.value_counts('bin').reset_index().rename(columns={'index':'value', 0:'count'})
    writeBinFile(bin_study_df, br)
    br.write("\n")
    br.write("Bin by DRS Id\n")
    bin_drs_df = drs_df.value_counts('bin').reset_index().rename(columns={'index':'value', 0:'count'})
    writeBinFile(bin_drs_df, br)

#print(ip_df['bin'].value_counts())




sys.exit(0)    


dflist = [ip_df, user_df, geo_df, study_df]


with open(reportfile,"w") as r:
    # IP
    print("IP Address report")
    r.write("IP Address\tGeolocation\tUser\tCount\n")
    ipTable(ip_df=ip_df, source_df=dcf_df, reportfile=r)
    r.write("\n")
    print("Geolocation report")
    r.write("Geolocation\tUser\tIP Address\tCount\n")
    geoTable(item_df=geo_df, source_df=dcf_df, reportfile=r)
    r.write("\n")
    print("User report")
    r.write("User\tIP Address\tGeolocation\tCount\n")
    userTable(item_df=user_df, source_df=dcf_df, reportfile=r)
    r.write("\n")
    print("Study report")
    r.write("Study ID\tStudy Name\tIP Addresses\tCount\n")
    studyTable(item_df=study_df, source_df=dcf_df, reportfile=r)
    r.write("\n")
    print("File report")
    r.write('DRS ID\tAnatomic Site\tFile Format\tData Source\n')
    drsTable(item_df=drs_df, source_df=dcf_df, reportfile=r)
