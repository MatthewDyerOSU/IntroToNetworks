import sys
import json
import math  # If you want to use math.inf for infinity
import netfuncs

"""
Functions from netfuncs:
ipv4_to_value(ipv4_addr)
value_to_ipv4(addr)
get_subnet_mask_value(slash)
ips_same_subnet(ip1, ip2, slash)
get_network(ip_value, netmask)
find_router_for_ip(routers, ip)
"""

def setup(src_ip, dest_ip, routers):
    '''
    Initialization: create a set of all the routers still to be visited.
    Create a distance dictionary with all routers as keys and values set 
    to infinity. Create a parent dictionary with all routers as keys and
    values set to None. Get the first and final routers for the path.
    Returns the set, both dictionaries, and the first and final routers.
    '''
    to_visit = set(routers.keys())
    distance = {node: math.inf for node in routers}
    parent = {node: None for node in routers}
    first_router = netfuncs.find_router_for_ip(routers, src_ip)
    final_router = netfuncs.find_router_for_ip(routers, dest_ip)
    return to_visit, distance, parent, first_router, final_router

def find_closest_router(current_node, distance, to_visit):
    '''
    Finds the closest router that still needs to be visitied and returns it.
    '''
    val = math.inf
    for node in distance:
        if distance[node] < val:
            if node in to_visit:
                current_node = node
                val = distance[node]
    return current_node

def relax(current_node, routers, to_visit, parent, distance):
    '''
    For each one of the current node's neighbors still in to_visit, 
    compute the distance from the starting node to the neighbor (the distance
    of the current node plus the edge weight to the neighbor). If the
    computed distance is less than the neighbor's current value in distance, 
    then set the neighbor's value in distance to the computed distance, then
    set the neighbor's parent to the current node.
    '''
    # For each one of the current node's neighbors still in to_visit
    for neighbor in routers[current_node]["connections"]:
        if neighbor in to_visit:
            # Compute the distance from the starting node to the neighbor.
            # This is the distance of the current node plus the edge weight to the neighbor
            ad = routers[current_node]["connections"][neighbor]["ad"]
            computed_distance = distance[current_node] + ad
            # If the computed distance is less than the neighbor's current value in distance:
            if computed_distance < distance[neighbor]:
                # Set the neighbor's value in distance to the computed distance
                distance[neighbor] = computed_distance
                # Set the neighbor's parent to the current node
                parent[neighbor] = current_node


def get_path(starting_node, destination_node, parent):
    '''
    Takes a starting node and destination node, and creates a list of all
    parent nodes leading backwards from the destination to the start. Then
    the list is reversed and returned.
    '''
    path = []
    current_node = destination_node
    while current_node != starting_node:
        path.append(current_node)
        current_node = parent[current_node]
    path.append(starting_node)
    return path


# def dijkstras_shortest_path(routers, src_ip, dest_ip):
def dijkstras_shortest_path(routers, dest_ip, src_ip):
    """
    This function takes a dictionary representing the network, a source
    IP, and a destination IP, and returns a list with all the routers
    along the shortest path.

    The source and destination IPs are **not** included in this path.

    Note that the source IP and destination IP will probably not be
    routers! They will be on the same subnet as the router. You'll have
    to search the routers to find the one on the same subnet as the
    source IP. Same for the destination IP. [Hint: make use of your
    find_router_for_ip() function from the last project!]

    The dictionary keys are router IPs, and the values are dictionaries
    with a bunch of information, including the routers that are directly
    connected to the key.

    This partial example shows that router `10.34.98.1` is connected to
    three other routers: `10.34.166.1`, `10.34.194.1`, and `10.34.46.1`:

    {
        "10.34.98.1": {
            "connections": {
                "10.34.166.1": {
                    "netmask": "/24",
                    "interface": "en0",
                    "ad": 70
                },
                "10.34.194.1": {
                    "netmask": "/24",
                    "interface": "en1",
                    "ad": 93
                },
                "10.34.46.1": {
                    "netmask": "/24",
                    "interface": "en2",
                    "ad": 64
                }
            },
            "netmask": "/24",
            "if_count": 3,
            "if_prefix": "en"
        },
        ...

    The "ad" (Administrative Distance) field is the edge weight for that
    connection.

    **Strong recommendation**: make functions to do subtasks within this
    function. Having it all built as a single wall of code is a recipe
    for madness.
    """   
    

    to_visit, distance, parent, first_router, final_router = setup(src_ip, dest_ip, routers)
    
    if first_router == final_router:
        return []
    
    distance[first_router] = 0

    current_node = first_router

    while to_visit:
        current_node = find_closest_router(current_node, distance, to_visit)
                    
        if current_node == final_router:
            break

        # remove the current node from the to_visit set
        to_visit.remove(current_node)

        relax(current_node, routers, to_visit, parent, distance)

    path = get_path(first_router, final_router, parent)
    return path

#------------------------------
# DO NOT MODIFY BELOW THIS LINE
#------------------------------
def read_routers(file_name):
    with open(file_name) as fp:
        data = fp.read()

    return json.loads(data)

def find_routes(routers, src_dest_pairs):
    for src_ip, dest_ip in src_dest_pairs:
        path = dijkstras_shortest_path(routers, src_ip, dest_ip)
        print(f"{src_ip:>15s} -> {dest_ip:<15s}  {repr(path)}")

def usage():
    print("usage: dijkstra.py infile.json", file=sys.stderr)

def main(argv):
    try:
        router_file_name = argv[1]
    except:
        usage()
        return 1

    json_data = read_routers(router_file_name)

    routers = json_data["routers"]
    routes = json_data["src-dest"]

    find_routes(routers, routes)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
    
