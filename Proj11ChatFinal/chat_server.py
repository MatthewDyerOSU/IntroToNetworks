import sys
import socket
import select
import json

# When server gets chat packet from one client, it rebroadcasts to all clients

# When a client connects/disconnects, this also is broadcasted

HOST = '127.0.0.1'

client_packet_buffers = {}

# Usage: python chat_server.py 3490
#   there is no default port, must be specified on command line
def usage():
    print("Usage: python server.py port")

def handle_hello_packet(sock, packet):
    global client_packet_buffers
    name = packet.get("nick")
    client_packet_buffers[sock]["nick"] = name
    return name

def handle_chat_packet(sock, packet):
    global client_packet_buffers
    type = packet.get("type")
    name = client_packet_buffers[sock]["nick"]
    message = packet.get("message")
    data = {
        "type": f"{type}",
        "nick": f"{name}",
        "message": f"{message}"
    }
    json_data = json.dumps(data)
    size = len(json_data)
    packet = str(size) + json_data
    return packet

def build_join_packet(name):
    global client_packet_buffers
    data = {
        "type": "join",
        "nick": f"{name}"
    }
    json_data = json.dumps(data)
    size = len(json_data)
    packet = str(size) + json_data
    return packet

def build_leave_packet(sock):
    global client_packet_buffers
    name = client_packet_buffers[sock]["nick"]
    data = {
        "type": "leave",
        "nick": f"{name}"
    }
    json_data = json.dumps(data)
    size = len(json_data)
    packet = str(size) + json_data
    return packet

def broadcast(packet):
    global client_packet_buffers
    for client_socket in client_packet_buffers.keys():
        try:
            client_socket.send(packet)
        except socket.error:
            # Handle socket errors (e.g., client disconnected)
            addr, port = client_socket.getpeername()
            print(f"('{addr}', {port}): disconnected")
            client_socket.close()
            del client_packet_buffers[client_socket]

def run_server(port):
    # since multiple clients will be sending data streams to the server...
    #   the server needs to maintain a packet buffer for each client.
    #       python dict matching clients socket as key to buffer
    
    global client_packet_buffers

    listening_socket = socket.socket()
    listening_socket.bind((HOST, port))
    listening_socket.listen()
    print("waiting for connections")

    # Listener socket will also be included in set 
    read_set = {listening_socket}

    # The server will run using select() to handle multiple connections 
    while True:
        ready_to_read, _, _ = select.select(read_set, {}, {})
        for s in ready_to_read:
            # When listener shows ready to read, there is a new connection to be accept()ed
            if s == listening_socket:
                conn, addr = s.accept()
                print(f'{addr}: connected')
                # build join packet
                read_set.add(conn)
                # add packet buffer to dictonary for the client
                client_packet_buffers[conn] = {"nick": "", "data": ""}
            else:
                addr, port = s.getpeername()
                try:
                    packet = s.recv(4096)
                    if packet:
                        json_payload = packet[2:]
                        decoded_packet = json.loads(json_payload.decode())
                        print(f"Decoded Packet: {decoded_packet}")
                        packet_type = decoded_packet.get("type")
                        if packet_type == "hello":
                            name = handle_hello_packet(s, decoded_packet)   
                            join_packet = build_join_packet(name)
                            broadcast(join_packet.encode())
                        elif packet_type == "chat":
                            if decoded_packet["message"] == "/quit":
                                leave_packet = build_leave_packet(s)
                                broadcast(leave_packet.encode())
                            else:
                                chat_packet = handle_chat_packet(s, decoded_packet)
                                broadcast(chat_packet.encode())
                        else:
                            print(f'Invalid packet type')
                            return 1
                    else:
                        break
                except ConnectionResetError:
                    read_set.remove(s)
                    client_packet_buffers.pop(s)
                    s.close()
                    

def main(argv):
    if len(argv) != 2:
        usage()
        return 1
    
    try:
        port = int(argv[1])
    except:
        usage()
        return 1
    
    run_server(port)
    

if __name__ == "__main__":
    sys.exit(main(sys.argv))