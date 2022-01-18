#!/usr/bin/env python3
import socket
import time
import os

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        #QUESTION 3
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        s.bind((HOST, PORT))
        #set to listening mode
        s.listen(2)
        
        #continuously listen for connections
        while True:
            conn, addr = s.accept()
            print("Connected by", addr)
            print("conn: ", conn)

            newpid = os.fork()
            if newpid == 0:
                #recieve data, wait a bit, then send it back
                full_data = conn.recv(BUFFER_SIZE)
                print("full_data: ", full_data)
                time.sleep(0.5)
                conn.sendall(full_data)
                conn.shutdown(socket.SHUT_RDWR)
                conn.close()
            else:
                print("Parent lives on")


if __name__ == "__main__":
    main()
