import sys
import json

def ipv4_to_value(ipv4_addr):
    """
    Convert a dots-and-numbers IP address to a single 32-bit numeric
    value of integer type. Returns an integer type.

    Example:

    ipv4_addr: "255.255.0.0"
    return:    4294901760  (Which is 0xffff0000 hex)

    ipv4_addr: "1.2.3.4"
    return:    16909060  (Which is 0x01020304 hex)
    """
    values = ipv4_addr.split(".")
    hex_string = ""
    for val in values:
        hex_string += format(int(val), '02x')
    dec_string = int(hex_string, 16)
    return dec_string

def value_to_ipv4(addr):
    """
    Convert a single 32-bit numeric value of integer type to a
    dots-and-numbers IP address. Returns a string type.

    Example:

    There is only one input value, but it is shown here in 3 bases.

    addr:   0xffff0000 0b11111111111111110000000000000000 4294901760
    return: "255.255.0.0"

    addr:   0x01020304 0b00000001000000100000001100000100 16909060
    return: "1.2.3.4"
    """
    addr_string = ""
    hex_val = format(addr, '08x')
    for i in range(0, len(hex_val), 2):
        addr_string += str(int(hex_val[i:i+2], 16))
        addr_string += "."

    return addr_string[:-1]

def get_subnet_mask_value(slash):
    """
    Given a subnet mask in slash notation, return the value of the mask
    as a single number of integer type. The input can contain an IP
    address optionally, but that part should be discarded.

    Returns an integer type.

    Example:

    There is only one return value, but it is shown here in 3 bases.

    slash:  "/16"
    return: 0xffff0000 0b11111111111111110000000000000000 4294901760

    slash:  "10.20.30.40/23"
    return: 0xfffffe00 0b11111111111111111111111000000000 4294966784
    """

    offset = slash.find("/")
    if offset < 0:
        print("Argument did not contain a '/'")
        exit(1)
    val = int(slash[offset+1:])
    bin_val = ((1 << val) - 1) << (32 - val)
    return bin_val

def ips_same_subnet(ip1, ip2, slash):
    """
    Given two dots-and-numbers IP addresses and a subnet mask in slash
    notation, return true if the two IP addresses are on the same
    subnet.

    Returns a boolean.

    FOR FULL CREDIT: this must use your get_subnet_mask_value() and
    ipv4_to_value() functions. Don't do it with pure string
    manipulation.

    This needs to work with any subnet from /1 to /31

    Example:

    ip1:    "10.23.121.17"
    ip2:    "10.23.121.225"
    slash:  "/23"
    return: True
    
    ip1:    "10.23.230.22"
    ip2:    "10.24.121.225"
    slash:  "/16"
    return: False
    """
    ip_val_1 = ipv4_to_value(ip1)
    ip_val_2 = ipv4_to_value(ip2)

    mask = get_subnet_mask_value(slash)

    subnet_1 = ip_val_1 & mask
    subnet_2 = ip_val_2 & mask

    return subnet_1 == subnet_2

def get_network(ip_value, netmask):
    """
    Return the network portion of an address value as integer type.

    Example:

    ip_value: 0x01020304
    netmask:  0xffffff00
    return:   0x01020300
    """
    return ip_value & netmask

def find_router_for_ip(routers, ip):
    """
    Search a dictionary of routers (keyed by router IP) to find which
    router belongs to the same subnet as the given IP.

    Return None if no routers are on the same subnet as the given IP.

    FOR FULL CREDIT: you must do this by calling your ips_same_subnet()
    function.

    Example:

    [Note there will be more data in the routers dictionary than is
    shown here--it can be ignored for this function.]

    routers: {
        "1.2.3.1": {
            "netmask": "/24"
        },
        "1.2.4.1": {
            "netmask": "/24"
        }
    }
    ip: "1.2.3.5"
    return: "1.2.3.1"


    routers: {
        "1.2.3.1": {
            "netmask": "/24"
        },
        "1.2.4.1": 
            "netmask": "/24"
        }
    }
    ip: "1.2.5.6"
    return: None
    """
    for key in routers:
        found = ips_same_subnet(key, ip, routers[key]["netmask"])
        if found:
            return key
    return None
# Uncomment this code to have it run instead of the real main.
# Be sure to comment it back out before you submit!

# def my_tests():
#     print("-------------------------------------")
#     print("This is the result of my custom tests")
#     print("-------------------------------------")

#     print(hex(get_subnet_mask_value("192.168.1.12/24")))
#     dec_val = ipv4_to_value("10.100.30.90")
#     print(hex(dec_val))
#     print(dec_val)
#     print(bin(dec_val))

#     dec_value = ipv4_to_value("255.255.0.0")
#     print(f'Decimal Value: {dec_value}')
#     dec_value = ipv4_to_value("1.2.3.4")
#     print(f'Decimal Value: {dec_value}')
#     dec_value = ipv4_to_value("192.168.0.1")
#     print(f'Decimal Value: {dec_value}')
#     dec_value = ipv4_to_value("192.0.2.37")
#     print(hex(dec_value))

#     addr = value_to_ipv4(3405804026)
#     print(addr)
#     addr = value_to_ipv4(0b11111111111111110000000000000000)
#     print(f'Address: {addr}')
#     addr = value_to_ipv4(16909060)
#     print(f'Address: {addr}')
#     addr = value_to_ipv4(0x01020304)
#     print(f'Address: {addr}')
#     addr = value_to_ipv4(3232235521)
#     print(f'Address: {addr}')

#     mask_val = get_subnet_mask_value("10.20.30.40/23")
#     print(f'Subnet Mask Val: {mask_val}')
#     mask_val = get_subnet_mask_value("/16")
#     print(f'Subnet Mask Val: {mask_val}')
    
#     equal_or_not = ips_same_subnet("10.23.121.17", "10.23.121.225", "/23")
#     print(equal_or_not)
#     equal_or_not = ips_same_subnet("10.23.230.22", "10.24.121.225", "/16")
#     print(equal_or_not)
   
#     network = get_network(0x01020304, 0xffffff00)
#     print(f'Network: {hex(network)}')

#     routers = {
#         "1.2.3.1": {
#             "netmask": "/24"
#         },
#         "1.2.4.1": {
#             "netmask": "/24"
#         }
#     }

#     result = find_router_for_ip(routers, "1.2.3.5")
#     print(f'Result: {result}')
#     result = find_router_for_ip(routers, "1.2.5.6")
#     print(f'Result: {result}')

## -------------------------------------------
## Do not modify below this line
##
## But do read it so you know what it's doing!
## -------------------------------------------

def usage():
    print("usage: netfuncs.py infile.json", file=sys.stderr)

def read_routers(file_name):
    with open(file_name) as fp:
        json_data = fp.read()
        
    return json.loads(json_data)

def print_routers(routers):
    print("Routers:")

    routers_list = sorted(routers.keys())

    for router_ip in routers_list:

        # Get the netmask
        slash_mask = routers[router_ip]["netmask"]
        netmask_value = get_subnet_mask_value(slash_mask)
        netmask = value_to_ipv4(netmask_value)

        # Get the network number
        router_ip_value = ipv4_to_value(router_ip)
        network_value = get_network(router_ip_value, netmask_value)
        network_ip = value_to_ipv4(network_value)

        print(f" {router_ip:>15s}: netmask {netmask}: " \
            f"network {network_ip}")

def print_same_subnets(src_dest_pairs):
    print("IP Pairs:")

    src_dest_pairs_list = sorted(src_dest_pairs)

    for src_ip, dest_ip in src_dest_pairs_list:
        print(f" {src_ip:>15s} {dest_ip:>15s}: ", end="")

        if ips_same_subnet(src_ip, dest_ip, "/24"):
            print("same subnet")
        else:
            print("different subnets")

def print_ip_routers(routers, src_dest_pairs):
    print("Routers and corresponding IPs:")

    all_ips = sorted(set([i for pair in src_dest_pairs for i in pair]))

    router_host_map = {}

    for ip in all_ips:
        router = str(find_router_for_ip(routers, ip))
        
        if router not in router_host_map:
            router_host_map[router] = []

        router_host_map[router].append(ip)

    for router_ip in sorted(router_host_map.keys()):
        print(f" {router_ip:>15s}: {router_host_map[router_ip]}")

def main(argv):
    if "my_tests" in globals() and callable(my_tests):
        my_tests()
        return 0

    try:
        router_file_name = argv[1]
    except:
        usage()
        return 1

    json_data = read_routers(router_file_name)

    routers = json_data["routers"]
    src_dest_pairs = json_data["src-dest"]

    print_routers(routers)
    print()
    print_same_subnets(src_dest_pairs)
    print()
    print_ip_routers(routers, src_dest_pairs)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
    
