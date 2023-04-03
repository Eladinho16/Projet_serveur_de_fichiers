import socket
import os

HOST = 'localhost'
PORT = 8001
BUFFER_SIZE = 4096
SERVER_DIRECTORY = "server_directory"

def HELP():
    print("==================== LIST OF COMMAND ====================")
    print("LIST : Display files on server")
    print("DOWNLOAD : Download a file from server")
    print("DEL :  Delete a file from server")
    print("NEW : Create a new file on server")
    print("DISCONNECT : Disconnect from server")
    print("HELP : Display list of all cammand")

def list_files(s):
   
    files = os.listdir(SERVER_DIRECTORY)
    if(len(files)==0):
        print("SERVER DIRECTORY EMPTY") 
    else :
        s.sendall("LIST".encode())
        file_list = s.recv(BUFFER_SIZE).decode()
    
        print(f"\nFiles on server:\n{file_list}")

def download_file(s):
   
    filename = input("\nEnter the filename to download: ")
    files = os.listdir(SERVER_DIRECTORY)
    s.sendall(f"GET {filename}".encode())
    response=s.recv(BUFFER_SIZE).decode()
    
    if filename in files :
        print(f"\nFile {filename} downloaded from server")
            
            
        with open(filename,"wb") as f :
            data = s.recv(BUFFER_SIZE)
            while data :
                f.write(data)
                data=s.recv(BUFFER_SIZE)
                    
    else:
        print("ERROR 402 : DOWNLOAD FAILED")
        print(f"\nERROR 401: FILE {filename} NOT FOUND ON SERVER\n")
        

def delete_file(s):
    filename = input("\nEnter the filename to delete: ")
    s.sendall(f"DEL {filename}".encode())
    response = s.recv(BUFFER_SIZE).decode()
    if response == "DELETED":
        print(f"\nFile {filename} deleted from server")
    else:
        print(f"ERROR 401: FILE {filename} NOT FOUND ON SERVER")

def create_file(s):
  
    filename = input("\nEnter the filename to create: ")
    s.sendall(f"NEW {filename}".encode())
    response = s.recv(BUFFER_SIZE).decode()
    if response == "CREATED":
        print(f"\nFile {filename} created on server")
    elif response == "EXISTS":
        print(f"\nFile {filename} already exists on server")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(" 200 : CONNECTED SUCCESSFULL ")
        print(f"==================== Connected to server on {HOST}:{PORT} ===================")
        
        while True:
            
            choice = input("\n>>>>>>>> ")
            
            if choice == "LIST":
                list_files(s)
            elif choice == "DOWNLOAD":
                download_file(s)
            elif choice == "DEL":
                delete_file(s)
            elif choice == "NEW":
                create_file(s)
            elif choice == "DISCONNECT" :
                s.sendall("DISCONNECT".encode())
                print("\n200 : DISCONNECTED SUCCESSFULL ")
                break
            elif choice == "HELP" :
                HELP()
            else:
                print("\n ERROR 403 : Invalid choice tape HELP for see all command ")

if __name__ == '__main__':
    main()
