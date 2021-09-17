#!/usr/bin/env python3
import socket
import time

#define address & buffer size
HOST = "" #local host
PORT = 8001
BUFFER_SIZE = 1024

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        #QUESTION 3
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        s.bind((HOST, PORT))
        #set to listening mode, Enable a server to accept connections
        s.listen(2) #it specifies the number of unaccepted connections that the system will allow before refusing new connections
        
        #continuously listen for connections
        while True:
            #conn is a new socket object usable to send and receive data on the connection, 
            #and address is the address bound to the socket on the other end of the connection.
            conn, addr = s.accept() 
            print("Connected by", addr)
            
            #recieve data, wait a bit, then send it back
            full_data = conn.recv(BUFFER_SIZE)
            time.sleep(0.5) # wait a little bit and echo it back
            conn.sendall(full_data) # send back to whoever send us data in the first place
            conn.close()

if __name__ == "__main__":
    main()
