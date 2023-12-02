from chatui import init_windows, read_command, print_message, end_windows
import sys
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
        port = int(argv[3])
    except:
        usage()
        return 1

    # very first packet sent is a 'hello' packet that has the nickname in it

    # every line ater that gets sent as chat packet
    #   chat packets are shown from the server as output

    # client has a TUI (text user interface) that keeps output clean
    #   output is asynchronously displayed on a different part of the screen
    #   than the input, some terminal 'magic' needs to happen to keep them from 
    #   overwriting eachother. (This is already made and included by Beej)

    # Client will be multithreaded so data can arrive while the user is typing
    #   Main sending thread will:
    #       Read keyboard input
    #       Send chat messages from the user to the server
    #   Receiving thread will:
    #       Receive packets from the server
    #       Display those results on-screen

    # There is no shared data between threads so no need for mutexes or the like

if __name__ == "__main__":
    sys.exit(main(sys.argv))