from ncclient import manager
from ncclient.xml_ import to_ele

hostname = '192.168.1.1'
port = 830
username = 'admin'
password = 'admin'

def create_ospf_configuration_commands(process_id, area_id, networks):
    commands = f"""
    <CLI>
        <Configuration>
            ospf {process_id}
            """
    for net in networks:
        commands += f"""
            area {area_id}
            network {net}
            """
    commands += """
            exit
        </Configuration>
    </CLI>
    """
    return commands

def configure_ospf(host, port, username, password, process_id, area_id, networks):
    with manager.connect(host=host, port=port, username=username,
                         password=password, hostkey_verify=False,
                         device_params={'name': 'h3c'}, timeout=30, allow_agent=False, look_for_keys=False) as m:
        # 生成并发送OSPF配置命令
        ospf_config_command = to_ele(create_ospf_configuration_commands(process_id, area_id, networks))
        response = m.dispatch(ospf_config_command)
        print(response.xml)

def ospf_conf():
    process_id = input('请输入 OSPF 进程 ID: ')
    area_id = input('请输入区域 ID: ')
    networks = input('请输入要宣告的网络地址和掩码反码，用逗号分隔: ').split(',')
    configure_ospf(hostname, port, username, password, process_id, area_id, networks)

# if __name__ == '__main__':
#     ospf_conf()
