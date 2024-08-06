import sys
import logging
from ncclient import manager
from ncclient import operations
from ncclient.transport.errors import SSHError
from ncclient.operations.rpc import RPCError

hostname = '192.168.1.1'
port = 830
username = 'admin'
password = 'wq20040903'

def create_vlan_rpc(vlan_id, vlan_name, vlan_description):
    return f"""
<config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
    <top xmlns="http://www.h3c.com/netconf/config:1.0">
        <VLAN xc:operation="create">
            <VLANs>
                <VLANID>
                    <ID>{vlan_id}</ID>
                    <Name>{vlan_name}</Name>
                    <Description>{vlan_description}</Description>
                </VLANID>
            </VLANs>
        </VLAN>
    </top>
</config>
"""

def delete_vlan_rpc(vlan_id):
    return f"""
<config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
    <top xmlns="http://www.h3c.com/netconf/config:1.0">
        <VLAN xc:operation="delete">
            <VLANs>
                <VLANID>
                    <ID>{vlan_id}</ID>
                </VLANID>
            </VLANs>
        </VLAN>
    </top>
</config>
"""

log = logging.getLogger(__name__)

def get_config(hostname, port, username, password):
    try:
        with manager.connect(host=hostname, port=port, username=username,
                             password=password, hostkey_verify=False,
                             device_params={'name': 'h3c'}, timeout=30, allow_agent=False, look_for_keys=False) as m:
            if m.connected:
                print("连接成功")
                n = m._session.id
                print('This session id is %s' % n)
            else:
                print("连接失败")
    except (SSHError, RPCError, AttributeError) as e:
        print(f"连接错误：{str(e)}")

def _check_response(rpc_obj, snippet_name):
    print("RPC reply for %s is %s" % (snippet_name, rpc_obj.xml))
    xml_str = rpc_obj.xml
    if "<ok/>" in xml_str:
        print("%s successful" % snippet_name)
    else:
        print("Cannot successfully execute: %s" % snippet_name)

def add_del_vlan(host, port, user, password, vlan_rpc):
    with manager.connect(host=host, port=port, username=user,
                         password=password, hostkey_verify=False,
                         device_params={'name': 'h3c'}, timeout=30, allow_agent=False, look_for_keys=False) as m:
        rpc_obj = m.edit_config(target='running', config=vlan_rpc)
        _check_response(rpc_obj, 'VLAN_MERGE')


# def add_del_vlan():
#     add_del_vlan_temp(hostname, port, username, password)
