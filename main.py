import socket
import threading
from concurrent.futures import ThreadPoolExecutor

LISTEN_PORT = 12345
MAX_REC_BYTES = 1024


def handle_forwarding(socket1, socket2):
    while True:
        request = socket1.recv(MAX_REC_BYTES)
        if not request:
            break
        socket2.sendall(request)


def handle_https_connect(c_socket, target_host, target_port):
    destination_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    destination_socket.connect((target_host, target_port))

    c_socket.sendall(b"HTTP/1.1 200 Connection established\r\n\r\n")

    t_read = threading.Thread(target=handle_forwarding, args=(c_socket, destination_socket,))
    t_write = threading.Thread(target=handle_forwarding, args=(destination_socket, c_socket,))

    t_read.start()
    t_write.start()
    t_read.join()
    t_write.join()
    c_socket.close()
    destination_socket.close()


def get_target(request_message):
    target = request_message.decode().split("\n")[0]
    http_verb, host, http_version = target.split()
    if http_verb == 'CONNECT':
        host, target_port = host.split(':')
    else:
        host = host.split('/')[2]
        target_port = 80
    return http_verb, host, int(target_port)


def handle_http_request(client_socket, target_host, target_port, initial_request):
    destination_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    destination_socket.connect((target_host, target_port))
    destination_socket.sendall(initial_request)
    client_socket.shutdown(socket.SHUT_RD)
    destination_socket.shutdown(socket.SHUT_WR)
    while True:
        response = destination_socket.recv(MAX_REC_BYTES)
        if not response:
            break
        # print(response)
        client_socket.sendall(response)
    client_socket.close()
    destination_socket.close()


def start_proxy_server():
    with ThreadPoolExecutor(max_workers=4) as executor:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('', LISTEN_PORT))
        server_socket.listen(10)
        while True:
            (client_socket, address) = server_socket.accept()
            executor.submit(start_worker, client_socket)


def start_worker(client_socket):
    initial_request = client_socket.recv(MAX_REC_BYTES)
    # print(initial_request)
    verb, target_host, target_port = get_target(initial_request)
    if verb == "CONNECT":
        handle_https_connect(client_socket, target_host, target_port)
    else:
        handle_http_request(client_socket, target_host, target_port, initial_request)


if __name__ == '__main__':
    start_proxy_server()
