'''
# evelop a client/server networked system that
# implements a “tuple space”. Clients send requests to include, read, or delete tuples. The server
# needs to deal with multiple clients at the same time. Each client connects to the server, starting
# “a session”, and sends one or more requests during the session, until it closes.

# After sending a request, the client waits for the response to arrive before sending the next
# request to the server. This is what we call “synchronous behaviour”, which simplifies the client
# implementation. After a number of requests and responses, the client terminates the session
# and closes the connection. The server detects that the client closed the connection and also
# ends the session with that client.

# Tuples: The server will implement a “tuple space”. Each tuple is a key-value pair, in which both
# key and value are strings of up to 999 characters each. The key needs to be unique, i.e. there
# cannot be two tuples with the same key. You can imagine this as a simple table containing two
# columns, namely a key and a value.

#tuple space example:  
# key:(greeting,lighthouse,andremaginot); 
# value:(expression of goodwill, a tower with a light, a french politician)

#The server implements three operations:
    #v = READ(k): if a tuple with key k exists, the tuple (k, v) is read and the value v is
    #returned; if k does not exist, the operation fails and v returns empty;

    #v = GET(k): if a tuple with key k exists, the tuple (k, v) is deleted and the value v is
    #returned; if k does not exist, the operation fails and v returns empty;

    #e = PUT(k, v): if the key k does not exist already, the tuple (k, v) is added to the tuple
    #space and e returns 0; if a tuple with key k already exists, the operation fails and e
    #equals 1 is returned.

#example response: 
  #- OK (k, v) read
  #- OK (k, v) removed
  #- OK (k, v) added
  #- ERR k already exists (in case of a PUT using a key k that already exists)
  #- ERR k does not exist (in case of a READ or GET using a key k that does not exist)







###
#Client output. As the client runs, for each line processed, the client will display what the
#operation was and its result. 
  #example output:
  #PUT Manchester-United 20: OK (Manchester-United, 20) added
  #PUT Liverpool 19: OK (Liverpool, 19) added
  #PUT Arsenal 31: OK (Arsenal, 31) added
  #PUT Everton 9: OK (Everton, 9) added
  #PUT Manchester-City 9: OK (Manchester-City, 9) added
  #READ Liverpool: OK (Liverpool, 19) read
  #READ Arsenal: OK (Arsenal, 31) read
  #PUT Arsenal 13: ERR Arsenal exists
  #GET Arsenal: OK (Arsenal, 31) removed
  #PUT Arsenal 13: OK (Arsenal, 13) added
  #GET Manchester-United: OK (Manchester-United, 20) removed
  #READ Manchester-United: ERR Manchester-United does not exist  



###
#Server output:The server, on its side, displays every 10s a summary of the current tuple
#space, containing the number of tuples in the tuple space, the average tuple size, the average
#key size, and the average value size (string), the total number of clients which have connected
#(finished or not) so far, the total number of operations, total READs, total GETs, total PUTs, and
#how many errors.


# Multi-threaded server:
# As stated above, the server needs to handle sessions with multiple
# clients at the same time. For this reason, the server will use multiple threads, each thread being
# created to deal with a single client. This allows the server implementation to be much simpler
# than if having to interleave requests from multiple clients. The server will spawn a new thread
# whenever a new client connects with the server. When the session/connection with the client is
# closed, the thread terminates.

#Command line arguments to client and server:
#  You first start the server providing the port
#number to be used by the server to wait for incoming connections. This has to be a high port,
#such as 51234 (50000 <= port <= 59999).


on a different host, you start each of your clients. The client gets three arguments:
- the hostname where the server resides (can be “localhost” if client and server are in the
same host);
- the port number to connect with the server (the same value used by the server);
- the pathname to the text file that contains the requests to be processed (sent to the
server), in the format described above


Multi-threaded server that uses TCP sockets. 

The focus of the assignment is to use TCP sockets to implement a client/server protocol with the three supported operations 
(READ, GET, and PUT) and a server which correctly implements these operations despite concurrent access 
of threads to the (shared) tuple space.

Your implementation must adhere to the protocol 
because your client and server should be able to interoperate with the server and client 
developed by other students. 
 
Protocol. The protocol to be implemented encodes the request messages as follows: 
- NNN R k 
- NNN G k 
- NNN P k v 
 
NNN is three characters indicating the total message size, the first letter indicates the command 
(R for READ, G for GET, and P for PUT), k is the key and v is the value. The minimum size is 7 
(which is when the key k is a single character in a READ/GET) and the maximum is 999.  
 
Examples of request messages that can be transmitted to a server: 
- 007 R a 
- 010 R abcd 
- 012 G 123456 
- 053 P good-morning-message how are you feeling today? 
 
The response messages (in line with what was defined earlier) are also implemented using 
strings, whose format is one of the following: 
- NNN OK (k, v) read 
- NNN OK (k, v) removed 
- NNN OK (k, v) added 
- NNN ERR k already exists 
- NNN ERR k does not exist 
 
Examples (if k and v are a single alphanumeric character): 
- 018 OK (k, v) read 
- 021 OK (k, v) removed 
- 014 OK k added 
- 024 ERR k already exists 
- 024 ERR k does not exist 
 
 
How to test your networked system. 
We provide example files to be given to the clients, and 
the expected outputs for each client and the server. In the test, the tuple space contains 100 
different words (from an English dictionary). Each of the files has 100,000 requests.  
 
Follow these steps: 
1) start the server at one host 
2) run all the clients one after the other (e.g. for Java it could be 
for i in {1..10}; do java myclient server 51234 client-$i.txt; done 
3) note the outputs produced by the clients and specially, the server 
4) close the server (^c) and start it again 
5) run all the clients one after the other (e.g. for Java it could be 
for i in {1..10}; do java myclient server 51234 client-$i.txt &; done 
6) note the outputs produced by the server


'''
import socket
import threading