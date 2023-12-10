from chatui import init_windows, read_command, print_message, end_windows
import sys
import socket
import threading
import json

def usage():
    print("Usage: client.py nickname server_address server_port")

def encode_packet_and_size(data):
    json_data = json.dumps(data)
    encoded_data = json_data.encode()
    size = len(json_data)
    size_bytes = size.to_bytes(2, 'big')
    packet = size_bytes + encoded_data
    return packet

def build_chat_packet(message):
    data = {
        "type": "chat",
        "message": f"{message}"
    }
    packet = encode_packet_and_size(data)
    return packet

def build_hello_packet(name):
    data = {
        "type": "hello",
        "nick": f"{name}"
        }
    packet = encode_packet_and_size(data)
    return packet

def handle_chat_packet(packet):
    name = packet.get("nick")
    message = packet.get("message")
    ret = f"{name}: {message}"
    return ret

def handle_join_packet(packet):
    name = packet.get("nick")
    ret = f"*** {name} has joined the chat"
    return ret

def handle_leave_packet(packet):
    name = packet.get("nick")
    ret = f"*** {name} has left the chat"
    return ret

def send_thread(sock, name):
    hello_packet = build_hello_packet(name)
    sock.send(hello_packet)
    while True:
        user_input = read_command(f'{name}> ')
        chat_packet = build_chat_packet(user_input)
        sock.send(chat_packet)
        if user_input == "/quit":
            break

def receive_thread(sock):
    while True:
        try:
            packet = sock.recv(4096).decode()
            if not packet:
                break
            decoded_packet = json.loads(packet[2:])
            message_type = decoded_packet.get("type")
            if not decoded_packet:
                break
            elif message_type == "chat":
                message = handle_chat_packet(decoded_packet)
            elif message_type == "join":
                message = handle_join_packet(decoded_packet)
            elif message_type == "leave":
                message = handle_leave_packet(decoded_packet)
            else:
                print_message("Unknown message type")
                break
            print_message(message)
        except ConnectionResetError:
            print_message("Connection Reset Error")
            break
        except json.JSONDecodeError:
            print_message("Invalid JSON format for message")
            break

def main(argv):
    # Client will be started by specifying the nickname, server address, and 
    #   server port on the command line. There are no defaults.

    # Usage: python client.py nickname server_address server_port
    # ex: python client.py chris localhost 3490
    num_args = len(argv)
    if num_args != 4:
        usage()
        return 1
    
    try:
        name = argv[1]
        host = argv[2]
        port = int(argv[3])
    except:
        usage()
        return 1
    
    # initialize UI
    init_windows()
    
    s = socket.socket()
    s.connect((host, port))

    # Client will be multithreaded so data can arrive while the user is typing
    #   Main sending thread will:
    #       Read keyboard input
    #       Send chat messages from the user to the server
    send_thread_instance = threading.Thread(target=send_thread, args=(s, name), daemon=True)
    #   Receiving thread will:
    #       Receive packets from the server
    #       Display those results on-screen
    recv_thread_instance = threading.Thread(target=receive_thread, args=(s,), daemon=True)

    send_thread_instance.start()
    recv_thread_instance.start()

    send_thread_instance.join()
    # There is no shared data between threads so no need for mutexes or the like

    end_windows()

if __name__ == "__main__":
    sys.exit(main(sys.argv))