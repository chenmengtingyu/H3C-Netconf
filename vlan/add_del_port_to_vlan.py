import sys
import logging
from ncclient import manager
from ncclient import operations
from ncclient.transport.errors import SSHError
from ncclient.operations.rpc import RPCError

hostname = '192.168.1.1'
port = 830
username = 'admin'
password = 'admin'

def create_interface_vlan_rpc(interface_name, vlan_id):
    return f"""
<config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
    <top xmlns="http://www.h3c.com/netconf/config:1.0">
        <Ifmgr>
            <Interfaces>
                <Interface>
                    <IfIndex>{interface_name}</IfIndex>
                    <LinkType>1</LinkType> <!-- 1代表Access -->
                    <PVID>{vlan_id}</PVID>
                </Interface>
            </Interfaces>
        </Ifmgr>
    </top>
</config>
"""

def delete_interface_from_vlan_rpc(interface_name):
    return f"""
<config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
    <top xmlns="http://www.h3c.com/netconf/config:1.0">
        <Ifmgr>
            <Interfaces>
                <Interface>
                    <IfIndex>{interface_name}</IfIndex>
                    <LinkType>1</LinkType> <!-- 重置为默认LinkType, 可能需要根据实际情况调整 -->
                    <PVID>1</PVID> <!-- 重置PVID为默认值，通常是1 -->
                </Interface>
            </Interfaces>
        </Ifmgr>
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

def vlan_int_mgmt_temp(host, port, user, password):
    choice = input('请输入操作类型 (add/del): ')
    if choice == 'add':
        interface_name = input("请输入接口名称 (例如 GigabitEthernet1/0/1): ")
        vlan_id = input("请输入 VLAN ID: ")
        rpc_xml = create_interface_vlan_rpc(interface_name, vlan_id)
        operation = '添加接口到VLAN'
    elif choice == 'del':
        interface_name = input("请输入需要从 VLAN 中删除的接口名称: ")
        rpc_xml = delete_interface_from_vlan_rpc(interface_name)
        operation = '从VLAN删除接口'
    else:
        print('无效输入')
        return

    with manager.connect(host=host, port=port, username=user,
                         password=password, hostkey_verify=False,
                         device_params={'name': 'h3c'}, timeout=30, allow_agent=False, look_for_keys=False) as m:
        rpc_obj = m.edit_config(target='running', config=rpc_xml)
        _check_response(rpc_obj, operation)

def vlan_int_mgmt():
    vlan_int_mgmt_temp(hostname, port, username, password)

# if __name__ == '__main__':
#     vlan_int_mgmt(hostname, port, username, password)