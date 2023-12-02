import socket
import sys

def checkNumArgs(argv):
    # if len(argv) != 2 and len(argv) != 3:
    if len(argv) not in {2, 3}:
        print("Incorrect number of arguments")
        exit(1)

def parseAddressAndPort(args):
    address = args[1]
    if len(args) > 2:
        port = int(args[2])
    else:
        port = 80
    return address, port

def buildHttpReq(path, address):
    request = (f'GET /{path} HTTP/1.1\r\n'
                f'Host: {address}\r\n'
                'Connection: close\r\n'
                '\r\n')
    return request

def decodeResponse(socket):
    decoded = ""
    while True:
        data = socket.recv(4096)
        decoded += data.decode("ISO-8859-1")
        if len(data) == 0:
            # Close socket when done
            socket.close()
            break
    return decoded

def main():
    args = sys.argv
    # Check input
    checkNumArgs(args)

    # Establish address and port number
    address, port = parseAddressAndPort(args)

    # Make a new socket and connect to it
    s = socket.socket()
    s.connect((address, port))

    # Build and send the HTTP request
    req = buildHttpReq("", address)
    
    # Encode string to bytes
    bytes = req.encode("ISO-8859-1")
    s.sendall(bytes)

    # Receive the web response
    decoded = decodeResponse(s)
    print(decoded)
    
if __name__ == "__main__":
    main()
