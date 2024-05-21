from ncclient import manager
from ncclient.xml_ import to_ele

hostname = '192.168.1.1'
port = 830
username = 'admin'
password = 'admin'

def create_delete_all_static_routes_command():
    return """
    <CLI>
        <Configuration>
            delete static-routes all
        </Configuration>
    </CLI>
    """

def delete_all_static_routes(host, port, username, password):
    with manager.connect(host=host, port=port, username=username,
                         password=password, hostkey_verify=False,
                         device_params={'name': 'h3c'}, timeout=30, allow_agent=False, look_for_keys=False) as m:
        # 生成并发送删除命令
        rpc_command = to_ele(create_delete_all_static_routes_command())
        response = m.dispatch(rpc_command)
        print(response.xml)

def delete_static_route():
    confirm = input('确定要删除所有静态路由吗？(yes/no): ')
    if confirm.lower() == 'yes':
        delete_all_static_routes(hostname, port, username, password)
    else:
        print("操作已取消。")

# if __name__ == '__main__':
#     delete_static_route()
