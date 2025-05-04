#multiserver
import socket
import threading
from tuple_space import TupleSpace
# --- Server Configuration ---

# --- Global Shared Resources ---
# thread-safe ways to manage statistics.
# Using locks for each counter is a straightforward approach.

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
def update_stats(key, increment=1):#add a default increment of 1
    with stats_lock:
        if key in stats:
            stats[key] += increment
        else:
            print(f"[Warning] Attempted to update unknown stat key: {key}")


# --- Read Stats Safely ---
def get_stat(key): #add a default value of 0
    with stats_lock:
        return stats.get(key, 0)  # Returns the value of the key if it exists, or 0 if it doesn't.


def handle_client(client_socket, addr, tuple_space):
    print(f"Client {addr} connected.")
    client_active = True #

    while client_active:
        message_body = receive_message(client_socket, addr)
        if message_body is None:
            client_active = False # Label Disconnect
            break # 

        print(f"[收到] 来自 {addr}: '{message_body}'")

        
        response_payload = process_command(message_body, tuple_space)
        print(f"[响应] 准备发给 {addr}: '{response_payload}'")

        if not send_message(client_socket, addr, response_payload):
            client_active = False # 标记断开
            break # 

    print(f"关闭客户端Shut Down Client {addr} 的连接's connection.")
    client_socket.close()


#handle processing of the command
def process_command(message_body, tuple_space):
    parts = message_body.split(' ', 2)  #   split the message into parts
    command = parts[0].upper()  # convert to uppercase
    # Initialize the response payload and key-value pair
    response_payload = None
    key = None
    value = None

    try:
        #handle the put
        if command == 'PUT' and len(parts) == 3:
            update_stats("put_ops") # update put operations
            key, value = parts[1], parts[2] 
            # use put in tuple_space
            success, _ = tuple_space.put(key, value) 
            if success:
                response_payload = f"OK ({key}, {value}) added"
            else:
                #key exists
                response_payload = f"ERR {key} already exists"
                update_stats("error_count") 


        # handle the get
        elif command == 'GET' and len(parts) >= 2:
            update_stats("get_ops") 
            key = parts[1]
            # use get in tuple_space

            value_got, status = tuple_space.get(key) #value_got 是返回的值，status 是状态码
    
            if status == "OK_REMOVED": 
                value = value_got 
                response_payload = f"OK ({key}, {value}) removed"
            else: 
                response_payload = f"ERR {key} does not exist"
                update_stats("error_count")

        #handle the read
        elif command == 'READ' and len(parts) >= 2:
            update_stats("read_ops")
            key = parts[1]
            # use read in tuple_space
            value_read, status = tuple_space.read(key)
            if status == "OK_READ":
                value = value_read 
                response_payload = f"OK ({key}, {value}) read"
            else: 
                response_payload = f"ERR {key} does not exist"
                update_stats("error_count")

        # handle anything not get or put or read
        else: 
            print(f"无效命令/格式: {message_body}")
            response_payload = "ERR"
            update_stats("error_count")
    
    #exception handling
    except Exception as e:
        response_payload = "ERR server internal error" # any error
        update_stats("error_count")

    # 返回最终准备好的响应负载字符串
    return response_payload
    return 1


#handle receiving the message
def receive_message(client_socket, addr):
    return 1

#handle sending the message
def send_message(client_socket, addr, response_payload):
    return 1

def message_body(client_socket, addr):

    return 1

def start_server(host='localhost', port=51234):
    
   
   
   return 1
   
   

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
 # 3. Calculate the number of bytes to read for the message body
    #bytes_to_read = total_msg_len - len(header_bytes)
# """ message_body = None # 重置消息体
#         response_payload = "" # 重置响应内容
#         key = None                # 初始化，以便在所有分支中都可能访问
#         value = None              # 初始化

#         try:
            
#             msg_len_str = header_bytes.decode('utf-8') # decode msg length
#             total_msg_len = int(msg_len_str) # convert to int

#         except :
#             print(f"Error decoding message length from client {addr}.")
#             #if not total_msg_len <= 999 and >= 7 , handel error
#             break
        
#         # Receive the body of the message
#         message_body = "" 

#         if bytes_to_read > 0:
#             body_bytes = client_socket.recv(bytes_to_read)
#                 message_body = body_bytes.decode('utf-8')

#             # --- 接收完成 ---
#             print(f"[收到] 来自 {addr}: '{message_body}'")
#             update_stats("total_ops") # 记录总操作尝试次数"""
#     message = client_socket.recv(1024).decode('utf-8')  # Receive message from the client
#     print("Received:", message)  # Print the received message

#     response = f"Message '{message}' received by server."  # Prepare a response to client
#     client_socket.sendall(response.encode('utf-8'))  # Send response to client
#     """Handles client connection."""
#     print(f"Client {addr} connected.")

#     message = client_socket.recv(1024).decode('utf-8')  # Receive message from the client
#     print("Received:", message)  # Print the received message

#     response = f"Message '{message}' received by server."  # Prepare a response to client
#     client_socket.sendall(response.encode('utf-8'))  # Send response to client




#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_socket.bind((host, port))
#     print(f"Server started on {host}:{port}")

#     while True:
#         client_socket, addr = server_socket.accept()  # Accept a new connection
#         print(f"Connection from {addr} has been established.")
#         client_thread = threading.Thread(target=handle_client, args=(client_socket,addr))