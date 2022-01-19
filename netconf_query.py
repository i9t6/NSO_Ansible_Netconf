#! /usr/bin/env python
# python netconf_query.py -a 172.16.1.16 -u cisco -p cisco --port 830

import lxml.etree as et
from argparse import ArgumentParser
from ncclient import manager
from ncclient.operations import RPCError
import xmltodict

payload = [
'''
<get xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <filter>
    <rib xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ip-rib-ipv4-oper">
      <vrfs>
        <vrf>
          <vrf-name>default</vrf-name>
          <afs>
            <af>
              <af-name>IPv4</af-name>
              <safs>
                <saf>
                  <saf-name>Unicast</saf-name>
                </saf>
              </safs>
            </af>
          </afs>
        </vrf>
      </vrfs>
    </rib>
  </filter>
</get>
''',
]

if __name__ == '__main__':

    parser = ArgumentParser(description='Usage: python netconf_query.py -a 172.16.1.16 -u cisco -p cisco --port 830')

    # script arguments
    parser.add_argument('-a', '--host', type=str, required=True,
                        help="Device IP address or Hostname")
    parser.add_argument('-u', '--username', type=str, required=True,
                        help="Device Username (netconf agent username)")
    parser.add_argument('-p', '--password', type=str, required=True,
                        help="Device Password (netconf agent password)")
    parser.add_argument('--port', type=int, default=830,
                        help="Netconf agent port")
    args = parser.parse_args()

    # connect to netconf agent
    with manager.connect(host=args.host,
                         port=args.port,
                         username=args.username,
                         password=args.password,
                         timeout=90,
                         device_params={'name':'iosxr'},
                         hostkey_verify=False) as m:

        # execute netconf operation
        for rpc in payload:
            try:
                response = m.dispatch(et.fromstring(rpc))
                data_xml = et.fromstring(response.xml)
                rib_dict = xmltodict.parse(response.xml)["rpc-reply"]["data"]
            except RPCError as e:
                data = e._raw

            # beautify output
            print(et.tostring(data_xml, pretty_print=True,encoding='unicode' ))
            
            # print response.xml
            # print(response.xml)

            # print as dictionary
            # print(rib_dict)
