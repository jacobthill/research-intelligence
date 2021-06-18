import csv, orcid, requests
from lxml import etree
from requests.auth import HTTPBasicAuth
from getpass import getpass
import pandas as pd

institution_key = 'APP-HOR65A6E12Q9FHY5'
institution_secret = '3e50093a-7393-4701-b5db-909a11b99c58'

api = orcid.PublicAPI(institution_key, institution_secret, sandbox=True)
search_token = api.get_search_token_from_orcid()

search = "http://www.orcid.org/ns/search"
common = "http://www.orcid.org/ns/common"

email_tree = etree.parse("output/orcids/orcid-public-email.xml")
email_records = email_tree.findall('/*/*/{http://www.orcid.org/ns/common}path')
print('There are {} records returned from email only.'.format(len(email_records)))

all_tree = etree.parse("output/orcids/orcid-public-all.xml")
all_records = all_tree.findall('/*/*/{http://www.orcid.org/ns/common}path')
print('There are {} records returned from search all four fields.'.format(len(all_records)))

# for r in email_records:
# # for o in orcids['ORCID']:
#     try:
#         q = api.read_record_public(r.text, 'record', search_token)
#         # q = api.search('ringgold=6429&?q={}:given-names,given-and-family-names,current-institution-affiliation-name'.format(r.text), access_token=search_token)
#         first_name = q['person']['name']['given-names'].get('value')
#         last_name = q['person']['name']['family-name'].get('value')
#         print(q['activities-summary'])
#     except:
#         print('not found')
#         pass

# while len(batch['result']) > 0:
#     for i in batch['result']:
#         # print(i['orcid-identifier']['path'])
#         orcids.append(i['orcid-identifier']['path'])
#     print('Harvesting records {} to {}.'.format(start, start+len(batch['result'])))
#     start += 200
#     batch = api.search('ringgold=6429&email=*@stanford.edu&rows=200&start={}'.format(start), access_token=search_token)
    # batch = api.search('ringgold=6429&grid=grid.168010.e&emaildomain=stanford.edu&orgname=Stanford%20University&rows=200&start={}'.format(start), access_token=search_token)

# with open('output/orcids.csv', 'w') as f:
#     write = csv.writer(f)
#     write.writerow(['ORCID'])
#     for i in orcids:
#         write.writerow([i])
