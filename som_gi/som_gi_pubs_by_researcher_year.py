import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

raw = pd.read_csv("input/som_gi_input_raw.csv")
ammended = pd.read_csv("input/som_gi_input_ammended.csv")
input = pd.read_csv("output/som_gi_report_clean.csv")

grouper = input.groupby(["display_name", "pub_year"])['display_name'].count()

data = grouper.to_frame(name = 'number_of_publicatons').reset_index()

data = data.sort_values(["display_name", "pub_year"], ascending = True)

data.to_csv('output/pubs_by_researcher_year.csv', index=False)

print(ammended['Display Name'].unique().size)
print(data['display_name'].unique().size)
print(np.setdiff1d(ammended['Display Name'].unique(), data['display_name'].unique()))
# for i in data['display_name'].unique():
#     years = []
#     pubs = []
#     for index, r in data.iterrows():
#         if i == r['display_name']:
#             years.append(r['pub_year'])
#             pubs.append(int(r['number_of_publicatons']))
#     fig = plt.figure()
#     plt.bar(years,pubs)
#     fig.suptitle("{}\nTotal = {}".format(i, sum(pubs)), fontsize=18)
#     plt.xlabel('Years', fontsize=14)
#     plt.ylabel('Publications', fontsize=14)
#     plt.savefig('figures/{}.png'.format(i.lower().replace(' ', '-')))



# g = data.groupby(['display_name', 'pub_year', 'number_of_publicatons'])
# plt.bar(g['pub_year'],g['number_of_publicatons'])
# plt.show()

# for k,v in pubs_per_year.items():
#     print("{}:".format(k))
#     for l,w in v.items():
#         print("\t{}: {}".format(l, w))
