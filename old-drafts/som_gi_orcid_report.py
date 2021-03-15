import csv, dimcli, json, os, pandas
from datetime import datetime
from dimcli.utils import *

username = "jtimAPI@stanford.edu"  #@param {type: "string"}
password = "IJ5kTsssv144XrKU"  #@param {type: "string"}
endpoint = "https://app.dimensions.ai"

# connect to the database
dimcli.login(username, password, endpoint)
dsl = dimcli.Dsl()

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

df = pandas.read_csv('input/single_name_test.csv', header=0)

with open('output/som_gi_dimensions_orcid_report_dupes.csv', mode='w') as out:
    out = csv.writer(out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    out.writerow(["title", "author_list", "pmid", "dimensions_id", "doi", "doi_url", "publisher", "journal", "volume", "issue", "pages", "mesh", "pub_year", "provenance", "pub_harvested_date"])

    for index, r in df.iterrows():
        # Query the first name value and the first institution value
        # query = dsl.query("""search publications where researchers.orcid_id = "\\"{}\\""
        #                     return publications [all] limit 1000""".format(r["ORCID iD"]))

        query = dsl.query("""search publications where researchers.orcid_id = "0000-0002-1838-9363" return publications""")

        for pub in query['publications']:
            print(pub)
            authors, journal_title = get_fields_from_query(query)
            out.writerow([pub['title'], '; '.join(authors), pub.get('pmid'), pub['id'], pub.get('doi'), "https://doi.org/{}".format(pub.get('doi')), pub.get('publisher'), journal_title, pub.get('volume'), pub.get('issue'), pub.get('pages'), pub.get('mesh_terms'), pub.get('year'), 'dimensions', datetime.now().strftime("%d/%m/%Y %H:%M:%S")])


out = pandas.read_csv("output/som_gi_dimensions_orcid_report_dupes.csv")
out.drop_duplicates(subset ="dimensions_id",
                     keep = False, inplace = True)
out.to_csv('output/som_gi_dimensions_orcid_report.csv', index=False)
os.remove('output/som_gi_dimensions_orcid_report_dupes.csv')
