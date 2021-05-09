#!/usr/bin/python3

from pyzabbix import ZabbixAPI
import json
import urllib3
import sys

# Parse arguments
opts = [opt for opt in sys.argv[1:] if opt.startswith("--")]
args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

if "--list" in opts and args == []:
  opt = "list"
elif "--host" in opts and args != []:
  opt = "host"
else:
  raise SystemExit(f"Usage: {sys.argv[0]} --list\n\t\t\t\t\t--host <HOST>")

# Disable certificate warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Zabbix URL
zabbix = ZabbixAPI("https://zabbix.local")

# Disable certifaicate verification
zabbix.session.verify = False

# Credentials
zabbix.login('user', 'password')

# Create dictionary
output = {}

if opt == "list":
  # Create section for host variables
  output.update({"_meta": { "hostvars": {}}})
  
  # Get hosts from hostgroups Windows and Linux
  #groups = zabbix.hostgroup.get(selectHosts=["host"], real_hosts=True, output=["name"], filter={ "name": ["Windows", "Linux"]})
  
  # Get hosts from all hostgroups
  #groups = zabbix.hostgroup.get(selectHosts=["host"], real_hosts=True, output=["name"])
  
  # Get hosts from all hostgroups except Discovered hosts
  groups = zabbix.hostgroup.get(selectHosts=["host"], real_hosts=True, output=["name"], search={ "name": "Discovered hosts"}, excludeSearch=True)
  
  for group in groups:
    # Create lists for hosts
    host_list = []

    for host in group['hosts']:
      # Add each host to host_list
      host_list.append(host['host'])

      # Get IP address for default host interface and add in host variable
      host_ip = zabbix.hostinterface.get(hostids=host['hostid'], filter={ "main": "1" }, selectHosts=["host"], output=['ip'])[0]['ip']
      output['_meta']['hostvars'].update( { host['host']: { "ansible_host": host_ip }})

      # Add host to group section in output
      output.update({ group['name']: { "hosts": host_list} })

if opt == "host":
  # Get host
  host = zabbix.host.get(filter={ "name": args[0]})[0]

  # Get IP address for default host interface and add in host variable
  host_ip = zabbix.hostinterface.get(hostids=host['hostid'], filter={ "main": "1" }, selectHosts=["host"], output=['ip'])[0]['ip']
  
  # Add host variable to output
  output.update({ "ansible_host": host_ip })

# Change to readable format
print(json.dumps(output, indent=4))

# Logout
zabbix.do_request('user.logout')