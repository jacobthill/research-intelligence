import dimcli, itertools, json, requests, sys
import pandas as pd
from datetime import datetime
from dimcli.utils import *
from requests.auth import AuthBase
# Need to add to the path to import config
sys.path.insert(1, '../')
import config

input = pd.read_csv('award_number_input.csv', header=0)

awards = []
awards_dict = {}

for index, row in input.iterrows():
    awards_dict[row['AwardNumber']] = row['StartDate']

site_names = ['Boulder Creek', 'Calhoun', 'Santa Catalina Mountains', 'Jemez River Basin', 'Christina River Basin', 'Eel River', 'Intensively Managed Landscapes', 'Luquillo', 'Reynolds Creek', 'Susquehanna Shale Hills', 'Southern Sierra']

full_text_query = """search publications in full_data for "\\"{}\\"" return publications [title + researchers + id + doi + publisher + journal + volume + issue + pages + year + concepts] limit 1000"""

# full_text_query = """search publications in full_data for "\\"{}\\"" return publications [all] limit 1000"""

# get specific fields from query
def get_authors(query):
    researcher_ids = []
    author_affiliations = pub.get('authors')
    if author_affiliations:
        for i in author_affiliations:
            researcher_ids.append(i.get('researcher_id'))

    return researcher_ids

# Get Dimesnions publications
# connect to the database
dimcli.login(config.username, config.password, config.endpoint)
dsl = dimcli.Dsl()

dimensions = pd.DataFrame(columns=["title", "author_list", "dimensions_id", "doi", "doi_url", "publisher", "journal", "volume", "issue", "pages", "pub_year", "concepts", "provenance", "query_term", "pub_harvested_date"])

# for k,v in awards_dict.items():
#     awards.append(str(k))

for count, i in enumerate(list(itertools.chain(awards, site_names)),start=1):

    # Get publications by search term
    query = dsl.query(full_text_query.format(i))
    for pub in query['publications']:
        try:
            researcher_ids = get_authors(query)
            new_row = [pub['title'], '; '.join(researcher_ids), pub['id'], pub.get('doi'), "https://doi.org/{}".format(pub.get('doi')), pub.get('publisher'), pub.get('journal'), pub.get('volume'), pub.get('issue'), pub.get('pages'), pub.get('year'), pub.get('concepts'), 'dimensions', i, datetime.now().strftime("%d/%m/%Y %H:%M:%S")]
            new_row_series = pd.Series(new_row, index = dimensions.columns)
            dimensions = dimensions.append(new_row_series, ignore_index=True)
        except:
            pass

    print('Finished term {} of {}: {}.'.format(count, len(list(itertools.chain(awards, site_names))), i))
    print('\n')

dimensions.to_csv('output/output_from_award_numbers.csv', index=False)
