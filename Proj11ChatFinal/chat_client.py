from chatui import init_windows, read_command, print_message, end_windows
import sys
import socket
import threading
import json

def usage():
    print("Usage: client.py nickname server_address server_port")

def encode_packet_and_size(data):
    """
    Encodes a JSON data packet with its size and returns the resulting binary packet.

    Parameters:
    - data (dict): The data to be encoded into a JSON packet.

    Returns:
    - bytes: The binary packet containing the JSON data preceded by its size.

    This function takes a dictionary `data`, converts it to a JSON-encoded string,
    and then encodes the size of the string into a 2-byte representation. The final
    binary packet consists of the size bytes followed by the encoded JSON data.

    Example:
    ```
    data = {"type": "hello", "nick": "John"}
    packet = encode_packet_and_size(data)
    ```
    """
    json_data = json.dumps(data)
    encoded_data = json_data.encode()
    size = len(json_data)
    size_bytes = size.to_bytes(2, 'big')
    packet = size_bytes + encoded_data
    return packet

def build_chat_packet(message):
    """
    Build a chat packet with the given message.

    Parameters:
    - message (str): The message content to include in the chat packet.

    Returns:
    bytes: The encoded chat packet with the message.
    """
    data = {
        "type": "chat",
        "message": f"{message}"
    }
    packet = encode_packet_and_size(data)
    return packet

def build_hello_packet(name):
    """
    Build a hello packet with the given nickname.

    Parameters:
    - name (str): The user's nickname.

    Returns:
    bytes: The encoded hello packet with the nickname.
    """
    data = {
        "type": "hello",
        "nick": f"{name}"
        }
    packet = encode_packet_and_size(data)
    return packet

def handle_chat_packet(packet):
    """
    Process a chat packet and return a formatted chat message.

    Parameters:
    - packet (dict): The chat packet containing sender's nickname and message.

    Returns:
    str: The formatted chat message in the form "nickname: message".
    """
    name = packet.get("nick")
    message = packet.get("message")
    ret = f"{name}: {message}"
    return ret

def handle_join_packet(packet):
    """
    Process a join packet and return a formatted announcement.

    Parameters:
    - packet (dict): The join packet containing the new member's nickname.

    Returns:
    str: The formatted announcement indicating a new member has joined the chat.
    """
    name = packet.get("nick")
    ret = f"*** {name} has joined the chat"
    return ret

def handle_leave_packet(packet):
    """
    Process a leave packet and return a formatted announcement.

    Parameters:
    - packet (dict): The leave packet containing the departing member's nickname.

    Returns:
    str: The formatted announcement indicating that a member has left the chat.
    """
    name = packet.get("nick")
    ret = f"*** {name} has left the chat"
    return ret

def send_thread(sock, name):
    """
    Thread for sending messages to the server.

    Parameters:
    - sock (socket.socket): The client's socket connected to the server.
    - name (str): The nickname of the client.
    """
    hello_packet = build_hello_packet(name)
    sock.send(hello_packet)
    while True:
        user_input = read_command(f'{name}> ')
        chat_packet = build_chat_packet(user_input)
        sock.send(chat_packet)
        if user_input == "/quit":
            break

def receive_thread(sock):
    """
    Thread for receiving and processing messages from the server.

    Parameters:
    - sock (socket.socket): The client's socket connected to the server.

    Exceptions:
    - ConnectionResetError: Raised if the connection is forcibly closed by the remote host.
      In such cases, the thread will print a message indicating the connection reset error
      and terminate gracefully.
    - json.JSONDecodeError: Raised if there is an issue decoding the received JSON-formatted packet.
      The thread will print a message indicating an invalid JSON format and terminate.
    """
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
    
    init_windows()
    
    s = socket.socket()
    s.connect((host, port))

    send_thread_instance = threading.Thread(target=send_thread, args=(s, name), daemon=True)
 
    recv_thread_instance = threading.Thread(target=receive_thread, args=(s,), daemon=True)

    send_thread_instance.start()
    recv_thread_instance.start()

    send_thread_instance.join()


    end_windows()

if __name__ == "__main__":
    sys.exit(main(sys.argv))