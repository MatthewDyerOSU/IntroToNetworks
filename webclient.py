import socket
import sys

def checkNumArgs(argv):
    if len(argv) != 2 and len(argv) != 3:
        print("Incorrect number of arguments")
        exit(1)

def main():
    args = sys.argv
    # Check input
    checkNumArgs(args)

    # Establish address and port number
    address = args[1]
    if len(args) > 2:
        port = args[2]
    else:
        port = 80

    # Make a new socket and connect to it
    s = socket.socket()
    s.connect((address, port))


    # Build and send the HTTP request
    req = ('GET / HTTP/1.1\r\n'
           f'Host: {address}\r\n'
           'Connection: close\r\n'
           '\r\n')
    
    # Encode string to bytes
    bytes = req.encode("ISO-8859-1")
    s.sendall(bytes)

    # Receive the web response
    decoded = ""
    while True:
        data = s.recv(4096)
        decoded += data.decode("ISO-8859-1")
        if len(data) == 0:
            # Close socket when done
            s.close()
            break

    # print(decoded)
    
if __name__ == "__main__":
    main()
