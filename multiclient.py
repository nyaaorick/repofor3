# This script creates multiple client threads that connect to a server and send messages.
import threading
import time
import socket
# This is a simple multiclient example where multiple clients connect to a server

# and send messages concurrently. Each client runs in its own thread.
# def main():
#     clients = []
    
#     for i in range(5):
#         client = threading.Thread(target=client_thread, args=(i,))
#         clients.append(client)
#         client.start()
#         time.sleep(1)  # Sleep to stagger client connections

#     for client in clients:
#         client.join()   # Wait for all clients to finish

#     print("All clients have finished sending messages.")

def client_thread(client_id):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 51234))  # Connect to the server

    message = f"Hello from client {client_id}!"
    client_socket.sendall(message.encode('utf-8'))  # Send message to the server

    response = client_socket.recv(1024).decode('utf-8')  # Receive response from the server
    print(f"Client {client_id} received: {response}")  # Print the server's response
    
if __name__ == "__main__":
    server_host = 'localhost'
    server_port = 51234

    filenames = [
        'test-workload/client_1.txt',
        'test-workload/client_2.txt',
        'test-workload/client_3.txt',
        'test-workload/client_4.txt',
        'test-workload/client_5.txt',
        'test-workload/client_6.txt',
        'test-workload/client_7.txt',
        'test-workload/client_8.txt',
        'test-workload/client_9.txt',
        'test-workload/client_10.txt'
    ]

    threads = [] 

    for i, filename in enumerate(filenames):
        client_id = i + 1 # gice client a unique ID

        #create a thread for each client
        thread = threading.Thread(target=client_thread,  # target function
                                  args=(client_id, server_host, server_port, filename))
        threads.append(thread) # 
        thread.start() # 
        print(f"thread Client-{client_id} ({filename}) successfully started.")

    
        time.sleep(0.1) # a little delay to stagger the start of threads


    for thread in threads:
        thread.join() # # Wait for all threads to finish

    print("all clients have finished sending messages.")
