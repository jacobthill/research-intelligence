import dimcli, itertools, json, requests, sys, woslite_client
import pandas as pd
from datetime import datetime
from dimcli.utils import *
from requests.auth import AuthBase
# Need to add to the path to import config
sys.path.insert(1, '../')
import config

queries = ["islamic", "kidney", "pandemic", "lungs", "cancer", "robitics", "artificial intelligence",
           "poetry", "blockchain", "amortisation", "antitrust", "schizophrenia", "psycology", "sociology"]

full_text_query = """search publications in full_data for "\\"{}\\"" return publications [title + researchers + id + doi + publisher + journal + volume + issue + pages + year + concepts + abstract + acknowledgements + funders + research_org_cities + research_org_names + research_org_state_names + research_orgs] limit 1000"""

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

dimensions = pd.DataFrame(columns=["title", "authors", "id", "doi", "publisher", "journal", "volume", "issue", "pages", "pub_year", "concepts", "abstract", "acknowledgements", "funders", "research_org_cities", "research_org_names", "research_org_state_names", "research_orgs", "provenance", "pub_harvested_date"])

for i in queries:

    # Get publications by search term
    query = dsl.query(full_text_query.format(i))
    for pub in query['publications']:
        researcher_ids = get_authors(query)
        new_row = [pub['title'], '; '.join(researcher_ids), pub['id'], pub.get('doi'), pub.get('publisher'), pub.get('journal'), pub.get('volume'), pub.get('issue'), pub.get('pages'), pub.get('year'), pub.get('concepts'), pub.get('abstract'), pub.get('acknowledgements'), pub.get('funders'), pub.get('research_org_cities'), pub.get('research_org_names'), pub.get('research_org_state_names'), pub.get('research_orgs'), 'dimensions', datetime.now().strftime("%d/%m/%Y %H:%M:%S")]
        new_row_series = pd.Series(new_row, index = dimensions.columns)
        dimensions = dimensions.append(new_row_series, ignore_index=True)

dimensions.to_csv('output/non_relevant.csv', index=False)
