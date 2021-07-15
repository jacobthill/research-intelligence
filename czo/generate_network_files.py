import math
import numpy as np
import pandas as pd
from itertools import combinations

# Load the data harvested from DOIs
from_dois = pd.read_csv('output/output_from_dois.csv', delimiter=',')

connections = []
researchers = []
publications = []

for count, (index, row) in enumerate(from_dois.iterrows()):
    ids = [x for x in str(row['authors']).split('; ')]
    publications.append(tuple((row['id'], row['doi'])))
    for r in ids:
        if str(r):
            researchers.append(r)

for r in np.unique(researchers)[:188]:
    matches = from_dois[from_dois['authors'].str.contains(r, na=False)]
    connections.extend(list(combinations(matches['id'].to_list(), 2)))

with open('output/pubs_author_graph.net', 'w') as out:
    out.write('*arcs\n')
    for c in connections:
        out.write('{} {}\n'.format(c[0], c[1]))

with open('output/pubs_with_id.net', 'w') as out:
    out.write('*Vertices {}\n'.format(len(publications)))
    for count, p in enumerate(publications, start=1):
        out.write('{} \"{}\"\n'.format(count, p[1]))
