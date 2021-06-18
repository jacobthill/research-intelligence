import csv, dimcli, json, pandas, sys
from datetime import datetime
# Need to add to the path to import config
sys.path.insert(1, '../')
import config

# connect to the database
dimcli.login(config.username, config.password, config.endpoint)
dsl = dimcli.Dsl()

input = pandas.read_csv('test.csv', header=0)

pubs_chunks = dsl.query("""search publications where doi in {} return publications limit 1000""".format(json.dumps(list(input.doi)))).chunks(250)


# test_query = """search publications
# where doi in ["10.1002/0470848944.hsa306", "10.1002/ 2016WR01883", "0.1890/ES14-00296.1"]
# return publications"""

# doi_query = """search publications
#                where doi="\\"{}\\""
#                return publications limit 1000"""

# get specific fields from query
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

query_results = []

# with open('output/test.csv', mode='w') as out:
#     out = csv.writer(out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#     # update
#     out.writerow(["title", "authors", "id", "doi", "publisher", "journal", "volume", "issue", "pages", "pub_year", "provenance", "pub_harvested_date"])


for c in pubs_chunks:
    mypubslist = json.dumps(list(pandas.DataFrame(c).id))

    query_results.append(

              dsl.query_iterative(f"""
                    search publications
                        where reference_ids in {mypubslist}
                        return publications
                    """).as_dataframe()
    )

pandas.concat(query_results).\
drop_duplicates(subset='id').\
to_csv('output/out.csv', index=False)

        # pubs = json.dumps(list(pandas.DataFrame(c).id))
    # query = dsl.query(doi_query.format(row['doi'].strip('DOI: ')))
    # query = dsl.query(f"""search publications
    #                         where doi in {json.dumps(list(input.doi))}
    #                         return publications limit 1000""")

    # query = dsl.query(doi_query)

# for index, row in input.iterrows():

        # for pub in c['publications']:
        #
        #     authors, journal_title = get_fields_from_query(query)
        #     out.writerow([pub['title'], '; '.join(authors), pub['id'], pub.get('doi'), pub.get('publisher'), journal_title, pub.get('volume'), pub.get('issue'), pub.get('pages'), pub.get('year'), 'dimensions', datetime.now().strftime("%d/%m/%Y %H:%M:%S")])
