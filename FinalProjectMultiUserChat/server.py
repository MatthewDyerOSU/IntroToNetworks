# The server will run using select() to handle multiple connections 

# Listener socket will also be included in set 

# When it shows ready to read, there is a new connection to be accept()ed

# if any other already accepted sockets show ready to read, it means client 
#   has data needing to be handled

# When server gets chat packet from one client, it rebroadcasts to all clients

# When a client connects/disconnects, this also is broadcasted

# since multiple clients will be sending data streams to the server...
#   the server needs to maintain a packet buffer for each client.
#       python dict matching clients socket as key to buffer

# Usage: python chat_server.py 3490
#   there is no default port, must be specified on command line

