import csv, json, pandas
import numpy as np

with open('input/som_gi_input_ammended.csv', mode='w') as out:
    out = csv.writer(out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    out.writerow(["Faculty/Fellow", "Institutions", "SUNet ID", "Cap Profile ID", "Email Address"])

    with open('input/author_results_smci.json') as input:
        in_data = json.load(input)
        for i in in_data:
            names = []
            if i.get('middle_name'):
                name = "{} {} {}".format(i.get('first_name'), i.get('middle_name'), i.get('last_name'))
            else:
                name = "{} {}".format(i.get('first_name'), i.get('last_name'))
            names.append(name)
            institutions = ['Stanford']
            if len(i['identities']) > 0:
                for j in i['identities']:
                    if j.get('middle_name'):
                        alt_name = "{} {} {}".format(j.get('first_name'), j.get('middle_name'), j.get('last_name'))
                    else:
                        alt_name = "{} {}".format(j.get('first_name'), j.get('last_name'))
                    names.append(alt_name)
                    if j.get('institution'):
                        if 'Stanford' not in j.get('institution'):
                            institutions.append(j.get('institution'))
            cap_profile_id = i.get('cap_profile_id')


            out.writerow(["; ".join(np.unique(names)), "; ".join(np.unique(institutions)), i.get('sunet'), i.get('cap_profile_id'), i.get('email')])
            # email =
