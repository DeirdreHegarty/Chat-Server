# server
import sys
import socket
import select

HOST = '' 
SOCKET_LIST = []
RECV_BUFFER = 4096 
PORT = 9009
CLIENT_USERS = {}           # dictionary for users - remote address
clearLine = "\x1b[2K\r"     # UNIX clear line character (had issue with \r)

def chat_server():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))   # bind the socket (program claims the socket)
    server_socket.listen(10)           # enable to accept connection (limit of 10 clients)
 
    # add server socket object to the list (both client and server sockets)
    SOCKET_LIST.append(server_socket)
 
    print "Chat server started on port " + str(PORT)
 
    while 1:

        # list sockets ready to be read through (more info in client comments)
        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)
      
        for sock in ready_to_read:

            # if found server socket & it wants to read
            if sock == server_socket: 
                sockfd, addr = server_socket.accept()   # accept client connection
                SOCKET_LIST.append(sockfd)              # add to list of sockets
                print "Client (%s, %s) connected" % addr

                # send message to client asking for username
                sockfd.send('Please enter a username.\n')

                # receive name from client & add username to dictionary
                username = sockfd.recv(RECV_BUFFER)
                CLIENT_USERS[sockfd.getpeername()] = username

                # tell all clients that user has connected
                broadcast(server_socket, sockfd, "%s entered our chatting room\n" % username)
             
            # message from a client & not a new connection
            else:
                try:
                    # receive data from the client socket.
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        # something in the socket = send to all clients
                        broadcast(server_socket, sock, clearLine + '[' + str(CLIENT_USERS[sock.getpeername()]) + '] ' + data)  
                    else:
                        # assume broken & remove the socket   
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)

                        # at this stage, no data means probably the connection has been broken
                        broadcast(server_socket, sock, "%s is offline\n" % username) 

                # exception (like try-catch in java)
                except:
                    broadcast(server_socket, sock, "%s is offline\n" % username)
                    continue

    server_socket.close()
    
# broadcast chat messages to all connected clients
def broadcast (server_socket, sock, message):
    for socket in SOCKET_LIST:
        # if not a server (clients only)
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                # close socket as may be broken
                socket.close()
                # remove from list
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)
 
if __name__ == "__main__":

    sys.exit(chat_server())         

