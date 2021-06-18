import csv, dimcli, json, math, pandas, sys
from datetime import datetime
# Need to add to the path to import config
sys.path.insert(1, '../')
import config

# connect to the database
dimcli.login(config.username, config.password, config.endpoint)
dsl = dimcli.Dsl()

input = pandas.read_csv('doi_input.csv', header=0)
print("Raw shape: {}".format(input.shape))
no_dupes = input.drop_duplicates(subset="doi", keep='first', inplace=False)
print("Without dupes: {}".format(no_dupes))
# pandas.read_csv('input.csv', header=0).drop_duplicates('doi', keep='first', inplace=True).shape()

# get specific fields from query
def get_authors(query):
    researcher_ids = []
    author_affiliations = pub.get('authors')
    if author_affiliations:
        for i in author_affiliations:
            researcher_ids.append(i.get('researcher_id'))

    return researcher_ids

chunk_size = 250
start = 0
end = 250
chunks = math.floor(len(list(input.doi)) / chunk_size)
with open('output/output_from_dois.csv', mode='w') as out:
    out = csv.writer(out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    # update
    out.writerow(["title", "authors", "id", "doi", "publisher", "journal", "volume", "issue", "pages", "pub_year", "concepts", "provenance", "pub_harvested_date"])

    for c in range(chunks):
        query = dsl.query("""search publications where doi in {} return publications [all] limit 1000""".format(json.dumps(list(input.doi)[start:end])))

        for pub in query['publications']:

            researcher_ids = get_authors(query)
            # out.writerow([pub['title'], '; '.join(authors), pub['id'], pub.get('doi'), pub.get('publisher'), journal_title, pub.get('volume'), pub.get('issue'), pub.get('pages'), pub.get('year'), 'dimensions', datetime.now().strftime("%d/%m/%Y %H:%M:%S")])
            out.writerow([pub['title'], '; '.join(researcher_ids), pub['id'], pub.get('doi'), pub.get('publisher'), pub.get('journal'), pub.get('volume'), pub.get('issue'), pub.get('pages'), pub.get('year'), pub.get('concepts'), 'dimensions', datetime.now().strftime("%d/%m/%Y %H:%M:%S")])

        start+=chunk_size
        end+=chunk_size

    query = dsl.query("""search publications where doi in {} return publications [all] limit 1000""".format(json.dumps(list(input.doi)[start:])))

    for pub in query['publications']:

        researcher_ids = get_authors(query)
        out.writerow([pub['title'], '; '.join(researcher_ids), pub['id'], pub.get('doi'), pub.get('publisher'), pub.get('journal'), pub.get('volume'), pub.get('issue'), pub.get('pages'), pub.get('year'), pub.get('concepts'), 'dimensions', datetime.now().strftime("%d/%m/%Y %H:%M:%S")])
