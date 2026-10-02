from cdapython import *
import sys


#print(tables())
#print(columns(column=["*project*"]))
#sys.exit(0)
#dflist = summarize_subjects(add_columns="project_name", return_data_as='dataframe_list')

#projectlist = column_values(column='project_id', return_data_as='list')
#print(projectlist)

#print(cda_functions())
#for proj in projectlist:
#    print(proj)

df = get_subject_data( "*", add_columns=['project_id', 'project_short_name'], collate_results=True)
#df = summarize_subjects(add_columns=['project_id', 'project_short_name'])
print(df)

sys.exit(0)

counter = 0
while counter <= 2:
    summary = summarize_subjects(projectlist[counter], return_data_as='dataframe_list')
    print(f"Summary for {projectlist[counter]}")
    print(summary)
    counter = counter +1

#for df in dflist:
#    print(df.columns)
