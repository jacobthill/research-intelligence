import pandas as pd

dimensions_in = pd.read_csv("../output/dimensions_report_som_gi.csv")

profiles_in = pd.read_csv("../output/profiles_results_with_status_3-17-2021.csv")

def get_status(row):
    # if row['publication_status'] == 'approved':
    #     return 'yes'
    if row['approved_in_profiles?'] is True:
        return 'yes'

# def is_approved(row):
#     if row['']df1.where(df1.values==df2.values).notna()


# profiles_in['is_true_positive?'] = profiles_in.apply (lambda row: get_status(row), axis=1)

# profiles_in.to_csv('../output/profiles_results_with_status_ammended_3-17-2021.csv', index=False)

dimensions_in['approved_in_profiles?'] = dimensions_in.doi.isin(profiles_in.doi)
dimensions_in['is_true_positive?'] = dimensions_in.apply (lambda row: get_status(row), axis=1)
dimensions_in.to_csv('../output/dimensions_report_som_gi_a.csv')
