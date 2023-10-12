import socket
import sys
import os

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

    # receive data in loop until blank line reached (\r\n\r\n)
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

def parseRequest(request):
    lines = request.split("\r\n")
    firstLine = lines[0]
    firstLineParts = firstLine.split()
    method = firstLineParts[0]
    path = firstLineParts[1]
    protocol = firstLineParts[2]
    return method, path, protocol

def getFileName(fullPath):
    pathAndFile = os.path.split(fullPath)
    pathOnly = pathAndFile[0]
    fileName = pathAndFile[1]
    return pathOnly, fileName

def getExtension(fileName):
    nameAndExt = os.path.splitext(fileName)
    name = nameAndExt[0]
    extension = nameAndExt[1]
    return name, extension

def readFile(fileName):
    try:
        with open(fileName) as fp:
            data = fp.read()
            return data
    except:
        return ""

def buildResponse(code, mime, length, body):
    res = (f'HTTP/1.1 {code}\r\n'
            f'Content-Type: {mime}\r\n'
            f'Content-Length: {length}\r\n'
            'Connection: close\r\n'
            '\r\n'
            f'{body}')
    return res

def main():
    args = sys.argv

    extDict = {
        ".txt": "text/plain",
        ".html": "text/html"
    }

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
        newConn, address = s.accept()
        # print(f'New Socket: {new_conn}, Address: {address}')
        newSocket = newConn

        # Receive the request from client in loop
        requestData = receiveRequest(newSocket)

        # Convert data into bytes
        requestBytes = requestData.decode("ISO-8859-1")

        # Parse the request, splitting off the method, path and protocol
        method, path, protocol = parseRequest(requestBytes)

        # Parse the path plus filename, splitting them from eachother
        pathOnly, fileName = getFileName(path)

        #Parse the filename, splitting off the extension
        nameOnly, extension = getExtension(fileName)

        # Read the file in
        data = readFile(fileName)

        if len(data) == 0:
            res = buildResponse("404 Not Found", "text/plain", "13", "404 not found")
        else:
            # Build the response
            res = buildResponse("200 OK", extDict[extension], len(data), data)
        
        # Encode the response
        bytes = res.encode("ISO-8859-1")
        # print(f'Bytes: {bytes}')
        
        # Send the response
        newSocket.sendall(bytes)

        # Close the new socket
        newSocket.close()
    # End loop


if __name__ == "__main__":
    main()