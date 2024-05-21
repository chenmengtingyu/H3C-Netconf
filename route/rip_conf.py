from ncclient import manager
from ncclient.xml_ import to_ele

hostname = '192.168.1.1'
port = 830
username = 'admin'
password = 'admin'

def create_rip_configuration_commands(networks):
    commands = """
    <CLI>
        <Configuration>
            rip 1
            """
    for net in networks:
        commands += f"""
            network {net}
            """
    commands += """
            exit
        </Configuration>
    </CLI>
    """
    return commands

def configure_rip(host, port, username, password, networks):
    with manager.connect(host=host, port=port, username=username,
                         password=password, hostkey_verify=False,
                         device_params={'name': 'h3c'}, timeout=30, allow_agent=False, look_for_keys=False) as m:
        # 生成并发送RIP配置命令
        rip_config_command = to_ele(create_rip_configuration_commands(networks))
        response = m.dispatch(rip_config_command)
        print(response.xml)

def rip_conf():
    networks = input('请输入要宣告的网络地址，用逗号分隔 (如 192.168.1.0,192.168.2.0): ').split(',')
    configure_rip(hostname, port, username, password, networks)

# if __name__ == '__main__':
#     rip_conf()
