# networktools
Simple tools for some basic Fortigate .

### fortirest.py

This is a basic use of Fortigate API. Right now there are no comprehensive guides or examples for Fortigate API. You may use this as an example.

### fortibackup.py

To use this under config system global, admin-scp must be enabled.
And you need paramiko, scp modules.

Then you may get config backups. An unsophisticated example:

```python
fortigates = {
	'FW1': '1.1.1.1',
	'FW2': '2.2.2.2',
	'FW3': '3.3.3.3',
	'FW4': '4.4.4.4'
}

for fw_name, ipaddress in fortigates.items():
	try:
		getconf(ip = ipaddress, fname = fw_name, uname = 'username', pword = 'password')
		print(f'Got {fw_name} backup config.')
	except:
		print(f'Couldn\'t get {fw_name}\'s backup config from {ipaddress}')
```
