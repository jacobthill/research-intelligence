import dimcli, itertools, json, requests, sys, woslite_client
import pandas as pd
from datetime import datetime
from dimcli.utils import *
from requests.auth import AuthBase
# Need to add to the path to import config
sys.path.insert(1, '../')
import config

queries = ["Xevo TQ-XS mass spectrometer system",
           "LTQ-Orbitrap mass spectrometer system",
           "Stanford Cancer Institute Proteomics/Mass Spectrometry Shared Resource"]

facility_names = ["Vincent Coates Foundation Mass Spectrometry Laboratory, Stanford University Mass Spectrometry",
                  "Vincent Coates Foundation Mass Spectrometry Laboratory",
                  "Vincent Coates Foundation Mass Spec"]

# rrids cause network timeout on wos
rrids = ["SCR_017801", "SCR_018694", "SCR_018510"]

grants = ["P30 CA124435", "P30CA124435", "S10 OD026962", "S10OD026962", "S10 RR027425", "S10RR027425"]

full_text_query = """search publications in full_data for "\\"{}\\"" return publications [all] limit 1000"""

# helper functions
def get_fields_from_query(query):
    authors = []
    author_affiliations = pub.get('author_affiliations')
    if author_affiliations:
        for i in author_affiliations:
            for j in i:
                authors.append("{}, {}".format( j['last_name'], j['first_name']))
    journal = pub.get('journal')
    if journal != None:
        journal_title = journal.get('title')
        return authors, journal_title
    else:
        return authors, ""

# Get Dimesnions publications
# connect to the database
dimcli.login(config.username, config.password, config.endpoint)
dsl = dimcli.Dsl()

dimensions = pd.DataFrame(columns=["title", "author_list", "pmid", "dimensions_id", "doi", "doi_url", "publisher", "journal", "volume", "issue", "pages", "mesh", "pub_year", "provenance", "pub_harvested_date"])

for i in list(itertools.chain(queries, facility_names, rrids, grants)):

    # Get publications by search term
    query = dsl.query(full_text_query.format(i))
    for pub in query['publications']:
        authors, journal_title = get_fields_from_query(query)
        new_row = [pub['title'], '; '.join(authors), pub.get('pmid'), pub['id'], pub.get('doi'), "https://doi.org/{}".format(pub.get('doi')), pub.get('publisher'), journal_title, pub.get('volume'), pub.get('issue'), pub.get('pages'), pub.get('mesh_terms'), pub.get('year'), 'dimensions', datetime.now().strftime("%d/%m/%Y %H:%M:%S")]
        new_row_series = pd.Series(new_row, index = dimensions.columns)
        dimensions = dimensions.append(new_row_series, ignore_index=True)

dimensions.to_csv('output/dimensions.csv', index=False)

# Get Web of Science publications
wos = pd.DataFrame(columns=["title", "author_list", "pmid", "wos_id", "doi", "doi_url", "publisher", "journal", "volume", "issue", "pages", "pub_year", "provenance", "pub_harvested_date"])

for i in list(itertools.chain(rrids, grants, queries, facility_names)):
    next = 1
    status_code = 200
    print('Searching for: {}'.format(i))
    while status_code == 200:
        response = requests.get('https://wos-api.clarivate.com/api/wos/?databaseId=WOS&usrQuery=ALL={}&count=100&firstRecord={}'.format(i, next),
                           headers={'X-ApiKey': '90abec316661b5de6f1447c067ef0485a4fcc6cf'})
        try:
            records_found = response.json().get('QueryResult').get('RecordsFound')
        except:
            try:
                records_found = response.json().get('Data').get('QueryResult').get('RecordsFound')
            except:
                records_found = 0
        if records_found > 0:
            for count, i in enumerate(response.json()['Data']['Records']['records']['REC'], start=1):
                # with open('output/wos_json/{}.json'.format(count), 'w') as out:
                #     json.dump(i, out, ensure_ascii=False)
                authors = []
                for author in i['static_data']['summary']['names']['name']:
                    if type(author) == dict:
                        if author.get('role') == 'author':
                            authors.append(author.get('display_name'))
                for t in i['static_data']['summary']['titles']['title']:
                    if t['type'] == 'source':
                        journal_title = t['content']
                    if t['type'] == 'item':
                        title = t['content']
                doc_type = i['static_data']['summary']['doctypes']['doctype']
                for id in i['dynamic_data']['cluster_related']['identifiers']['identifier']:
                    if type(id) == dict:
                        if id['type'] == 'doi':
                            doi = id['value']
                        if id['type'] == 'pmid':
                            pmid = id['value']
                issue = i['static_data']['summary']['pub_info'].get('issue')
                pages = i['static_data']['summary']['pub_info']['page'].get('content')
                publisher = i['static_data']['summary']['publishers']['publisher']['names']['name'].get('unified_name')
                pub_year = i['static_data']['summary']['pub_info']['pubyear']
                volume = i['static_data']['summary']['pub_info'].get('vol')
                wos_id = i['UID']

                new_row = [title, '; '.join(authors), pmid, wos_id, doi, "https://doi.org/{}".format(doi), publisher, journal_title, volume, issue, pages, pub_year, 'wos', datetime.now().strftime("%d/%m/%Y %H:%M:%S")]
                new_row_series = pd.Series(new_row, index = wos.columns)
                wos = wos.append(new_row_series, ignore_index=True)
                next+=100
                next_response = requests.get('https://wos-api.clarivate.com/api/wos/?databaseId=WOS&usrQuery=ALL={}&count=100&firstRecord={}'.format(i, next),
                                   headers={'X-ApiKey': '90abec316661b5de6f1447c067ef0485a4fcc6cf'})
                status_code = next_response.status_code
            print('Records found: {}'.format(response.json()['QueryResult']['RecordsFound']))
        else:
            status_code = 'Not returned'
            pass

wos.to_csv('output/wos.csv', index=False)
