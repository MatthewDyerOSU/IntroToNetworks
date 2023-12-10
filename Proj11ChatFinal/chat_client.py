from chatui import init_windows, read_command, print_message, end_windows
import sys
import socket
import threading
import json

# init_windows(): call this first before any other UI-oriented I/O of any
#   kind. Should also be called before you start the receiver thread since 
#   that thread does I/O.

# end_windows(): call this when your program completes to clean everything up

# read_command(): this prints a prompt out at the bottom of the screen 
#   and accepts user input. It returns the line the user entered once
#   they hit the ENTER key.
#   Ex. s = read_command("Enter something> ")
#   The function takes care of screen placement of the element

# print_message(): prints a message to the output potion of the screen. The
#   handle scrolling and making sure the output doesn't interfere with the 
#   input from read_command(). No need to include newline.

def usage():
    print("Usage: client.py nickname server_address server_port")

def build_chat_packet(message):
    data = {
        "type": "chat",
        "message": f"{message}"
    }
    json_data = json.dumps(data)
    size = len(json_data)
    packet = str(size) + json_data
    return packet

def build_hello_packet(name):
    data = {
        "type": "hello",
        "nick": f"{name}"
        }
    json_data = json.dumps(data)
    size = len(json_data)
    packet = str(size) + json_data
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
    sock.send(hello_packet.encode())
    while True:
        user_input = read_command(f'{name}> ')
        chat_packet = build_chat_packet(user_input)
        sock.send(chat_packet.encode())
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

if __name__ == "__main__":
    sys.exit(main(sys.argv))