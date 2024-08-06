from ncclient import manager
from ncclient.xml_ import to_ele

hostname = '192.168.1.1'
port = 830
username = 'admin'
password = 'wq20040903'

def create_static_route_command(destination, mask, next_hop):
    return f"""
    <CLI>
        <Configuration>
            ip route-static {destination} {mask} {next_hop}
        </Configuration>
    </CLI>
    """

def static_route_config(host, port, username, password, destination, mask, next_hop):
    with manager.connect(host=host, port=port, username=username,
                         password=password, hostkey_verify=False,
                         device_params={'name': 'h3c'}, timeout=30, allow_agent=False, look_for_keys=False) as m:
        # 生成并发送配置命令
        rpc_command = to_ele(create_static_route_command(destination, mask, next_hop))
        response = m.dispatch(rpc_command)
        print(response.xml)

# def static_route_config():
#     destination = input('请输入目的网络地址（如 192.168.30.0）: ')
#     mask = input('请输入网络掩码长度（如 24）: ')
#     next_hop = input('请输入下一跳地址（如 192.168.20.1）: ')
#     configure_static_route(hostname, port, username, password, destination, mask, next_hop)

# if __name__ == '__main__':
#     static_route_config()
