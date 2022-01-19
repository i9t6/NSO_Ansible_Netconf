# GET
import requests

netconf-console
netconf-console --host=127.0.0.1 -u admin -p admin --port 2022 -i

netconf-console --host=172.16.1.16 -u cisco -p cisco --port 830 -i
usar codigo en ping.xml

<action xmlns="urn:ietf:params:xml:ns:yang:1">
  <services xmlns="http://tail-f.com/ns/ncs">
   <vrf xmlns="http://example.com/vrf">
    <name>vrf_1</name>
     <re-deploy/>
   </vrf>
  </services>
</action>

<rpc message-id="101" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">

 <action xmlns="http://tail-f.com/ns/netconf/actions/1.0">
  <data>
  <devices xmlns="http://tail-f.com/ns/ncs">
   <device>
    <name>c0</name>
     <ping/>
   </device>
  </devices>
 </data>
</action>

<action xmlns="http://tail-f.com/ns/netconf/actions/1.0">
  <data>
    <services xmlns="http://tail-f.com/ns/ncs">
      <Srv_Policy_Map xmlns="http://example.com/Srv_Policy_Map">
        <policy_name>100Mbps</policy_name>
        <re-deploy>
         <reconcile/>
        </re-deploy>
      </Srv_Policy_Map>
    </services>  
  </data>
</action>

a2 = etree.Element("action",  nsmap = {None: 'http://tail-f.com/ns/netconf/actions/1.0'})
data = etree.SubElement(a2, "data")
srvs = etree.SubElement(data, "services", nsmap = {None: 'http://tail-f.com/ns/ncs'})
srv_pol_map = etree.SubElement(srvs, "Srv_Policy_Map",nsmap = {None: 'http://example.com/Srv_Policy_Map'})
pn = etree.SubElement(srv_pol_map, "policy_name").text = "110Mbps"
rd = etree.SubElement(srv_pol_map, "re-deploy")
rc = etree.SubElement(rd,"reconcile")
print(etree.tostring(a2))

<action xmlns="http://tail-f.com/ns/netconf/actions/1.0">
  <data>
    <services xmlns="http://tail-f.com/ns/ncs">
      <Srv_Policy_Map xmlns="http://example.com/Srv_Policy_Map">
        <policy_name>100Mbps</policy_name>
        <re-deploy/>
      </Srv_Policy_Map>
    </services>
  </data>
</action>


<action xmlns="http://tail-f.com/ns/netconf/actions/1.0">
  <data>
    <devices xmlns="http://tail-f.com/ns/ncs">
    <device>
      <name>xr0</name>
      <check-sync/>
    </device>
  </devices>
  </data>
</action>

</rpc>

reqUrl = "http://172.16.1.122:8080/restconf/data/tailf-ncs:services/port-turnup:port-turnup"

headersList = {
 "Accept": "application/yang-data+json",
 "User-Agent": "Thunder Client (https://www.thunderclient.io)",
 "Authorization": "Basic YWRtaW46YWRtaW4=" 
}

payload = ""

response = requests.request("GET", reqUrl, data=payload,  headers=headersList)

print(response.text)

#----------------
# get detailed
import requests

reqUrl = "http://172.16.1.122:8080/restconf/data/tailf-ncs:services/port-turnup:port-turnup=c0,GigabitEthernet,3%2F0"

headersList = {
 "Accept": "application/yang-data+json",
 "User-Agent": "Thunder Client (https://www.thunderclient.io)",
 "Content-Type": "application/yang-data+json",
 "Authorization": "Basic YWRtaW46YWRtaW4=" 
}

payload = ""

response = requests.request("GET", reqUrl, data=payload,  headers=headersList)

print(response.text)

#---------------------------------
# POST
reqUrl = "http://172.16.1.122:8080/restconf/data/tailf-ncs:services/"

headersList = {
 "Accept": "application/yang-data+json",
 "User-Agent": "Thunder Client (https://www.thunderclient.io)",
 "Content-Type": "application/yang-data+json",
 "Authorization": "Basic YWRtaW46YWRtaW4=",
 "Content-Type": "application/json" 
}

payload = "{\n  \"port-turnup:port-turnup\": [{\n  \"device\": \"c0\",\n  \"interface_type\": \"GigabitEthernet\",\n  \"interface_number\": \"3/0\",\n  \"description\":\"algo\",\n  \"mtu\":1514\n } ]}\n"

response = requests.request("POST", reqUrl, data=payload,  headers=headersList)

print(response.text)

{
  "port-turnup:port-turnup": [{
  "device": "c0",
  "interface_type": "GigabitEthernet",
  "interface_number": "3/0",
  "mtu":1514,
  "description":"algo"
 } ]}
#-------------------------- ----------------------------
# PATH
import requests

reqUrl = "http://172.16.1.122:8080/restconf/data/tailf-ncs:services/port-turnup:port-turnup"

headersList = {
 "Accept": "application/yang-data+json",
 "User-Agent": "Thunder Client (https://www.thunderclient.io)",
 "Content-Type": "application/yang-data+json",
 "Authorization": "Basic YWRtaW46YWRtaW4=",
 "Content-Type": "application/json" 
}

payload = "{\n  \"port-turnup:port-turnup\": [{\n  \"device\": \"c0\",\n  \"interface_type\": \"GigabitEthernet\",\n  \"interface_number\": \"3/0\",\n  \"description\":\"algo algo\",\n  \"mtu\":9000\n } ]}\n"

response = requests.request("PATCH", reqUrl, data=payload,  headers=headersList)

print(response.text)

#-------------------------------------------------
# delete
import requests

reqUrl = "http://172.16.1.122:8080/restconf/data/tailf-ncs:services/port-turnup:port-turnup=c0,GigabitEthernet,3%2F1"

headersList = {
 "Accept": "application/yang-data+json",
 "User-Agent": "Thunder Client (https://www.thunderclient.io)",
 "Content-Type": "application/yang-data+json",
 "Authorization": "Basic YWRtaW46YWRtaW4=" 
}

payload = ""

response = requests.request("DELETE", reqUrl, data=payload,  headers=headersList)

print(response.text)

# --------------------
 # GET

 import requests

reqUrl = "http://172.16.1.122:8080/restconf/data/tailf-ncs:services/vrf:vrf"
reqUrl = "http://172.16.1.122:8080/restconf/data/tailf-ncs:services/vrf:vrf=vrf_2"

headersList = {
 "Accept": "application/yang-data+json",
 "User-Agent": "Thunder Client (https://www.thunderclient.io)",
 "Content-Type": "application/yang-data+json",
 "Authorization": "Basic YWRtaW46YWRtaW4=",
 "Content-Type": "application/json" 
}

payload = "{\n  \"port-turnup:port-turnup\": [{\n  \"device\": \"c0\",\n  \"interface_type\": \"GigabitEthernet\",\n  \"interface_number\": \"3/5\",\n  \"mtu\":999,\n  \"description\":\"algo_conpath\"\n } ]}"

response = requests.request("GET", reqUrl, data=payload,  headers=headersList)

print(response.text)


#------------------------
# post
{
  "vrf:vrf": [
    {
      "name": "vrf_3",
      "devices": [
        {
          "device": "c0",
          "primary_route_target": "300:301"
        },
        {
          "device": "xr0",
          "primary_route_target": "300:300"
        }
      ]
    }
  ]
}

{
  "vrf:vrf": [
    {"name": "vrf_4",
      "devices": [
        {
          "device": "c0",
          "primary_route_target": "400:200",
          "RT_import": [
            "400:210"
          ],
          "RT_export": [
            "400:211"
          ]
        },
        {
          "device": "xr0",
          "primary_route_target": "400:202",
          "RT_import": [
            "400:220"
          ],
          "RT_export": [
            "400:221"
          ],
          "iosxr": {
            "route_map_import": "PASS",
            "route_map_export": "PASS"
          }
        }
      ]
    }
  ]
}

{
  "Srv_Policy_Map:Srv_Policy_Map": [
    {
      "policy_name": "50M",
      "cir": 10,
      "units": "mbps",
      "cir_xe": "10000",
      "units_xe": "bps",
      "device": [
        "c0",
        "xr0"
      ]
    }
  ]
}

import requests

reqUrl = "http://172.16.1.122:8080/restconf/data/tailf-ncs:services//Srv_Policy_Map:Srv_Policy_Map"

headersList = {
 "Accept": "application/yang-data+json",
 "User-Agent": "Thunder Client (https://www.thunderclient.io)",
 "Content-Type": "application/yang-data+json",
 "Authorization": "Basic YWRtaW46YWRtaW4=",
 "Content-Type": "application/json" 
}

payload = "{\n  \"Srv_Policy_Map:Srv_Policy_Map\": [\n    {\n      \"policy_name\": \"50M\",\n      \"cir\": 50,\n      \"units\": \"mbps\",\n      \"cir_xe\": \"50000\",\n      \"units_xe\": \"bps\",\n      \"device\": [\n        \"c0\",\n        \"xr0\"\n      ]\n    }\n  ]\n}"

response = requests.request("PATCH", reqUrl, data=payload,  headers=headersList)

print(response.text)


{
  "l3vpn:l3vpn_client": [
    {
      "client": "cliente_1",
      "client_id": 1000,
      "site": "1001",
      "vpn_attachments": [
        {
          "circuit_id": "10001",
          "device": "c0",
          "iosxe": {
            "vrf": "vrf_1",
            "policy_map": "10M"
          },
          "static_route": [
            {
              "LAN_prefix": "10.0.0.0",
              "LAN_mask": "255.255.255.0",
              "next_hop_address": "2.2.2.2"
            }
          ],
          "interface": {
            "WAN_prefix": "30.0.0.0",
            "WAN_mask": "255.255.255.252",
            "proxy_arp": [null],
            "iosxe": {
              "dot1q_tag": 100,
              "second_dot1q_tag": 200,
              "GigabitEthernet": {
                "ifnumber": "3/0"
              }
            }
          }
        }
      ]
    }
  ]
}

{
  "l3vpn:l3vpn_client": [
    {
      "client": "cliente_1",
      "client_id": 1000,
      "site": "1000",
      "vpn_attachments": [
        {
          "circuit_id": "10000",
          "device": "xr0",
          "iosxr": {
            "vrf": "vrf_1",
            "policy_map": "10M"
          },
          "static_route": [
            {
              "LAN_prefix": "10.0.0.0",
              "LAN_mask": "255.255.255.0",
              "next_hop_address": "2.2.2.2"
            }
          ],
          "interface": {
            "WAN_prefix": "30.0.0.0",
            "WAN_mask": "255.255.255.252",
            "proxy_arp": [null],
            "iosxr": {
              "dot1q_tag": 100,
              "second_dot1q_tag": 200,
              "GigabitEthernet": {
                "ifnumber": "3/0"
              }
            }
          }
        }
      ]
    }
  ]
}


import requests

reqUrl = "https://172.16.1.122:7443/restconf/operations/show_action:action/show-action"

headersList = {
 "Accept": "application/yang-data+json",
 "Content-Type": "application/yang-data+json",
 "Authorization": "Basic YWRtaW46YWRtaW4=",
 "Content-Type": "application/json" 
}

payload = "{\n    \"device_name\":\"xr0\",\n    \"command\":\"show version\"\n}"

response = requests.request("POST", reqUrl, data=payload,  headers=headersList)

print(response.text)