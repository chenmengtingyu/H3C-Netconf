import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext

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

from vlan.add_del_port_to_vlan import vlan_int_mgmt, create_interface_vlan_rpc, delete_interface_from_vlan_rpc
from vlan.get_vlan_info import get_vlan_info
from vlan.vlan_add_del import add_del_vlan, create_vlan_rpc, delete_vlan_rpc
from vlan.vlanip_conf import vlan_ip_config

class NetworkManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Manager")
        
        self.host = tk.StringVar()
        self.port_num = tk.StringVar()
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        
        self.create_login_widgets()

    def create_login_widgets(self):
        login_frame = ttk.LabelFrame(self.root, text="Login Details")
        login_frame.grid(row=0, column=0, padx=101, pady=101, sticky="ew")
        
        ttk.Label(login_frame, text="IP Address:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(login_frame, textvariable=self.host).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(login_frame, text="Port:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(login_frame, textvariable=self.port_num).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(login_frame, text="Username:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(login_frame, textvariable=self.username).grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(login_frame, text="Password:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(login_frame, textvariable=self.password, show="*").grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Button(login_frame, text="Login", command=self.create_main_menu).grid(row=4, columnspan=2, pady=101)

    def create_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        main_menu_frame = ttk.LabelFrame(self.root, text="Main Menu")
        main_menu_frame.grid(row=0, column=0, padx=101, pady=101, sticky="ew")
        
        ttk.Button(main_menu_frame, text="Interface Operations", command=self.create_interface_menu).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        ttk.Button(main_menu_frame, text="Routing Operations", command=self.create_routing_menu).grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        ttk.Button(main_menu_frame, text="VLAN Operations", command=self.create_vlan_menu).grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        ttk.Button(main_menu_frame, text="Exit", command=self.root.quit).grid(row=3, column=0, padx=5, pady=5, sticky="ew")

    def create_interface_menu(self):
        self.create_sub_menu("Interface Operations", [
            ("View Interface Info", self.get_int_info, []),
            ("View Detailed Interface Info", self.get_int_all, []),
            ("Manage Interface State", self.int_mgmt, ["Interface Name", "Action (enable/disable)"]),
            ("Manage Port Speed", self.port_speed_mgmt, ["Interface Name", "Speed (e.g., 1000 for 1Gbps)"])
        ])

    def create_routing_menu(self):
        self.create_sub_menu("Routing Operations", [
            ("Configure Static Route", self.static_route_config, ["Destination Network", "Network Mask Length", "Next Hop"]),
            ("Delete All Static Routes", self.delete_static_route, []),
            ("View Static Routing Table", self.get_static_routing_table, []),
            ("Configure RIP", self.rip_conf, ["Networks (comma separated)"]),
            ("View RIP Info", self.get_rip, []),
            ("Configure OSPF", self.ospf_conf, ["Process ID", "Area ID", "Networks (comma separated)"]),
            ("View OSPF Info", self.get_ospf, []),
            ("View IP Routing Table", self.get_ip_routing_table, [])
        ])

    def create_vlan_menu(self):
        self.create_sub_menu("VLAN Operations", [
            ("Add/Delete VLAN", self.add_del_vlan, ["Action (add/del)", "VLAN ID", "VLAN Name", "VLAN Description"]),
            ("Configure VLAN IP Address", self.vlan_ip_config, ["VLAN ID", "IP Address", "Subnet Mask"]),
            ("Manage Interface in VLAN", self.vlan_int_mgmt, ["Action (add/del)", "Interface Name", "VLAN ID"]),
            ("View VLAN Info", self.get_vlan_info, [])
        ])

    def create_sub_menu(self, title, operations):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        sub_menu_frame = ttk.LabelFrame(self.root, text=title)
        sub_menu_frame.grid(row=0, column=0, padx=101, pady=101, sticky="ew")
        
        for idx, (op_name, op_func, inputs) in enumerate(operations):
            ttk.Button(sub_menu_frame, text=op_name, command=lambda f=op_func, i=inputs: self.create_operation_frame(f, i, self.create_sub_menu, title, operations)).grid(row=idx, column=0, padx=5, pady=5, sticky="ew")
        
        ttk.Button(sub_menu_frame, text="Back", command=self.create_main_menu).grid(row=len(operations), column=0, padx=5, pady=5, sticky="ew")

    def create_operation_frame(self, operation, inputs, back_function, *back_args):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        operation_frame = ttk.LabelFrame(self.root, text="Operation")
        operation_frame.grid(row=0, column=0, padx=101, pady=101, sticky="ew")

        input_vars = []
        for idx, input_label in enumerate(inputs):
            ttk.Label(operation_frame, text=input_label + ":").grid(row=idx, column=0, padx=5, pady=5, sticky="e")
            var = tk.StringVar()
            input_vars.append(var)
            ttk.Entry(operation_frame, textvariable=var).grid(row=idx, column=1, padx=5, pady=5, sticky="ew")

        output_text = scrolledtext.ScrolledText(operation_frame, wrap=tk.WORD, width=50, height=15)
        output_text.grid(row=len(inputs), column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        def run_operation():
            output_text.delete(1.0, tk.END)
            try:
                params = [var.get() for var in input_vars]
                result = operation(*params)
                if result:
                    output_text.insert(tk.END, result + "\n")
            except Exception as e:
                output_text.insert(tk.END, str(e) + "\n")
        
        ttk.Button(operation_frame, text="Execute", command=run_operation).grid(row=len(inputs) + 1, column=0, padx=5, pady=5, sticky="ew")
        ttk.Button(operation_frame, text="Back", command=lambda: back_function(*back_args)).grid(row=len(inputs) + 1, column=1, padx=5, pady=5, sticky="ew")

    def get_int_info(self):
        return self.run_and_capture_output(get_int_info)

    def get_int_all(self):
        return self.run_and_capture_output(get_int_all)

    def int_mgmt(self, interface, action):
        int_mgmt(self.host.get(), self.port_num.get(), self.username.get(), self.password.get(), interface, action)
        return "Interface Management Completed"

    def port_speed_mgmt(self, interface, speed):
        port_speed_mgmt(self.host.get(), self.port_num.get(), self.username.get(), self.password.get(), interface, speed)
        return "Port Speed Management Completed"

    def static_route_config(self, destination, mask, next_hop):
        static_route_config(self.host.get(), self.port_num.get(), self.username.get(), self.password.get(), destination, mask, next_hop)
        return "Static Route Configuration Completed"

    # def delete_static_route(self):
    #     delete_static_route()
    #     return "All Static Routes Deleted"
    def delete_static_route(self):
        if messagebox.askyesno("确认删除", "确定要删除所有静态路由吗？"):
            delete_static_route()
            return "All Static Routes Deleted"
        else:
            return "Operation Cancelled"


    def get_static_routing_table(self):
        return self.run_and_capture_output(get_static_routing_table)

    def rip_conf(self, networks):
        networks = networks.split(',')
        rip_conf(self.host.get(), self.port_num.get(), self.username.get(), self.password.get(), networks)
        return "RIP Configuration Completed"

    def get_rip(self):
        return self.run_and_capture_output(get_rip)

    def ospf_conf(self, process_id, area_id, networks):
        networks = networks.split(',')
        ospf_conf(self.host.get(), self.port_num.get(), self.username.get(), self.password.get(), process_id, area_id, networks)
        return "OSPF Configuration Completed"

    def get_ospf(self):
        return self.run_and_capture_output(get_ospf)

    def get_ip_routing_table(self):
        return self.run_and_capture_output(get_ip_routing_table)

    def add_del_vlan(self, action, vlan_id, vlan_name=None, vlan_description=None):
        if action == 'add':
            vlan_rpc = create_vlan_rpc(vlan_id, vlan_name, vlan_description)
        elif action == 'del':
            vlan_rpc = delete_vlan_rpc(vlan_id)
        else:
            raise ValueError("Invalid action")
        add_del_vlan(self.host.get(), self.port_num.get(), self.username.get(), self.password.get(), vlan_rpc)
        return f"VLAN {action} operation completed"

    def vlan_ip_config(self, vlan_id, ip_address, subnet_mask):
        vlan_ip_config(self.host.get(), self.port_num.get(), self.username.get(), self.password.get(), vlan_id, ip_address, subnet_mask)
        return "VLAN IP Configuration Completed"

    def vlan_int_mgmt(self, action, interface_name, vlan_id):
        if action == 'add':
            rpc_xml = create_interface_vlan_rpc(interface_name, vlan_id)
        elif action == 'del':
            rpc_xml = delete_interface_from_vlan_rpc(interface_name)
        else:
            raise ValueError("Invalid action")
        vlan_int_mgmt(self.host.get(), self.port_num.get(), self.username.get(), self.password.get(), rpc_xml, action)
        return f"VLAN Interface {action} operation completed"

    def get_vlan_info(self):
        return self.run_and_capture_output(get_vlan_info)

    def run_and_capture_output(self, func, *args, **kwargs):
        import io
        import sys

        # Capture output
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()
        try:
            func(*args, **kwargs)
        finally:
            sys.stdout = old_stdout
        return buffer.getvalue()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkManagerApp(root)
    root.mainloop()
