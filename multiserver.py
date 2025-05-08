#multiserver
import socket
import threading
import time
from tuple_space import TupleSpace

# --- Server Configuration ---
# thread-safe ways to manage statistics.
# Using locks for each counter is a straightforward approach.
#keep track of operations
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

        print(f"[receive] from {addr}: '{message_body}'")
        response_payload = process_command(message_body, tuple_space)
        print(f"[response] send to {addr}: '{response_payload}'")

        if not send_message(client_socket, addr, response_payload):
            client_active = False # connect close
            break # 

    print(f"Shut Down Client {addr} 's connection.")
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

    # return the response payload
    return response_payload


#handle receiving the message
def receive_message(client_socket, addr):
    message_body = None # reset message body
    try:
        header_bytes = client_socket.recv(3)
        if not header_bytes or len(header_bytes) < 3:
            return None # handel err

        # decode the header bytes to get the message length
        try:
            msg_len_str = header_bytes.decode('utf-8')
            total_msg_len = int(msg_len_str)
            # check if the message length is valid 7 - 992
            if not (7 <= total_msg_len <= 992):
                update_stats("error_count")
                return None
                 
            
        except (ValueError, UnicodeDecodeError) as e:
            update_stats("error_count")
            return None # 

        # 3. Calculate the number of bytes to read for the message body
        bytes_to_read = total_msg_len - 3
        if bytes_to_read < 0:
             update_stats("error_count")
             return None

        body_bytes_list = []
        bytes_read = 0

        while bytes_read < bytes_to_read:
            chunk = client_socket.recv(min(bytes_to_read - bytes_read, 4096))
            body_bytes_list.append(chunk)
            bytes_read += len(chunk)

        #decode the message body
        message_body = b"".join(body_bytes_list).decode('utf-8')
        print(f"[rec] from {addr}: '{message_body}'")
    
    # exception handling
    except Exception as e:
        update_stats("error_count")
        return None # 

    return message_body #return the message body
    

#handle sending the message
#As the client runs, for each line processed, 
#the client will display what the operation was and its result from the server.
def send_message(client_socket, addr, response_payload):

    try:
        payload_bytes = response_payload.encode('utf-8')
        total_len = len(payload_bytes) + 3

        # check if the total length is valid
        if total_len > 992:
             print(f"[err] len too long ({total_len} bytes) send to {addr}")
             response_payload = "ERR response too long"
             payload_bytes = response_payload.encode('utf-8')
             total_len = len(payload_bytes) + 3
             update_stats("error_count")
             return False 

        header = f"{total_len:03d}"
        full_message = header.encode('utf-8') + payload_bytes
        client_socket.sendall(full_message)
        return True 
   
    # exception handling
    except Exception as e:
        print(f"[err] send to {addr} exception happen : {e}")
        update_stats("error_count")
        return False #failure



def report_stats(interval, tuple_space):
     #every "interval"  second , it print 
     while True:
        time.sleep(interval)
        ts_stats = tuple_space.calculate_stats() 
        with stats_lock:
            current_stats = stats.copy() 

        #print everything
        print("\n----- Server Statistics -----")
        print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  Connected Clients (Total): {current_stats['total_clients']}")
        print(f"  Tuple Space:")
        print(f"    - Count: {ts_stats['count']}")
        print(f"    - Avg Tuple Size: {ts_stats['avg_tuple_size']:.2f}")
        print(f"    - Avg Key Size: {ts_stats['avg_key_size']:.2f}")
        print(f"    - Avg Value Size: {ts_stats['avg_value_size']:.2f}")
        print(f"  Operations:")
        print(f"    - READs: {current_stats['read_ops']}")
        print(f"    - GETs: {current_stats['get_ops']}")
        print(f"    - PUTs: {current_stats['put_ops']}")
        print(f"  Errors: {current_stats['error_count']}")
        print("):---------------------------------------------:(\n")


#
def start_server(host='localhost', port=51234):

    # crate a tuple space instance
    tuple_space = TupleSpace()
    print("TupleSpace started.")


    # daemon=True this thread is a daemon thread, meaning it will not prevent the program from exiting.
    stats_thread = threading.Thread(target=report_stats, args=(10, tuple_space), daemon=True)
    stats_thread.start()
    print("stats thread reporter now starts every 10s.")


    #socket server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
     
     
    #listen for incoming connections
    server_socket.listen(10)  ### listen 10 thread
    print(f"server {host}:{port} start, wait for connection...")

    # Main loop to accept and handle client connections
    # The server will run indefinitely until interrupted
    try:
        while True:
                # accept() will block until a client connects
                # server_socket is the listening socket
                # client_socket is the new socket object to communicate with the client
                # addr is the address bound to the socket on the other end
                # accept() returns a tuple (client_socket, addr)
                client_socket, addr = server_socket.accept()

                # calulate the total number of clients
                update_stats("total_clients")
                print(f"\n[connection] accept from {addr} 's connection , total client num : {get_stat('total_clients')}")

                # Create a new thread for each client connection
                client_thread = threading.Thread(target=handle_client,args=(client_socket, addr, tuple_space))
                # execute the thread
                client_thread.start()

    except KeyboardInterrupt:
        print("\n[err] server shutdown by keyboard interrupt.")

    finally:
        # Close the server socket
        # This will close the listening socket and all connected client sockets
        print("close socket。")
        server_socket.close()

if __name__ == "__main__":
    # default as assigment advised
    server_port = 51234
    # loaclhost
    start_server(host='0.0.0.0', port=server_port)
