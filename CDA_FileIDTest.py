from cdapython import   get_file_data
from urllib.parse import unquote
import pandas as pd


#csvfile = r'C:\Users\pihltd\Documents\DCFUsage\async_waf_audit_revproxy_matched_logs_merged_standard_format_with_geo_with_dc (1) 1.csv'
#reportfile = r'C:\Users\pihltd\Documents\DCFUsage\dcf_file_report.tsv'

#dcf_df = pd.read_csv(csvfile, sep=",")
#drslist = dcf_df['guid'].unique().tolist()
#print(f"DRS List lenght: {len(drslist)}")

#drs_df = dcf_df.value_counts('guid').reset_index().rename(columns={'index':'value', 0:'count'})
#print(drs_df)
drs = "c2887085-0219-4bf9-8735-c35a0fd47fd3"
#drs = "768c0d33-e543-4444-9e10-ab400ca25aa1"
#drs = "dg.4DFC%2F9ade52a2-6ca4-5184-a4b8-71d396abc855"
#drs = unquote(drs)

drssearch = get_file_data(drs)


print(drssearch)