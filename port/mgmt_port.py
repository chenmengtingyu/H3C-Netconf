from ncclient import manager
from ncclient.xml_ import to_ele

hostname = '192.168.1.1'
port = 830
username = 'admin'
password = 'admin'

def create_interface_command(interface_name, action):
    # 根据action参数，生成开启或关闭命令
    command = "undo shutdown" if action == "enable" else "shutdown"
    return f"""
    <CLI>
        <Configuration>
            interface {interface_name}
            {command}
        </Configuration>
    </CLI>
    """

def action(host, port, username, password, interface_name, action):
    with manager.connect(host=host, port=port, username=username,
                         password=password, hostkey_verify=False,
                         device_params={'name': 'h3c'}, timeout=30, allow_agent=False, look_for_keys=False) as m:
        # 生成并发送配置命令
        rpc_command = to_ele(create_interface_command(interface_name, action))
        response = m.dispatch(rpc_command)
        print(response.xml)

def int_mgmt():
    interface = input('请输入接口名称:')
    action_input = input('请输入操作(enable/disable):')
    if action_input not in ['enable', 'disable']:
        print("输入错误，只接受 'enable' 或 'disable' 作为命令。")
        return
    action(hostname, port, username, password, interface, action_input)

# if __name__ == '__main__':
#     int_mgmt()
