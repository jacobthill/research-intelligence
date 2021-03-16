import csv, dimcli, json, os, pandas, sys
import numpy as np
from datetime import datetime
from dimcli.utils import *
# Need to add to the path to import config
sys.path.insert(1, '../')
import config

# username = "jtimAPI@stanford.edu"  #@param {type: "string"}
# password = "IJ5kTsssv144XrKU"  #@param {type: "string"}
# endpoint = "https://app.dimensions.ai"

# connect to the database
dimcli.login(config.username, config.password, config.endpoint)
dsl = dimcli.Dsl()

# Query for publications based on researcher id and GRID
id_institution_query = """search publications
                          where researchers.id in {}
                          and research_orgs.id in {}
                          return publications limit 1000"""

# Query for publications based on researcher id only
id_query = """search publications
              where researchers.id in {}
              return publications [all] limit 1000"""

# Query for publications based on name string and GRID
name_institution_query = """search publications in authors for "\\"{}\\""
                            where research_orgs.id in {}
                            return publications [all] limit 1000"""

# Query for publications based on ORCID
orcid_query = """search publications
                 where researchers.orcid_id = "{}"
                 return publications [all] limit 1000"""

# Query for researcher ids from name string
researcher_ids_from_name_query = """search researchers for "\\"{}\\""
                                    where obsolete = 0
                                    return researchers[id]"""

# get organization ids for organizations associated with Stanford University
def get_grids_by_name(institution_name):
    grids = []
    name_institution_query  = dsl.query("""search organizations where name~"\\"{}\\"" return organizations[id]""".format(institution_name)).data
    for org in name_institution_query ['organizations']:
        grids.append(org.get('id'))
    return json.dumps(grids)

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

df = pandas.read_csv('input/som_gi_input_ammended.csv', header=0)

with open('output/dimensions_report_smci.csv', mode='w') as out:
    out = csv.writer(out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    out.writerow(["display_name", "search_strategy", "researcher_id", "faculty/fellow", "searched_name", "searched_institution", "title", "author_list", "pmid", "dimensions_id", "doi", "doi_url", "publisher", "journal", "volume", "issue", "pages", "mesh", "pub_year", "provenance", "pub_harvested_date"])

    for index, r in df.iterrows():
        researcher_ids = []
        names = r["Faculty/Fellow"].split(';')
        institutions = r["Institutions"].split(';')
        for n in names:
            # Query for ids by researcher name
            id_data = dsl.query(researcher_ids_from_name_query.format(n.strip())).data
            id_list = id_data.get('researchers')
            for i in id_list:
                researcher_ids.append(i['id'])

        # Get publications by ORCID
        query = dsl.query(orcid_query.format(r['ORCID iD']))
        for pub in query['publications']:
            authors, journal_title = get_fields_from_query(query)
            out.writerow([r["Display Name"], 'ORCID', '', r["Faculty/Fellow"], '', '', pub['title'], '; '.join(authors), pub.get('pmid'), pub['id'], pub.get('doi'), "https://doi.org/{}".format(pub.get('doi')), pub.get('publisher'), journal_title, pub.get('volume'), pub.get('issue'), pub.get('pages'), pub.get('mesh_terms'), pub.get('year'), 'dimensions', datetime.now().strftime("%d/%m/%Y %H:%M:%S")])

        # Get publications by researcher id and institution
        for id in researcher_ids:
            for institution in institutions:
                query = dsl.query(id_institution_query .format(json.dumps(researcher_ids), get_grids_by_name(institution)))
                for pub in query['publications']:
                    authors, journal_title = get_fields_from_query(query)
                    out.writerow([r["Display Name"], 'Reasearcher id & GRID', id, r["Faculty/Fellow"], n.strip(), institution, pub['title'], '; '.join(authors), pub.get('pmid'), pub['id'], pub.get('doi'), "https://doi.org/{}".format(pub.get('doi')), pub.get('publisher'), journal_title, pub.get('volume'), pub.get('issue'), pub.get('pages'), pub.get('mesh_terms'), pub.get('year'), 'dimensions', datetime.now().strftime("%d/%m/%Y %H:%M:%S")])

            # Query for ids without institution
            query = dsl.query(id_query .format(json.dumps(researcher_ids)))
            for pub in query['publications']:
                authors, journal_title = get_fields_from_query(query)
                out.writerow([r["Display Name"], 'Researcher id', id, r["Faculty/Fellow"], n.strip(), 'No institution recorded', pub['title'], '; '.join(authors), pub.get('pmid'), pub['id'], pub.get('doi'), "https://doi.org/{}".format(pub.get('doi')), pub.get('publisher'), journal_title, pub.get('volume'), pub.get('issue'), pub.get('pages'), pub.get('mesh_terms'), pub.get('year'), 'dimensions', datetime.now().strftime("%d/%m/%Y %H:%M:%S")])

        # Get publications by name and instituition
        combinations = [(n,i) for n in names for i in institutions]
        for c in combinations:
            query = dsl.query(name_institution_query.format(c[0].strip(), get_grids_by_name(c[1].strip())))
            for pub in query['publications']:
                authors, journal_title = get_fields_from_query(query)
                out.writerow([r["Display Name"], 'Name string & GRID', '', r["Faculty/Fellow"], c[0].strip(), c[1].strip(), pub['title'], '; '.join(authors), pub.get('pmid'), pub['id'], pub.get('doi'), "https://doi.org/{}".format(pub.get('doi')), pub.get('publisher'), journal_title, pub.get('volume'), pub.get('issue'), pub.get('pages'), pub.get('mesh_terms'), pub.get('year'), 'dimensions', datetime.now().strftime("%d/%m/%Y %H:%M:%S")])

no_dupes_per_researcher = pandas.read_csv("output/dimensions_report_smci.csv")
no_dupes_per_researcher.drop_duplicates(subset=["display_name","dimensions_id"], keep='first', inplace=True)
no_dupes_per_researcher.to_csv('output/dimensions_report_smci.csv', index=False)

no_dupes = pandas.read_csv("output/dimensions_report_smci.csv")
no_dupes.drop_duplicates(subset="dimensions_id", keep='first', inplace=True)
no_dupes.to_csv('output/dimensions_report_no_dupes_smci.csv', index=False)
