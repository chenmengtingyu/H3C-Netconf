from ncclient import manager
from ncclient.xml_ import to_ele

hostname = '192.168.1.1'
port = 830
username = 'admin'
password = 'admin'

def create_interface_speed_command(interface_name, speed):
    return f"""
    <CLI>
        <Configuration>
            interface {interface_name}
            speed {speed}
        </Configuration>
    </CLI>
    """

def configure_interface_speed(host, port, username, password, interface_name, speed):
    with manager.connect(host=host, port=port, username=username,
                         password=password, hostkey_verify=False,
                         device_params={'name': 'h3c'}, timeout=30, allow_agent=False, look_for_keys=False) as m:
        # 生成并发送设置速率的命令
        speed_config_command = to_ele(create_interface_speed_command(interface_name, speed))
        response = m.dispatch(speed_config_command)
        print(response.xml)

def port_speed_mgmt():
    interface_name = input('请输入接口名称: ')
    speed = input('请输入速率设置(如 1000表示1Gbps): ')
    configure_interface_speed(hostname, port, username, password, interface_name, speed)

# if __name__ == '__main__':
#     port_speed_mgmt()
