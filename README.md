# Chat-Server

Simple chat client-server application which transmits user messages to a multicast address and receives messages sent from other clients on other machines sent to the same multicast address.

## To Run

Start `chat-server.py` first. The port will be specified in terminal - you will need this for connecting client.

```bash
python2.7 chat-server.py
```

Then open new terminal and start between 1 - 10 clients.

```bash
python2.7 chat_client.py <insert host here> <insert port here>
# example:
python2.7 chat_client.py localhost 9009
```


