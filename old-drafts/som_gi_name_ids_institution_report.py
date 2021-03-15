import csv, dimcli, json, os, pandas
from datetime import datetime
from dimcli.utils import *

username = "jtimAPI@stanford.edu"  #@param {type: "string"}
password = "IJ5kTsssv144XrKU"  #@param {type: "string"}
endpoint = "https://app.dimensions.ai"

# connect to the database
dimcli.login(username, password, endpoint)
dsl = dimcli.Dsl()

# get organization ids for organizations associated with Stanford University
# returns a json object
def get_grids_by_name(name):
    grids = []
    name_query = dsl.query("""search organizations where name~"\\"{}\\"" return organizations[id]""".format(name)).data
    for org in name_query['organizations']:
        grids.append(org.get('id'))
    return json.dumps(grids)

def researcher_ids_by_name(last_name):
    ids = []
    name_query = dsl.query("""search researchers where last_name~"\\"{}\\"" return authors[id]""").data
    for id in name_query['authors']:
        ids.append(id.get('id'))
    return json.dumps(ids)

print(researcher_ids_by_name('Triadafilopoulos'))

def som_gi_query(researcher_names, researcher_institutions):
    return """search publications
                        in authors for "\\"{}\\""
                        where research_orgs.id in {}
                        return publications [all] limit 1000""".format(researcher_names, researcher_institutions)

def get_fields_from_query(query):
    authors = []
    author_affiliations = pub['author_affiliations']
    for i in author_affiliations:
        for j in i:
            authors.append("{}, {}".format( j['last_name'], j['first_name']))
    journal = pub.get('journal')
    if journal != None:
        journal_title = journal.get('title')
        return authors, journal_title
    else:
        return authors, ""

# df = pandas.read_csv('input/single_name_test.csv', header=0)
#
# with open('output/som_gi_dimensions_name_institution_report_dupes.csv', mode='w') as out:
#     out = csv.writer(out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#     out.writerow(["title", "author_list", "pmid", "dimensions_id", "doi", "doi_url", "publisher", "journal", "volume", "issue", "pages", "mesh", "pub_year", "provenance", "pub_harvested_date"])
#
#     for index, r in df.iterrows():
#         # Query the first name value and the first institution value
#         query = dsl.query(som_gi_query(r["Faculty/Fellow"].split(';')[0], get_grids_by_name(r["Institutions"].split(';')[0])))
#         for pub in query['publications']:
#             print(pub)
#             authors, journal_title = get_fields_from_query(query)
#             out.writerow([pub['title'], '; '.join(authors), pub.get('pmid'), pub['id'], pub.get('doi'), "https://doi.org/{}".format(pub.get('doi')), pub.get('publisher'), journal_title, pub.get('volume'), pub.get('issue'), pub.get('pages'), pub.get('mesh_terms'), pub.get('year'), 'dimensions', datetime.now().strftime("%d/%m/%Y %H:%M:%S")])
#
#         # Query the second name value and the first institution value
#         if len(r["Faculty/Fellow"].split(';')) > 1:
#             query = dsl.query(som_gi_query(r["Faculty/Fellow"].split(';')[1], get_grids_by_name(r["Institutions"].split(';')[0])))
#             for pub in query['publications']:
#                 authors, journal_title = get_fields_from_query(query)
#                 out.writerow([pub['title'], '; '.join(authors), pub.get('pmid'), pub['id'], pub.get('doi'), "https://doi.org/{}".format(pub.get('doi')), pub.get('publisher'), journal_title, pub.get('volume'), pub.get('issue'), pub.get('pages'), pub.get('mesh_terms'), pub.get('year'), 'dimensions', datetime.now().strftime("%d/%m/%Y %H:%M:%S")])
#
#         # Query the first name value and the second institution value
#         if len(r["Institutions"].split(';')) > 1:
#             query = dsl.query(som_gi_query(r["Faculty/Fellow"].split(';')[0], get_grids_by_name(r["Institutions"].split(';')[1])))
#             for pub in query['publications']:
#                 authors, journal_title = get_fields_from_query(query)
#                 out.writerow([pub['title'], '; '.join(authors), pub.get('pmid'), pub['id'], pub.get('doi'), "https://doi.org/{}".format(pub.get('doi')), pub.get('publisher'), journal_title, pub.get('volume'), pub.get('issue'), pub.get('pages'), pub.get('mesh_terms'), pub.get('year'), 'dimensions', datetime.now().strftime("%d/%m/%Y %H:%M:%S")])
#
#         # Query the second name value and the second institution value
#         if len(r["Faculty/Fellow"].split(';')) > 1 and len(r["Institutions"].split(';')) > 1:
#             query = dsl.query(som_gi_query(r["Faculty/Fellow"].split(';')[1], get_grids_by_name(r["Institutions"].split(';')[1])))
#             for pub in query['publications']:
#                 authors, journal_title = get_fields_from_query(query)
                # out.writerow([pub['title'], '; '.join(authors), pub.get('pmid'), pub['id'], pub.get('doi'), "https://doi.org/{}".format(pub.get('doi')), pub.get('publisher'), journal_title, pub.get('volume'), pub.get('issue'), pub.get('pages'), pub.get('mesh_terms'), pub.get('year'), 'dimensions', datetime.now().strftime("%d/%m/%Y %H:%M:%S")])


# To do
# - Can we get researcher id by name search, similar to the way we get grid ids?
# -- Why does George Triadafilopoulos have 541(468) publications but much fewer returned?
# - Can we search by ORCID?
# - Report by author.

# out = pandas.read_csv("output/som_gi_dimensions_name_institution_report_dupes.csv")
# out.drop_duplicates(subset ="dimensions_id",
#                      keep = False, inplace = True)
# out.to_csv('output/som_gi_name_institution_dimensions_report.csv', index=False)
# os.remove('output/som_gi_dimensions_name_institution_report_dupes.csv')
