import socket
import sys

def checkNumArgs(argv):
    # if len(argv) != 1 and len(argv) != 2:
    if len(argv) not in {1, 2}:
        print("Incorrect number of arguments")
        exit(1)

def parsePort(args):
    if len(args) > 1:
        port = int(args[1])
    else:
        port = 28333
    return port

def bindSocket(sock, port):
    # Error handling for bind is from geeksforgeeks.org
    try:   
        sock.bind(('', port))
    except socket.error as message:
        print('Bind failed. Error Code:'
            + str(message[0]) + ' Message ' 
            + message[1])
        exit(1)

def receiveRequest(sock):
    request_data = b''

    while True:
        data = sock.recv(4096)
        # print(f'Data: {data}')
        if not data:
            break
        request_data += data

        #Check for end of request
        if b'\r\n\r\n' in request_data:
            break
    return request_data

def buildResponse(code, mime, length, body):
    res = (f'HTTP/1.1 {code}\r\n'
            f'Content-Type: {mime}\r\n'
            f'Content-Length: {length}\r\n'
            'Connection: close\r\n'
            '\r\n'
            f'{body}\r\n')
    return res

def main():
    args = sys.argv

    checkNumArgs(args)

    port = parsePort(args)

    # Get a socket
    s = socket.socket()

    # Bind the socket to a port: bind()
    bindSocket(s, port)

    # Set the socket up to listen: listen()
    s.listen()
    print(f"Server listening on port {port}")

    # Accept new connections (returns a tuple)
    while True:
        new_conn, address = s.accept()
        # print(f'New Socket: {new_conn}, Address: {address}')
        new_socket = new_conn

        # Receive the request from client in loop
        request_data = receiveRequest(new_socket)
        
        # decoded = request_data.decode("ISO-8859-1")
        # print(f'Decoded: {decoded}')

        # Build the response
        res = buildResponse("200 OK", "text/plain", "6", "Hello!")
        
        # Encode the response
        bytes = res.encode("ISO-8859-1")
        # print(f'Bytes: {bytes}')
        
        # Send the response
        new_socket.sendall(bytes)

        # Close the new socket
        new_socket.close()
    # End loop


if __name__ == "__main__":
    main()