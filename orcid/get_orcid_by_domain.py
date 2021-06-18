import csv, orcid, requests
from requests.auth import HTTPBasicAuth
from getpass import getpass

institution_key = 'APP-HOR65A6E12Q9FHY5'
institution_secret = '3e50093a-7393-4701-b5db-909a11b99c58'


api = orcid.MemberAPI(institution_key, institution_secret, sandbox=True)
search_token = api.get_search_token_from_orcid()
orcids = []
start = 0
one =  api.search('(ringgold-org-id:"6429")OR(affiliation-org-name:"stanford+university")OR(grid-org-id:"grid.168010.e")OR(email:*@stanford.edu)&rows=200&start={}'.format(start), access_token=search_token)
#
two = api.search('(ringgold=6429)OR(grid=grid.168010.e)OR(email=*.stanford.edu)OR(orgname=Stanford%20University)&rows=200&start={}'.format(start), access_token=search_token)
three = api.search('email=*stanford.edu&rows=200&start={}'.format(start), access_token=search_token)
four = api.search('ringgold=6429&rows=200&start={}'.format(start), access_token=search_token)
five = api.search('grid=grid.168010.e&rows=200&start={}'.format(start), access_token=search_token)
six = api.search('orgname=Stanford%20University&rows=200&start={}'.format(start), access_token=search_token)
# two = api.search('grid=grid.168010.e&email=*@stanford.edu&orgname=Stanford%20University&rows=200&start={}'.format(start), access_token=search_token)
# three = api.search('ringgold=6429&email=*@stanford.edu&orgname=Stanford%20University&rows=200&start={}'.format(start), access_token=search_token)
# four = api.search('ringgold=6429&grid=grid.168010.e&email=*@stanford.edu&rows=200&start={}'.format(start), access_token=search_token)
# five = api.search('ringgold=6429&grid=grid.168010.e&email=*@stanford.edu&orgname=Stanford%20University&rows=200&start={}'.format(start), access_token=search_token)
# six = api.search('orgname=Stanford&rows=200&start={}'.format(start), access_token=search_token)

print('All four: {}'.format(two['num-found']))
print('Ringgold only: {}'.format(four['num-found']))
print('Email only: {}'.format(three['num-found']))
print('GRID only: {}'.format(five['num-found']))
print('Org name only: {}'.format(six['num-found']))


# print(four['num-found'])
# print(six['num-found'])

# batch = api.search('ringgold=6429&grid=grid.168010.e&email=*@stanford.edu&orgname=Stanford%20University&rows=200&start={}'.format(start), access_token=search_token)
# while len(batch['result']) > 0:
#     for i in batch['result']:
#         # print(i['orcid-identifier']['path'])
#         orcids.append(i['orcid-identifier']['path'])
#     print('Harvesting records {} to {}.'.format(start, start+len(batch['result'])))
#     start += 200
    # batch = api.search('ringgold=6429&email=*@stanford.edu&rows=200&start={}'.format(start), access_token=search_token)
    # batch = api.search('ringgold=6429&grid=grid.168010.e&emaildomain=stanford.edu&orgname=Stanford%20University&rows=200&start={}'.format(start), access_token=search_token)

with open('output/orcids.csv', 'w') as f:
    write = csv.writer(f)
    write.writerow(['ORCID'])
    for i in orcids:
        write.writerow([i])
