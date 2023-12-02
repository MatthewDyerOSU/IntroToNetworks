import sys
import socket

# How many bytes is the word length?
WORD_LEN_SIZE = 2

def usage():
    print("usage: wordclient.py server port", file=sys.stderr)

packet_buffer = b''


def get_next_word_packet(s):
    """
    Return the next word packet from the stream.

    The word packet consists of the encoded word length followed by the
    UTF-8-encoded word.

    Returns None if there are no more words, i.e. the server has hung
    up.
    """
    global packet_buffer
    while True:
        if len(packet_buffer) >= 2:
            packet_size = int.from_bytes(packet_buffer[:2], 'big')
            if len(packet_buffer) >= packet_size + 2:
                packet_data = packet_buffer[:packet_size+2]
                packet_buffer = packet_buffer[packet_size+2:]
                return packet_data
        data = s.recv(5)
        if len(data) == 0:
            return None
        packet_buffer += data



def extract_word(word_packet):
    """
    Extract a word from a word packet.

    word_packet: a word packet consisting of the encoded word length
    followed by the UTF-8 word.

    Returns the word decoded as a string.
    """
    extracted_word = word_packet[2:]
    decoded_word = extracted_word.decode()
    return decoded_word

# Do not modify:

def main(argv):
    try:
        host = argv[1]
        port = int(argv[2])
    except:
        usage()
        return 1

    s = socket.socket()
    s.connect((host, port))

    print("Getting words:")

    while True:
        word_packet = get_next_word_packet(s)

        if word_packet is None:
            break

        word = extract_word(word_packet)

        print(f"    {word}")

    s.close()

if __name__ == "__main__":
    sys.exit(main(sys.argv))