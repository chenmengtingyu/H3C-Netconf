from port.get_int import get_int_info
from port.get_int_all import get_int_all
from port.mgmt_port import int_mgmt
from port.port_speed_conf import port_speed_mgmt

from route.delete_static_route import delete_static_route
from route.get_ip_routing_table import get_ip_routing_table
from route.get_ospf import get_ospf
from route.get_rip import get_rip
from route.get_static_route_table import get_static_routing_table
from route.ospf_conf import ospf_conf
from route.rip_conf import rip_conf
from route.static_route import static_route_config

from vlan.add_del_port_to_vlan import vlan_int_mgmt
from vlan.get_vlan_info import get_vlan_info
from vlan.vlan_add_del import add_del_vlan
from vlan.vlanip_conf import vlan_ip_config

# ANSI Escape Sequences for colors
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
RESET = "\033[0m"

# host = input('请输入IP地址:')
# port = input('请输入端口号:')
# username = input('请输入用户名:')
# password = input('请输入密码:')

host = '192.168.1.1'
port_num = 830
username = 'admin'
password = 'admin'

def main():
    while True:
        print(f'{GREEN}请输入操作:{RESET}')
        print(f'{GREEN}1.接口操作{RESET}')
        print(f'{GREEN}2.路由操作{RESET}')
        print(f'{GREEN}3.VLAN操作{RESET}')
        print(f'{GREEN}4.退出程序{RESET}')
        choice = input(f'{YELLOW}请输入你的操作:{RESET}')
        if choice == '1':
            while True:
                print(f'{GREEN}1.查看接口信息{RESET}')
                print(f'{GREEN}2.查看接口详细信息{RESET}')
                print(f'{GREEN}3.接口开关管理{RESET}')
                print(f'{GREEN}4.接口速率管理{RESET}')
                print(f'{GREEN}5.返回上一级操作{RESET}')
                choice_1 = input(f'{YELLOW}请输入你的操作:{RESET}')
                if choice_1 == '1':
                    get_int_info()
                elif choice_1 == '2':
                    get_int_all()
                elif choice_1 == '3':
                    int_mgmt()
                elif choice_1 == '4':
                    port_speed_mgmt()
                elif choice_1 == '5':
                    break
        if choice == '2':
            while True:
                print(f'{GREEN}1.配置静态路由{RESET}')
                print(f'{GREEN}2.删除所有静态路由{RESET}')
                print(f'{GREEN}3.查看静态路由表{RESET}')
                print(f'{GREEN}4.配置RIP{RESET}')
                print(f'{GREEN}5.查看RIP信息{RESET}')
                print(f'{GREEN}6.配置OSPF{RESET}')
                print(f'{GREEN}7.查看OSPF信息{RESET}')
                print(f'{GREEN}8.查看IP路由表{RESET}')
                print(f'{GREEN}9.返回上一级操作{RESET}')
                choice_2 = input(f'{YELLOW}请输入你的操作:{RESET}')
                if choice_2 == '1':
                    static_route_config()
                elif choice_2 == '2':
                    delete_static_route()
                elif choice_2 == '3':
                    get_static_routing_table()
                elif choice_2 == '4':
                    rip_conf()
                elif choice_2 == '5':
                    get_rip()
                elif choice_2 == '6':
                    ospf_conf()
                elif choice_2 == '7':
                    get_ospf()
                elif choice_2 == '8':
                    get_ip_routing_table()
                elif choice_2 == '9':
                    break
        if choice == '3':
            while True:
                print(f'{GREEN}1.添加或删除VLAN{RESET}')
                print(f'{GREEN}2.VLAN接口配置IP地址{RESET}')
                print(f'{GREEN}3.将接口加入到或从VLAN删除{RESET}')
                print(f'{GREEN}4.查看VLAN信息{RESET}')
                print(f'{GREEN}5.返回上一级操作{RESET}')
                choice_3 = input(f'{YELLOW}请输入你的操作:{RESET}')
                if choice_3 == '1':
                    add_del_vlan()
                elif choice_3 == '2':
                    vlan_ip_config()
                elif choice_3 == '3':
                    vlan_int_mgmt()
                elif choice_3 == '4':
                    get_vlan_info()
                elif choice_3 == '5':
                    break
        if choice == '4':
            break

if __name__ == '__main__':
    main()
