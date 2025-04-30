import socket
import threading
import time

def main():
    clients = []
    
    for i in range(5):
        client = threading.Thread(target=client_thread, args=(i,))
        clients.append(client)
        client.start()
        time.sleep(1)  # Sleep to stagger client connections

    for client in clients:
        client.join()   # Wait for all clients to finish

    print("All clients have finished sending messages.")

def client_thread(client_id):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 9090))  # Connect to the server

    message = f"Hello from client {client_id}!"
    client_socket.sendall(message.encode('utf-8'))  # Send message to the server

    response = client_socket.recv(1024).decode('utf-8')  # Receive response from the server
    print(f"Client {client_id} received: {response}")  # Print the server's response
    
if __name__ == "__main__":
    main()