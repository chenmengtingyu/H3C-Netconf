from ncclient import manager
from ncclient.xml_ import to_ele

hostname = '192.168.1.1'
port = 830
username = 'admin'
password = 'wq20040903'

def display_vlan_info():
    # 移除 error-when-rollback 属性
    return """
    <CLI>
        <Configuration exec-use-channel="false">
            display vlan all
        </Configuration>
    </CLI>
    """

def get_vlan_info_temp(host, port, username, password):
    with manager.connect(host=host, port=port, username=username,
                         password=password, hostkey_verify=False,
                         device_params={'name': 'h3c'}, timeout=30, allow_agent=False, look_for_keys=False) as m:
        # 使用to_ele函数来将XML字符串转换为元素
        rpc_command = to_ele(display_vlan_info())
        response = m.dispatch(rpc_command)
        print(response.xml)

def get_vlan_info():
    get_vlan_info_temp(hostname, port, username, password)

# if __name__ == '__main__':
#     get_vlan_info(hostname, port, username, password)
