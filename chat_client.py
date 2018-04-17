# client

import sys
import socket
import select
 
def chat_client():
    # need host & port from command line
    if(len(sys.argv) < 3) :
        print 'Usage : python chat_client.py hostname port'
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])
     
    # create socket
    chat_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    chat_server.settimeout(2)
     
    # connect to remote server
    try :
        chat_server.connect((host, port))
    except :
        print 'Unable to connect'
        sys.exit()

    print 'Connected to remote host. You can start sending messages'

    # try to receive message & set username
    try :
        data = chat_server.recv(4096)
        sys.stdout.write(data); sys.stdout.flush()  
        name = sys.stdin.readline().strip()         # remove end of line character
        chat_server.send(name)
        sys.stdout.write('['+name+' - Me] '); sys.stdout.flush()
    except :
        print 'Unable to set username'
        sys.exit() 


    while 1:
        # only ever have 2 sockets (unlike server)
        # these are server and stdin
        socket_list = [sys.stdin, chat_server]
         
        # Get the list sockets which are readable
        # server is handling the sockets in non-blocking mode using select.select()
        # select.select(
        #          potential_readers,
        #          potential_writers,
        #          potential_errs,
        #          timeout)
        # ready_to_read = an array of all socket descriptors that are readable

        ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])
         
        for sock in ready_to_read: 

            # try and receive a message & print OR read in from keyboard            
            if sock == chat_server:           # if socket is server
                data = sock.recv(4096)
                if not data :
                    print '\nDisconnected from chat server'
                    sys.exit()
                else :
                    sys.stdout.write(data)
                    sys.stdout.write('['+name+' - Me] '); sys.stdout.flush()     
            
            else :
                # message entered
                msg = sys.stdin.readline()
                chat_server.send(msg)
                sys.stdout.write('['+name+' - Me] '); sys.stdout.flush() # reprint the prompt (ready for next message)

if __name__ == "__main__":

    sys.exit(chat_client())