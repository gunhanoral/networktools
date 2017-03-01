import requests
import getpass
import sys
import json
from pandas.io.json import json_normalize

if len(sys.argv) < 3:
	fortigate_host = input('IP Address: ')
	fortigate_user = input('Username: ')

else:
	fortigate_host = sys.argv[1]
	fortigate_user = sys.argv[2]

fortigate_pass = getpass.getpass()
login_url = f'https://{fortigate_host}/logincheck'
login_payload = {'username': fortigate_user, 'secretkey': fortigate_pass}

s = requests.session()
s.keep_alive = False
r = s.post(login_url, data=login_payload, verify=False)
cookiejar = r.cookies

print(r.headers)
print(r.text)

#the structure to query stuff follows the cmdb (cli structure)
#https://{fortigate_host}/api/v2/cmdb/firewall/address?vdom=root
#https://{fortigate_host}/api/v2/cmdb/firewall/policy?vdom=root
#https://{fortigate_host}/api/v2/cmdb/firewall/policy6?vdom=root
#https://{fortigate_host}/api/v2/cmdb/system/interface/
#https://{fortigate_host}/api/v2/cmdb/firewall/vip?vdom=LOCAL-FW

r = s.get(f'https://{fortigate_host}/api/v2/cmdb/firewall/vip?vdom=LOCAL-FW',
             cookies=cookiejar, verify=False)
s.close()
data = json.loads(r.text)
print(json_normalize(data['results']).head())
