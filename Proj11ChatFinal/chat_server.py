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
    """
    Handles the "hello" packet received from a client.

    Parameters:
    - sock (socket): The client's socket connection.
    - packet (dict): The parsed JSON packet containing the "hello" information.

    Returns:
    - str: The nickname associated with the client.

    This function extracts the nickname from the "hello" packet and associates it with
    the client's socket in the global `client_packet_buffers` dictionary. It then returns
    the extracted nickname.
    """
    global client_packet_buffers
    name = packet.get("nick")
    client_packet_buffers[sock]["nick"] = name
    return name

def encode_packet_and_size(data):
    """
    Encodes a JSON data packet with its size and returns the resulting binary packet.

    Parameters:
    - data (dict): The data to be encoded into a JSON packet.

    Returns:
    - bytes: The binary packet containing the JSON data preceded by its size.

    This function takes a dictionary `data`, converts it to a JSON-encoded string,
    and then encodes the size of the string into a 2-byte representation. The final
    binary packet consists of the size bytes followed by the encoded JSON data.

    Example:
    ```
    data = {"type": "hello", "nick": "John"}
    packet = encode_packet_and_size(data)
    ```
    """
    json_data = json.dumps(data)
    encoded_data = json_data.encode()
    size = len(json_data)
    size_bytes = size.to_bytes(2, 'big')
    packet = size_bytes + encoded_data
    return packet

def handle_chat_packet(sock, packet):
    """
    Handles a "chat" packet received from a client.

    Parameters:
    - sock (socket): The client's socket connection.
    - packet (dict): The parsed JSON packet containing the "chat" information.

    Returns:
    - bytes: The binary packet ready for broadcasting.

    This function extracts the relevant information (type, sender's nickname, and message)
    from the "chat" packet, constructs a new dictionary, encodes it into a binary packet with
    the size information, and returns the resulting binary packet. This packet is suitable
    for broadcasting to other clients.

    Example:
    ```
    sock = client_socket  # Replace with the actual client socket
    packet_data = {"type": "chat", "message": "Hello, everyone!"}
    packet = handle_chat_packet(sock, packet_data)
    ```
    """
    global client_packet_buffers
    type = packet.get("type")
    name = client_packet_buffers[sock]["nick"]
    message = packet.get("message")
    data = {
        "type": f"{type}",
        "nick": f"{name}",
        "message": f"{message}"
    }
    packet = encode_packet_and_size(data)
    return packet

def build_join_packet(name):
    """
    Constructs a "join" packet for a new client.

    Parameters:
    - name (str): The nickname of the client joining the chat.

    Returns:
    - bytes: The binary packet containing the "join" information.

    This function takes the nickname of a client joining the chat, constructs a dictionary
    with the "join" type and the nickname, and then encodes it into a binary packet with
    the size information. The resulting binary packet is suitable for broadcasting to other clients
    to notify them of the new user joining the chat.

    Example:
    ```
    new_member_name = "Alice"
    join_packet = build_join_packet(new_member_name)
    ```
    """
    global client_packet_buffers
    data = {
        "type": "join",
        "nick": f"{name}"
    }
    packet = encode_packet_and_size(data)
    return packet

def build_leave_packet(sock):
    """
    Constructs a "leave" packet for a client leaving the chat.

    Parameters:
    - sock (socket): The client's socket connection.

    Returns:
    - bytes: The binary packet containing the "leave" information.

    This function takes the socket connection of a client leaving the chat, retrieves
    the client's nickname from the global packet buffer, constructs a dictionary with the
    "leave" type and the nickname, and then encodes it into a binary packet with the size
    information. The resulting binary packet is suitable for broadcasting to other clients
    to notify them of the user leaving the chat.

    Example:
    ```
    leaving_client_socket = client_socket  # Replace with the actual client socket
    leave_packet = build_leave_packet(leaving_client_socket)
    ```
    """
    global client_packet_buffers
    name = client_packet_buffers[sock]["nick"]
    data = {
        "type": "leave",
        "nick": f"{name}"
    }
    packet = encode_packet_and_size(data)
    return packet

def get_next_packet(sock):
    """
    Retrieves the next complete packet from a client's packet buffer.

    Parameters:
    - sock (socket): The client's socket connection.

    Returns:
    - bytes or None: The binary packet data if available, or None if no complete packet is present.

    This function checks the client's packet buffer for a complete packet (containing size and data).
    If a complete packet is found, it is extracted from the buffer, and the buffer is updated accordingly.
    If no complete packet is available, the function reads data from the client's socket and appends it to
    the buffer until a complete packet is formed or the socket is closed.

    Example:
    ```
    client_socket = some_client_socket  # Replace with the actual client socket
    next_packet = get_next_packet(client_socket)
    ```
    """
    global client_packet_buffers
    while True:
        if len(client_packet_buffers[sock]["data"]) >= 2:
            packet_size = int.from_bytes(client_packet_buffers[sock]["data"][:2], "big")
            if len(client_packet_buffers[sock]["data"]) >= packet_size + 2:
                packet_data = client_packet_buffers[sock]["data"][:packet_size + 2]
                client_packet_buffers[sock]["data"] = client_packet_buffers[sock]["data"][packet_size + 2:]
                return packet_data
        data = sock.recv(4096)
        if len(data) == 0:
            return None
        client_packet_buffers[sock]["data"] += data


def broadcast(packet):
    """
    Sends a binary packet to all connected clients.

    Parameters:
    - packet (bytes): The binary packet to be sent to all clients.

    This function iterates through the global dictionary of client sockets and attempts to send
    the provided binary packet to each client. If any socket encounters an error (e.g., due to a
    client disconnecting), it closes the socket, removes it from the dictionary, and prints a
    notification about the disconnection.

    Example:
    ```
    chat_message = build_chat_packet("Alice", "Hello, everyone!")
    broadcast(chat_message)
    ```
    """
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

def accept_new_connection(listening_socket, read_set):
    """Accepts a new connection and initializes client data."""
    conn, addr = listening_socket.accept()
    read_set.add(conn)
    client_packet_buffers[conn] = {"nick": "", "data": b""}

def run_server(port): 
    """
    Runs the chat server, managing client connections and packet processing.

    Parameters:
    - port (int): The port number on which the server listens for incoming connections.

    This function sets up a listening socket, accepts incoming connections, and continuously
    processes packets from connected clients. It uses the select() function to efficiently handle
    multiple connections. The server reacts to "hello" packets by adding clients to the dictionary
    of connected clients and broadcasting "join" packets. It also handles "chat" packets, broadcasts
    chat messages, and reacts to "/quit" messages by broadcasting "leave" packets. If a client
    disconnects, the function cleans up the associated resources.

    Example:
    ```
    run_server(12345)
    ```
    """
    global client_packet_buffers

    listening_socket = socket.socket()
    listening_socket.bind((HOST, port))
    listening_socket.listen()
    print("waiting for connections")
 
    read_set = {listening_socket} 

    while True:
        ready_to_read, _, _ = select.select(read_set, {}, {})
        for s in ready_to_read:
            if s == listening_socket:
                accept_new_connection(listening_socket, read_set)
            else:
                addr, port = s.getpeername()
                try:
                    packet = get_next_packet(s)
                    if packet:
                        json_payload = packet[2:]
                        decoded_packet = json.loads(json_payload.decode())
                        packet_type = decoded_packet.get("type")
                        if packet_type == "hello":
                            name = handle_hello_packet(s, decoded_packet)   
                            join_packet = build_join_packet(name)
                            broadcast(join_packet)
                        elif packet_type == "chat":
                            if decoded_packet["message"] == "/quit":
                                leave_packet = build_leave_packet(s)
                                broadcast(leave_packet)
                            else:
                                chat_packet = handle_chat_packet(s, decoded_packet)
                                broadcast(chat_packet)
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