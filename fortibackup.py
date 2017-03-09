from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient
from getpass import getpass
from datetime import datetime
timestamp = datetime.now().strftime('_%Y-%m-%d-%H-%M-%S')
def getconf(ip, uname, pword = None, fname = 'fortibackup'):
	if not pword:
		pword = getpass()
	ssh = SSHClient()
	ssh.set_missing_host_key_policy(AutoAddPolicy())
	ssh.connect(ip, username=uname, password=pword)
	scp = SCPClient(ssh.get_transport())
	scp.get('fgt-config', local_path=fname+timestamp+'.cfg')
	scp.close()
	ssh.close()