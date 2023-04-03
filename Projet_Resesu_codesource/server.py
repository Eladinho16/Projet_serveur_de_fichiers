import os
import socket
import threading

HOST = 'localhost'
PORT = 8001
BUFFER_SIZE = 4096
SERVER_DIRECTORY = "server_directory"

def list_files():
    files = os.listdir(SERVER_DIRECTORY)
    if (len(files) == 0):
        return 0
        
    else:
               
        return files

def send_file(conn, filename):
    filepath = os.path.join(SERVER_DIRECTORY, filename)
    if os.path.exists(filepath):
        
        
        
        conn.sendall("FOUND" .encode())
        
        with open(filepath, 'rb') as f:
            data = f.read(BUFFER_SIZE)
            while data:
                conn.sendall(data)
                data = f.read(BUFFER_SIZE)
        print(f"File {filename} sent to client")
        
    else:
        conn.sendall("NOT FOUND".encode())
        print(f"ERROR 401: FILE {filename} NOT FOUND ON SERVER")
        

def delete_file(filename):
    filepath = os.path.join(SERVER_DIRECTORY, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        print(f"File {filename} deleted from server")
        return "DELETED"
    else:
        print(f"ERROR 401: FILE {filename} NOT FOUND ON SERVER")
        return "NOT FOUND"

def create_file(filename):
    filepath = os.path.join(SERVER_DIRECTORY, filename)
    if os.path.exists(filepath):
        print(f"File {filename} already exists on server")
        return "EXISTS"
    else:
        with open(filepath, 'w') as f:
            f.write("This is a new file created on the server")
        print(f"File {filename} created on server")
        return "CREATED"

def client_handler(conn, addr):
    print(f"Connected by {addr}")
    while True:
        data = conn.recv(BUFFER_SIZE).decode()
        if data.startswith("LIST"):
            files = list_files()
            if(files == 0):
                print("SERVER DIRECTORY EMPTY")
            else :
                file_list = "\n".join(files)
                conn.sendall(file_list.encode())
        elif data.startswith("GET"):
            filename = data[4:]
            send_file(conn, filename)
        elif data.startswith("DEL"):
            filename = data[4:]
            response = delete_file(filename)
            conn.sendall(response.encode())
        elif data.startswith("NEW"):
            filename = data[4:]
            response = create_file(filename)
            conn.sendall(response.encode())
        elif data == "DISCONNECT":
            print(f"Client {addr} has disconnected")
            conn.close()
            break

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5) # nombre de connexions simultanées autorisées
    print(f"Server is listening on {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()
        client_thread = threading.Thread(target=client_handler, args=(conn, addr))
        client_thread.start()

if __name__ == '__main__':
    main()
