from ncclient import manager
from ncclient.xml_ import to_ele

hostname = '192.168.1.1'
port = 830
username = 'admin'
password = 'wq20040903'

def create_vlan_ip_command(vlan_id, ip_address, subnet_mask):
    return f"""
    <CLI>
        <Configuration>
            interface Vlan-interface{vlan_id}
            ip address {ip_address} {subnet_mask}
        </Configuration>
    </CLI>
    """

def vlan_ip_config(host, port, username, password, vlan_id, ip_address, subnet_mask):
    with manager.connect(host=host, port=port, username=username,
                         password=password, hostkey_verify=False,
                         device_params={'name': 'h3c'}, timeout=30, allow_agent=False, look_for_keys=False) as m:
        # 生成并发送配置命令
        rpc_command = to_ele(create_vlan_ip_command(vlan_id, ip_address, subnet_mask))
        response = m.dispatch(rpc_command)
        print(response.xml)

# def vlan_ip_config():
#     vlan_id = input('请输入 VLAN ID: ')
#     ip_address = input('请输入 IP 地址: ')
#     subnet_mask = input('请输入子网掩码: ')
#     assign_ip_to_vlan(hostname, port, username, password, vlan_id, ip_address, subnet_mask)

# if __name__ == '__main__':
#     vlan_ip_config()
