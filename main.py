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

#tuple space example:  key:(greeting,lighthouse,andremaginot); value:(expression of goodwill, a tower with a light, a french politician)
