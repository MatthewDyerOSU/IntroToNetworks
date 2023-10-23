from datetime import datetime
import socket

def system_seconds_since_1900():
    """
    The time server returns the number of seconds since 1900, but Unix
    systems return the number of seconds since 1970. This function
    computes the number of seconds since 1900 on the system.
    """

    # Number of seconds between 1900-01-01 and 1970-01-01
    seconds_delta = 2208988800

    seconds_since_unix_epoch = int(datetime.now().strftime("%s"))
    seconds_since_1900_epoch = seconds_since_unix_epoch + seconds_delta

    return seconds_since_1900_epoch

def nist_seconds_since_1900():
    """
    This function creates a socket which connects to and queries 
    the NIST atomic time server, receives the response 4 bytes at a time, 
    decodes those bytes into an integer, and returns that integer which
    represents the number of seconds since 1900 until now as calculated by
    the NIST time server.
    """
    s = socket.socket()
    s.connect(("time.nist.gov", 37))
    request_data = b''

    while True:
        data = s.recv(4)

        # print(f'Data: {data}')
        if not data:
            break

        request_data += data
    
    decoded_bytes = int.from_bytes(request_data, "big")
    
    return decoded_bytes


def main():

    nist_time = nist_seconds_since_1900()
    system_time = system_seconds_since_1900()

    print(f'NIST time  : {nist_time}')
    print(f'System time: {system_time}')

if __name__ == '__main__':
    main()