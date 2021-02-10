from os import read
import requests
import json
import re

# disable ssl warnings
requests.packages.urllib3.disable_warnings()


#f5ip = rawdata("Enter the F5 IP Address: ")
f5ip = '192.168.1.5'
f5auth = 'YWRtaW46YWRtaW4='

# Get the device version
versionuri = '/mgmt/tm/cli/version'
vurl = "https://"+f5ip+versionuri+"?expandSubcollections=true"

payload = {}
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic '+f5auth+"'",
}

vresponse = requests.request(
    "GET", vurl, headers=headers, data=payload, verify=False)
f5version = vresponse.json()[
    u'entries'][u'https://localhost/mgmt/tm/cli/version/0'][u'nestedStats'][u'entries'][u'active'][u'description']

vernum = (str(f5version).split(".", 1)[0])

# Get the profile data

with open('/mnt/e/Git/get-profiles/profilescope', 'r') as f, \
        open('/mnt/e/Git/get-profiles/temp', 'w') as w:
    w.write('[\n')
    for line in f.readlines():
        prftype, prfname = line.split()
        w.write('{\n')
        w.write((f'\"profileType\": \"{prftype}\" , \"profileName\": \"{prfname}\",'))
        w.write('\n\"profileData\":\n')

        prfuri = '/mgmt/tm/ltm/profile/'+prftype+"/"+prfname
        prfurl = "https://"+f5ip+prfuri+"?expandSubcollections=true"

        prfresponse = requests.request(
            "GET", prfurl, headers=headers, data=payload, verify=False)
        json.dump(prfresponse.json(), w)
        w.write('\n},')
    w.write('\n]')

    regex = r"(\,\n\])"
    subst = "\\n]"

with open('/mnt/e/Git/get-profiles/temp', 'r') as regexdata, \
        open('/mnt/e/Git/get-profiles/v'+vernum+'/profiledata.json', 'w') as regexwrite:
    result = re.sub(regex, subst, regexdata.read(), flags=re.M)
    regexwrite.write(result)
