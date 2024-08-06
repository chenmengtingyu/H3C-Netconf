import sys
import logging
from ncclient import manager
from ncclient import operations
from ncclient.transport.errors import SSHError
from ncclient.operations.rpc import RPCError
import xml.etree.ElementTree as ET

log = logging.getLogger(__name__)

hostname = '192.168.1.1'
port = 830
username = 'admin'
password = 'wq20040903'

# 获取接口信息的 RPC 报文
IF_GET_RPC = """
<top xmlns="http://www.h3c.com/netconf/data:1.0">
    <Ifmgr>
        <Interfaces>
            <Interface></Interface>
        </Interfaces>
    </Ifmgr>
</top>
"""

IF_GET_CONFIG_RPC = """
<top xmlns="http://www.h3c.com/netconf/config:1.0">
    <Ifmgr>
        <Interfaces>
            <Interface></Interface>
        </Interfaces>
    </Ifmgr>
</top>
"""

def get_int_all_temp(hostname, port, username, password):
    try:
        with manager.connect(host=hostname, port=port, username=username,
                             password=password, hostkey_verify=False,
                             device_params={'name': 'h3c'}, timeout=30, allow_agent=False, look_for_keys=False) as m:
            if m.connected:
                print("连接成功")
                n = m._session.id
                print('This session id is %s' % n)
                # 发送 get 操作 RPC 请求，并将回复报文写入到 xml 文件中
                get_reply = m.get(("subtree", IF_GET_RPC)).data_xml
                result = ET.fromstring(get_reply)
                for interface in result.findall(".//{http://www.h3c.com/netconf/data:1.0}Interface"):
                    index = interface.find("{http://www.h3c.com/netconf/data:1.0}IfIndex").text
                    name = interface.find("{http://www.h3c.com/netconf/data:1.0}Name").text
                    description = interface.find("{http://www.h3c.com/netconf/data:1.0}Description").text
                    admin_status = interface.find("{http://www.h3c.com/netconf/data:1.0}AdminStatus").text
                    oper_status = interface.find("{http://www.h3c.com/netconf/data:1.0}OperStatus").text
                    mac = interface.find("{http://www.h3c.com/netconf/data:1.0}MAC").text
                    pvid = interface.find("{http://www.h3c.com/netconf/data:1.0}PVID").text
                    
                    print(f"Interface Index: {index}")
                    print(f"Name: {name}")
                    print(f"Description: {description}")
                    print(f"Admin Status: {'Up' if admin_status == '1' else 'Down'}")
                    print(f"Operational Status: {'Up' if oper_status == '1' else 'Down'}")
                    print(f"MAC Address: {mac}")
                    print(f"PVID: {pvid}")
                    print("-----")
                # with open(f"{hostname}_get.xml", 'w') as f:
                #     f.write(get_reply)
                # 通过 get-config 接口发送 get-config 操作 RPC 请求，并将回复报文写入到 xml 文件中
                get_reply2 = m.get(("subtree", IF_GET_CONFIG_RPC)).data_xml
                result2 = ET.fromstring(get_reply2)
                for interface in result2.findall(".//{http://www.h3c.com/netconf/data:1.0}Interface"):
                    index = interface.find("{http://www.h3c.com/netconf/data:1.0}IfIndex").text
                    name = interface.find("{http://www.h3c.com/netconf/data:1.0}Name").text
                    description = interface.find("{http://www.h3c.com/netconf/data:1.0}Description").text
                    admin_status = interface.find("{http://www.h3c.com/netconf/data:1.0}AdminStatus").text
                    oper_status = interface.find("{http://www.h3c.com/netconf/data:1.0}OperStatus").text
                    mac = interface.find("{http://www.h3c.com/netconf/data:1.0}MAC").text
                    pvid = interface.find("{http://www.h3c.com/netconf/data:1.0}PVID").text
                    
                    print(f"Interface Index: {index}")
                    print(f"Name: {name}")
                    print(f"Description: {description}")
                    print(f"Admin Status: {'Up' if admin_status == '1' else 'Down'}")
                    print(f"Operational Status: {'Up' if oper_status == '1' else 'Down'}")
                    print(f"MAC Address: {mac}")
                    print(f"PVID: {pvid}")
                    print("-----")
                # with open(f"{hostname}_getconfig.xml", 'w') as f:
                #     f.write(get_reply2)
                # 通过 get-config 接口发送 get-config 操作 RPC 请求，并将回复报文写入到 xml 文件中
                c = m.get_config(source='running', filter=('subtree', IF_GET_CONFIG_RPC)).data_xml
                with open(f"{hostname}_getconfig2.xml", 'w') as f:
                    f.write(c)
            else:
                print("连接失败")
    except (SSHError, RPCError, AttributeError) as e:
        # print(f"连接错误：{str(e)}")
        print('')

def get_int_all():
    get_int_all_temp(hostname, port, username, password)


# if __name__ == '__main__':
#     get_int_all(hostname, port, username, password)
