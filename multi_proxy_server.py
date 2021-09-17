import socket, time, sys
from multiprocessing import Process

HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

def handle_request(addr, conn):
    print("Connected by", addr)
    full_data = conn.recv(BUFFER_SIZE)
    conn.sendall(full_data)
    conn.shutdown(socket.SHUT_RDWR)
    conn.close()

def main():

    external_host = "www.google.com"
    port = 80

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start: #start of proxy(connects to localhost)
        #bind, and set to listening mode
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_start.bind((HOST, PORT))
        proxy_start.listen(1)

        while True:
            conn, addr = proxy_start.accept()
            print("Connected by", addr)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end: #end of proxy(connects to google)
                print("Connecting to Google")
                remote_ip = get_remote_ip(external_host)
                proxy_end.connect((remote_ip, port))

                #multiprocessing

                conn, addr = proxy_end.accept() 
                p = Process(target=handle_request, args=(addr, conn))
                p.daemon = True
                p.start()
                print("Started process ", p)

            conn.close()

if __name__ == "__main__":
    main()