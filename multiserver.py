#multiserver
import socket
import threading
import time
import sys # To get command line arguments (port)
from tuple_space import TupleSpace

# Import the TupleSpace class from my other file
try:
    from tuple_space import TupleSpace
except ImportError:
    print("Error: Could not import TupleSpace class.")
    sys.exit(1)


# --- Global Shared Resources ---
# thread-safe ways to manage statistics.
# Using locks for each counter is a straightforward approach.
'''
    --- Information the Server Needs to Print ---
    Server output:
    The server, on its side, displays every 10s a summary of the current tuple space, containing the number of tuples in the tuple space, the average tuple size, the average key size, and the average value size (string), the total number of clients which have connected (finished or not) so far, the total number of operations, total READs, total GETs, total PUTs, and how many errors.

        #the total number of clients which have connected...: stats["total_clients"] 
        #the total number of operations:  stats["total_ops"] 
        #total READs:  stats["read_ops"] 
        #total GETs:  stats["get_ops"] 
        #total PUTs:  stats["put_ops"] 
        #and how many errors: stats["error_count"] 

    --- How the Server Handles Many Clients at Once (Multi-threaded server) ---
    Multi-threaded server: As stated above, the server needs to handle sessions with multiple clients at the same time. 
    For this reason, the server will use multiple threads

'''
stats = {
    "total_clients": 0,
    "total_ops": 0,
    "read_ops": 0,
    "get_ops": 0,
    "put_ops": 0,
    "error_count": 0,
}
stats_lock = threading.Lock() # A single lock to protect the entire stats dictionary

# --- Update Stats Safely ---
def update_stats(key, increment=1):
    """Safely increments a statistic counter."""
    with stats_lock:
        if key in stats:
            stats[key] += increment
        else:
            print(f"[Warning] Attempted to update unknown stat key: {key}")

# --- Read Stats Safely ---
def get_stat(key):
    """Safely reads a statistic counter."""
    with stats_lock:
        return stats.get(key, 0)  # Returns the value of the key if it exists, or 0 if it doesn't.
#不存在的情况（返回 0）。服务器代码在需要获取某个统计数字（比如在 report_stats 中准备输出报告时）会调用这个函数




def handle_client(client_socket, addr, tuple_space):
    """Handles client connection."""
    print(f"Client {addr} connected.")

    message = client_socket.recv(1024).decode('utf-8')  # Receive message from the client
    print("Received:", message)  # Print the received message

    response = f"Message '{message}' received by server."  # Prepare a response to client
    client_socket.sendall(response.encode('utf-8'))  # Send response to client
    """Handles client connection."""
    print(f"Client {addr} connected.")

    message = client_socket.recv(1024).decode('utf-8')  # Receive message from the client
    print("Received:", message)  # Print the received message

    response = f"Message '{message}' received by server."  # Prepare a response to client
    client_socket.sendall(response.encode('utf-8'))  # Send response to client
   

def start_server(host='localhost', port=9090):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)  # Allow up to 5 clients to connect
    print(f"Server started on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()  # Accept a new connection
        print(f"Connection from {addr} has been established.")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,addr))
        client_thread.start()  # Start a new thread for the client
    
        