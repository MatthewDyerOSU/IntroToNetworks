# When launched, user specifies nickname on command line along with server info

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

# Client will be started by specifying the nickname, server address, and 
#   server port on the command line. There are no defaults.

# Usage: python client.py nickname server_address server_port
# ex: python client.py chris localhost 3490