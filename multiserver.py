#multiserver
import socket
import threading

def handle_client(client_socket,addr):
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
    
        