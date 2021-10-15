#!/home/cisco/py3/bin/python
from ncclient import manager
from ncclient.xml_ import to_ele
import xmltodict
import json
import csv
import re
import sys
import requests

nso_srv = {'host':'172.16.1.125','port':'2022','username':'admin','password':'admin','hostkey_verify':False}

def read_csv(var_csv_file, var_key):
    data = {}
    with open(var_csv_file, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf,delimiter=';')
        for rows in csvReader:
            key = rows[var_key]
            if not '#' in key:
                data[key] = rows
    return data

def fix_device_list(var_srv,var_key,var_data,var_case):
    dic={}
    with manager.connect(**nso_srv) as m:
        for key in var_data.keys():
            netconf_reply = m.get(filter=('xpath',f"/services/{var_srv}[{var_key}='{key}']/device-list"))
            devices_list = xmltodict.parse(netconf_reply.xml)["rpc-reply"]["data"]
            if not devices_list == None:
                if type(devices_list['services'][var_srv]['device-list']) == type('str'):
                    dic[key] = [devices_list['services'][var_srv]['device-list']]
                else:
                    dic[key] = devices_list['services'][var_srv]['device-list']
            else:
                dic[key] = []
    for key, values in var_data.items():
        final_list =[]
        if not values['devices'] == '':
            for device in eval(values['devices']):
                if var_case == 'config':
                    final_list = dic[key]
                    if not device in dic[key]:
                        final_list.append(device)
                elif var_case == 'delete':
                    final_list.append(device)
        else:
            final_list = []
        var_data[key]['devices'] = final_list
    #print(var_data)
    return var_data

def fill_template_qos(var_template_file,var_data, var_verbose):
    dic = {}
    netconf_template = open(var_template_file).read()
    for key, values in var_data.items():
        list = []
        for line in netconf_template.split('\n'):
            if (('delete' in line) and (not "device" in line)):
                if not len(values['devices']) == 0:
                    final_line = line.replace("operation=\"delete\"", "" )
                    list.append(final_line)
                else:
                    list.append(line)
            elif '{' in line:
                value = re.search(r"\{(.*)\}",line).group(1)
                if not value == 'devices':
                    if not values[value] == '':
                        final_line = line.replace("{" + value + "}", values[value] )
                        list.append(final_line)
                    else:
                        continue
                else:
                    for device in values['devices']:
                        final_line = line.replace("{" + value + "}",device)
                        list.append(final_line)
            else:
                list.append(line)
        # verbose
        if 'v' in var_verbose:
            for i in list:
                print(i)    
        dic[key]="\n".join(list)
    return dic

def config_netconf(var_dic_templates,):
    with manager.connect(**nso_srv) as m:
        for key, case in var_dic_templates.items():
            try:
                netconf_reply = m.edit_config(case, target="running", default_operation='merge')        
            except:
                print(f"Error {key}, Posible servicio o equipo no existente")
            else:
                if netconf_reply.ok:
                    print(f"Service: {key} : Change Completed")
    return 'Netconf config: Done'

def reconcile(var_dic_reconcile):
    
    payload = json.dumps({"input": {"reconcile": { }}})
    headers = {'Accept': 'application/yang-data+json','Content-Type': 'application/yang-data+json','Authorization': 'Basic YWRtaW46YWRtaW4='}
    
    for key, info in var_dic_reconcile.items():
        url = f"http://172.16.1.125:8080/restconf/data/tailf-ncs:services/Srv_Policy_Map:Srv_Policy_Map={key}/re-deploy"
        response = requests.request("POST", url, headers=headers, data=payload)
        print(f"Re-deploy/Reconcile {key}: {response}   (204 es ok)")
        for device in info['devices']:
            for i in ['compare-config','check-sync']:
                url = f"http://172.16.1.125:8080/restconf/data/tailf-ncs:devices/device={device}/{i}"
                response = requests.request("POST", url, headers=headers)
                if response.json() == {}:
                    print(f"\t{i} {device}: Sin cambios")
                else:
                    print(f"\t{i} {device}: {response.json()['tailf-ncs:output']}")
    return '\nReconcile complete\n'


if __name__ == '__main__':
    try:
        option = sys.argv[1]
    except:
        option = 'c'
    try:
        verbose = sys.argv[2]
    except:
        verbose = ''
    if 'c' in option :
        data = read_csv('srv_policy.csv','policy_name')
        if 'v' in verbose:
            print(data,"\n-----------------------")
        data_fixed = fix_device_list('Srv_Policy_Map','policy_name', data, 'config')
        if 'v' in verbose:
            print(data_fixed,"\n-----------------------")
        dic_templates = fill_template_qos('config_qos.xml', data_fixed, verbose) 
        print(config_netconf(dic_templates),"\n-----------------------")
    elif 'd' in option:
        data_delete = read_csv('srv_policy_delete.csv','policy_name')
        if 'v' in verbose:
            print(data_delete,"\n-----------------------")
        data_fixed_delete = fix_device_list('Srv_Policy_Map','policy_name', data_delete,'delete')
        if 'v' in verbose:
            print(data_fixed_delete,"\n-----------------------")
        dic_templates_delete = fill_template_qos('config_qos_delete.xml', data_fixed_delete, verbose)
        print(config_netconf(dic_templates_delete),"\n-----------------------")
    elif 'r' in option:
        # Se puede hacer en 2 pasos, configurar y despues reconcile
        data_reconcile = read_csv('srv_policy_reconcile.csv','policy_name')
        if 'v' in verbose:
            print(data_reconcile,"\n-----------------------")
        data_fixed = fix_device_list('Srv_Policy_Map','policy_name', data_reconcile, 'config')
        if 'v' in verbose:
            print(data_fixed,"\n-----------------------")
        dic_templates = fill_template_qos('config_qos.xml', data_fixed, verbose) 
        print(config_netconf(dic_templates),"\n-----------------------")
        print(reconcile(data_reconcile))
    print("------ COMPLETE ------")


        