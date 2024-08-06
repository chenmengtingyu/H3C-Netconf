from ncclient import manager
from ncclient.xml_ import to_ele

host = {
    'host': '192.168.1.1',
    'username': 'admin',
    'password': 'wq20040903',
    'port': 830,
    'device_params': {'name': 'h3c'},
}

def create_iface_request():
    return """
    <top xmlns="http://www.h3c.com/netconf/data:1.0">
        <Ifmgr>
            <Interfaces>
                <Interface>
                    <Name></Name>
                    <InetAddressIPV4></InetAddressIPV4>
                    <AdminStatus></AdminStatus>
                </Interface>
            </Interfaces>
        </Ifmgr>
    </top>
    """

def get_iface_info(host):
    with manager.connect(**host, hostkey_verify=False, look_for_keys=False, allow_agent=False) as conn:
        iface_request = to_ele(create_iface_request())
        response = conn.get(('subtree', iface_request))
        return response.xml

def process_interfaces(xml_data):
    from xml.etree import ElementTree as ET
    
    namespaces = {
        'nc': 'urn:ietf:params:xml:ns:netconf:base:1.0',
        'h3c': 'http://www.h3c.com/netconf/data:1.0'
    }

    root = ET.fromstring(xml_data)
    output_text = []
    for interface in root.findall(".//h3c:Interface", namespaces=namespaces):
        if_index = interface.find('h3c:IfIndex', namespaces=namespaces).text
        name = interface.find('h3c:Name', namespaces=namespaces).text
        admin_status = interface.find('h3c:AdminStatus', namespaces=namespaces).text
        ip_element = interface.find('h3c:InetAddressIPV4', namespaces=namespaces)
        ip_address = ip_element.text if ip_element is not None else None

        line = f"Interface Index: {if_index}, Name: {name}, Admin Status: {'Up' if admin_status == '1' else 'Down'}"
        if ip_address:
            line += f", IP Address: {ip_address}"
        output_text.append(line)
    
    return output_text

def get_int_info():
    xml_response = get_iface_info(host)
    formatted_text = process_interfaces(xml_response)
    for line in formatted_text:
        print(line)

# if __name__ == '__main__':
#     get_int_info()
