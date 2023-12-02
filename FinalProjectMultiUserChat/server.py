import sys
import socket
import select



# When server gets chat packet from one client, it rebroadcasts to all clients

# When a client connects/disconnects, this also is broadcasted





HOST = '127.0.0.1'

# Usage: python chat_server.py 3490
#   there is no default port, must be specified on command line
def usage():
    print("Usage: python server.py port")

def run_server(port):
    # since multiple clients will be sending data streams to the server...
    #   the server needs to maintain a packet buffer for each client.
    #       python dict matching clients socket as key to buffer
    client_packet_buffers = {}

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
                read_set.add(conn)
                # add packet buffer to dictonary for the client
                client_packet_buffers[conn] = []
            else:
                addr, port = s.getpeername()
                packet = s.recv(4096)
                if packet:
                    data_len = len(packet)
                    print(f"('{addr}', {port}) {data_len} bytes: {packet}")
                else:
                    read_set.remove(s)
                    client_packet_buffers.pop(s)
                    s.close()
                    print(f"('{addr}', {port}): disconnected")
                    

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