#!/usr/bin/env python3
import socket, sys, os

#define address & buffer size
HOST = ""
GOOG_HOST = "www.google.com"
HTTP_PORT = 80
MY_PORT = 8002
BUFFER_SIZE = 4096

#create a tcp socket
def create_tcp_socket():
    print('Creating socket')
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except (socket.error, msg):
        print(f'Failed to create socket. Error code: {str(msg[0])} , Error message : {msg[1]}')
        sys.exit()
    print('Socket created successfully')
    return s

#get host information
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

def google_proxy(payload: bytes) -> bytes:
    '''
    Sends payload to google and returns reply
    Args: payload - exact data to send to google
    Returns: exact data returned from google
    '''

    full_data = b""
    try:
        #make the socket, get the ip, and connect
        sock = create_tcp_socket()

        remote_ip = get_remote_ip(GOOG_HOST)

        sock.connect((remote_ip , HTTP_PORT))
        print (f'Socket Connected to {GOOG_HOST} on ip {remote_ip}')

        payload_str = payload.decode('utf-8')
        payload_str = payload_str.replace("127.0.0.1", GOOG_HOST)
        payload = payload_str.encode()
        
        #send the data and shutdown
        print("proxy server is sending modified payload:", payload)
        sock.sendall(payload)
        sock.shutdown(socket.SHUT_WR)

        #continue accepting data until no more left
        while True:
            data = sock.recv(BUFFER_SIZE)
            if not data:
                 break
            full_data += data
    except Exception as e:
        print(e)
    finally:
        #always close at the end!
        sock.close()
    print("Server got a response from google.")
    return full_data

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        #QUESTION 3
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        s.bind((HOST, MY_PORT))
        #set to listening mode
        s.listen(2)
        
        #continuously listen for connections
        while True:
            conn, addr = s.accept()
            print("Connected by", addr)

            # Fork for part 8
            newpid = os.fork()
            if newpid == 0:
                #recieve data, send to google, then reply with googles response
                full_data = conn.recv(BUFFER_SIZE)
                print("Received data: ", full_data)
                google_response = google_proxy(full_data)
                print("Server is sending response to proxy_client")
                if google_response:
                    conn.sendall(google_response)
                conn.shutdown(socket.SHUT_RDWR)
                conn.close()
                break
            else:
                print("Parent lives on")

if __name__ == "__main__":
    main()

