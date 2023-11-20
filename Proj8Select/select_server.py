# Example usage:
#
# python select_server.py 3490

import sys
import socket
import select

HOST = '127.0.0.1'

def run_server(port):
    
    listening_socket = socket.socket()
    listening_socket.bind((HOST, port))
    listening_socket.listen()
    print("waiting for connections")
    read_set = {listening_socket}

    while True:
        ready_to_read, _, _ = select.select(read_set, {}, {})
        for s in ready_to_read:
            if s == listening_socket:
                conn, addr = s.accept()
                print(f'{addr}: connected')
                read_set.add(conn)
            else:
                addr, port = s.getpeername()
                data = s.recv(4096)
                if data:
                    data_len = len(data)
                    print(f"('{addr}', {port}) {data_len} bytes: {data}")
                else:
                    read_set.remove(s)
                    s.close()
                    print(f"('{addr}', {port}): disconnected")



#--------------------------------#
# Do not modify below this line! #
#--------------------------------#

def usage():
    print("usage: select_server.py port", file=sys.stderr)

def main(argv):
    try:
        port = int(argv[1])
    except:
        usage()
        return 1

    run_server(port)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
