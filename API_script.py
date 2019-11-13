#
# Demo script to use Actfio API to perform a mount
#
# Warning - currently does not do any error checking

# Parameters
sky = '172.27.24.146'
vendorkey = 'YourVendorKey'
appname = 'ebidb'
target = 'ebimysql3'
targetMountPoint = '/mysql'

# Begin script

import requests, urllib3

# API - Login
#
url = "https://" + sky + "/actifio/api/login?vendorkey=" + vendorkey
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
requests.packages.urllib3.disable_warnings()
payload = ""
headers = {
    'Authorization': "Basic YWRtaW46cGFzc3dvcmQ=",
    'cache-control': "no-cache",
    }
response = requests.request("POST", url, data=payload, headers=headers, verify=False)

session = response.json()['sessionid']
print("Session ID is " + session)

headers = {
    'Authorization': "Actifio " + response.json()['sessionid'],
    'cache-control': "no-cache",
    }

# API - lsapplication
#
api = "https://" + sky + "/actifio/api/info/lsapplication"
filter = "appname=" + appname
url = api + '?filtervalue=' + requests.utils.quote(filter)
response = requests.request("GET", url, headers=headers, verify=False)

appid = response.json()['result'][0]['id']
print("App ID for application " + appname + " is " + appid)

# API - lshost
#
api = "https://" + sky + "/actifio/api/info/lshost"
filter = "hostname=" + target
url = api + '?filtervalue=' + requests.utils.quote(filter)
response = requests.request("GET", url, headers=headers, verify=False)
hostid = response.json()['result'][0]['id']

print("Host ID for client " + target + " is " + hostid)

# API - mountimage
#
roxml = "mountpointperimage=" + targetMountPoint
api = "https://" + sky + "/actifio/api/task/mountimage"
params = "?host=" + hostid + "&appid=" + appid + "&nowait=true" + "&restoreoption=" + requests.utils.quote(roxml)
url = api + params
response = requests.request("POST", url, data=payload, headers=headers, verify=False)

print(response.json())
