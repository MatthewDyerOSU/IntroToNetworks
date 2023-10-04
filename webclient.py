import socket
import sys

def checkNumArgs(argv):
    if len(argv) != 2 and len(argv) != 3:
        print("Incorrect number of arguments")
        exit(1)


def main():

    # Check input
    checkNumArgs(sys.argv)

    # Establish address and port number
    args = sys.argv
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
    seq = req.encode("ISO-8859-1")
    s.sendall(seq)

    # Receive the web response
    while True:
        d = s.recv(4096)
        if len(d) == 0:
            # Close socket when done
            s.close()
            break

if __name__ == "__main__":
    main()
