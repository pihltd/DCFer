import pandas as pd
from pathlib import Path


mapped_file = r'C:\Users\pihltd\Documents\DCFUsage\CDA_mapped_files.tsv'
unmapped_file = r'C:\Users\pihltd\Documents\DCFUsage\CDA_unmapped_drsIDs.tsv'
report_file = r'C:\Users\pihltd\Documents\DCFUsage\CDA_Report.tsv'

mapped_df = pd.read_csv(mapped_file, sep="\t")
#remove duplicate lines
mapped_df.drop_duplicates(inplace=True)

unmapped_list = Path(unmapped_file).read_text().splitlines()
#remove duplicates
unmapped_list = list(set(unmapped_list))

mapped_count = len(mapped_df['file_id'].unique().tolist())
unmapped_count = len(unmapped_list)


print(f"Mapped file IDs: {mapped_count}\nUnmapped file IDs: {unmapped_count}\nTotal file IDs{unmapped_count+mapped_count}\n")

#category
cat_df = mapped_df['category'].value_counts().to_frame()

#file_type
file_df = mapped_df['file_type'].value_counts().to_frame()

#format
format_df = mapped_df['format'].value_counts().to_frame()

#tumor_vs_normal
tn_df = mapped_df['tumor_vs_normal'].value_counts().to_frame()

#data_source
ds_df = mapped_df['data_source'].value_counts().to_frame()

final_df = pd.concat([cat_df, file_df, format_df, tn_df, ds_df])

print("\n\n")
print(final_df)
final_df.to_csv(report_file, sep="\t")