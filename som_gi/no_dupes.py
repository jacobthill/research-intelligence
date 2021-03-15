import pandas
no_dupes_per_researcher = pandas.read_csv("output/som_gi_report.csv")
no_dupes_per_researcher.drop_duplicates(subset=["display_name","dimensions_id"], keep='first', inplace=True)
no_dupes_per_researcher.to_csv('output/som_gi_report_no_dupes_per_researcher.csv', index=False)

no_dupes = pandas.read_csv("output/som_gi_report.csv")
no_dupes.drop_duplicates(subset="dimensions_id", keep='first', inplace=True)
no_dupes.to_csv('output/som_gi_report_no_dupes.csv', index=False)
