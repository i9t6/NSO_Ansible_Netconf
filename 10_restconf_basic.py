#!/usr/bin/python

import json
import csv
import sys
import requests
import logging
from datetime import datetime
import urllib3

urllib3.disable_warnings()

date = datetime.now().date().strftime('%Y-%d-%m')
console_formartter = logging.Formatter('%(asctime)s:module:%(module)s>> %(message)s')
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(console_formartter)
my_logger = logging.getLogger()
my_logger.addHandler(console_handler)

"""
POST https://10.57.236.6:8443/restconf/tailf/query
{"immediate-query": {
    "foreach": "/devices/device",
    "select": [{
        "label": "Host name",
        "expression": "name",
        "result-type": ["string"]
    }],
    "sort-by": ["name"],
    "limit": 100,
    "offset": 1
}}

{"immediate-query": {
    "foreach": "/devices/device[address = '2.2.2.2']",
    "select": [{
 
        "expression": "name",
        "result-type": ["string"]
    },{
        "expression": "address",
        "result-type": ["string"]}
    ],
    "sort-by": ["name"],
    "limit": 100,
    "offset": 1
}
}

    my NSO
    "Authorization": "Basic YWRtaW46YWRtaW4=",
    
    Entel
    "Authorization": "Basic cXVpcm96ZjpFbnQzbDEyMzQ=",
    """
nso_port = "10.57.236.6:8443"
#nso_port = "172.16.1.122:8443"

def read_csv(var_csv_file, *var_key):
    with open(var_csv_file, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf,delimiter=',')
        if var_key:
            data = {}
            for rows in csvReader:
                key = rows[var_key[0]]
                if not '#' in key:
                    data[key] = rows
        else:
            data = []
            for rows in csvReader:
                data.append(rows)
    return data

def get_devices():
    headersList = {
            "Accept": "application/yang-data+json",
            "Content-Type": "application/yang-data+json",
            "Authorization": "Basic cXVpcm96ZjpFbnQzbDEyMzQ=",
    }
    reqUrl_data = f"https://{nso_port}/restconf/data/tailf-ncs:devices/device?fields=name;address"
    response = requests.request("GET", reqUrl_data,  headers=headersList, verify=False) 
    return response.json()['tailf-ncs:device']

def check_status(var_devices_list):
    headersList = {
            "Accept": "application/yang-data+json",
            "Content-Type": "application/yang-data+json",
            "Authorization": "Basic cXVpcm96ZjpFbnQzbDEyMzQ=",
    }
    reqUrl = f"https://{nso_port}/restconf/operations/tailf-ncs:devices/device=--device--/--operation--"
    print(f"""{'#':<10} {'Name':<40} {'Address':<20} {'Connect':<15} {'Check-sync':}""")
    print(f"""{'-'*100}""")
    i=1
    for device in var_devices_list:
        total = len(var_devices_list)
        temp_url = reqUrl.replace('--device--',device['name'])
        
        response = requests.request("POST", temp_url.replace('--operation--','connect'), headers=headersList, verify=False)
        device['connect'] = response.json()['tailf-ncs:output']['result']
        if not device['connect']:
            device['check-sync'] = "No Sync Check"
            device['connect'] = "No Connection"
        else:
            response = requests.request("POST", temp_url.replace('--operation--','check-sync'), headers=headersList, verify=False)
            device['check-sync'] = response.json()['tailf-ncs:output']['result']
        print(f"""{i}/{total:<10} {device['name']:<35} {device['address']:<20} {device['connect']:<15} {device['check-sync']:}""")
        i += 1
    with open('devices_list.txt','w') as f:
        for line in var_devices_list:
            f.write(str(line)+"\n")
    return var_devices_list

def print_table(var_devices_list):
    print(f""" {'Name':<20} {'Address':<20} {'Check-sync':<15} {'Connect':}""")
    print(f"""{'-'*70}""")
    for device in var_devices_list:
        print(f""" {device['name']:<20} {device['address']:<20} {device['check-sync']:<15} {device['connect']:}""")

 
if __name__ == '__main__':
    try:
        option = sys.argv[1]
    except:
        option = 'c'
    
    try:
        verbose = sys.argv[2]
    except:
        verbose = ''

    # ERROR < WARNING < INFO
    if 'vv' in verbose:    
        vb = 'INFO'
    elif 'v' in verbose:
        vb='WARNING'
    else:
        vb ='ERROR'
    my_logger.setLevel(eval(f"logging.{vb}"))

    # Configure
    if 'c' in option :
        result = check_status( get_devices())
        

    # Delete
    elif 'd' in option:
        data_list = read_csv('ptu_vars.csv')
        my_logger.warning(f"{data_list}\n-----------------------")

        result = restconf_nso('delete','ptu',data_list)
        print(result)    
    # Patch (modify)
    elif 'p' in option:
        data_list = read_csv('ptu_vars.csv')
        my_logger.warning(f"{data_list}\n-----------------------")

        result = restconf_nso('patch','ptu',data_list)
        print(result) 
    # Reconcile
    elif 'r' in option:
        data_list = read_csv('ptu_vars_reconcile.csv')
        my_logger.warning(f"{data_list}\n-----------------------")

        result = restconf_nso('reconcile','ptu',data_list)
        print(result)

    print("------ COMPLETE ------")