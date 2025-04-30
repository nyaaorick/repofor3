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

# --- 命令处理辅助函数 ---
def process_command(message_body, tuple_space):
    #
    ##
    ###
    return 1

def receive_message(client_socket, addr):
    #
    #
    #
    return 1

def send_message(client_socket, addr, response_payload):
    """Sends a message to the client."""
    return 1



    # 1. 发送响应
# """ message_body = None # 重置消息体
#         response_payload = "" # 重置响应内容
#         key = None                # 初始化，以便在所有分支中都可能访问
#         value = None              # 初始化

#         header_bytes = client_socket.recv(3)  # Receive header from the client
#         if not header_bytes:
#             print(f"Client {addr} disconnected.")
#             client_active = False
#             break  #error handling
        
#         try:
            
#             msg_len_str = header_bytes.decode('utf-8') # decode msg length
#             total_msg_len = int(msg_len_str) # convert to int

#         except :
#             print(f"Error decoding message length from client {addr}.")
#             #if not total_msg_len <= 999 and >= 7 , handel error
#             break
        
#         # Receive the body of the message
#         bytes_to_read = total_msg_len - 3
#         message_body = "" # 默认消息体为空

#         if bytes_to_read > 0:
#             # **简化点：尝试一次性读取所有需要的字节**
#             body_bytes = client_socket.recv(bytes_to_read)

#              # **关键检查：** 必须检查是否收到了预期的字节数
#             if not body_bytes or len(body_bytes) != bytes_to_read:
#                 print(f"err: {len(body_bytes)} != {bytes_to_read}")
#                 client_active = False
#                 break # 退出主循环

#                 # 如果检查通过，解码消息体
#                 message_body = body_bytes.decode('utf-8')
#             # (如果 bytes_to_read 为 0，message_body 保持为空字符串)

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


# def start_server(host='localhost', port=9090):
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_socket.bind((host, port))
#     server_socket.listen(5)  # Allow up to 5 clients to connect
#     print(f"Server started on {host}:{port}")

#     while True:
#         client_socket, addr = server_socket.accept()  # Accept a new connection
#         print(f"Connection from {addr} has been established.")
#         client_thread = threading.Thread(target=handle_client, args=(client_socket,addr))