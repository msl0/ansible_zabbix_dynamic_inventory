# zabbix_inventory.py

Python script to retrieve data from Zabbix API and convert it to Ansible inventory format

## Requirements

- Python3
- pyzabbix

## How to use

1. Download zabbix_inventory.py on Ansible control node
2. Install pyzabbix `pip3 install pyzabbix`
3. Modify file
   - Zabbix URL: [line 23](https://github.com/msl0/ansible_zabbix_dynamic_inventory/blob/main/zabbix_inventory.py#L23)
   - Zabbix user credentials: [line 29](https://github.com/msl0/ansible_zabbix_dynamic_inventory/blob/main/zabbix_inventory.py#L29)
   - optionaly adjust hostgroup criteria to limit groups: [line 38](https://github.com/msl0/ansible_zabbix_dynamic_inventory/blob/main/zabbix_inventory.py#L38) - [45](https://github.com/msl0/ansible_zabbix_dynamic_inventory/blob/main/zabbix_inventory.py#L45)
4. Change permissions to allow execute `chmod +x zabbix_inventory.py`
5. Verify `ansible-inventory -i zabbix_inventory.py --list`

## Note

The script has been tested on Zabbix 5.0
