import socket
import threading

# Constants
TCP_PORT = 12345
UDP_PORT = 12346
BUFFER_SIZE = 1024

# Function to handle TCP connections
def handle_tcp_client(client_socket):
    while True:
        data = client_socket.recv(BUFFER_SIZE)
        if not data:
            break
        print(f"Received TCP data: {data.decode()}")
        client_socket.sendall(data)
    client_socket.close()

# Function to handle UDP connections
def handle_udp_client(udp_socket):
    while True:
        data, addr = udp_socket.recvfrom(BUFFER_SIZE)
        print(f"Received UDP data from {addr}: {data.decode()}")
        udp_socket.sendto(data, addr)

# Main server function
def start_server():
    # TCP server setup
    tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server.bind(('0.0.0.0', TCP_PORT))
    tcp_server.listen(5)
    print(f"TCP server listening on port {TCP_PORT}")

    # UDP server setup
    udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_server.bind(('0.0.0.0', UDP_PORT))
    print(f"UDP server listening on port {UDP_PORT}")

    # Start UDP handler thread
    udp_thread = threading.Thread(target=handle_udp_client, args=(udp_server,))
    udp_thread.start()

    # Handle TCP clients
    while True:
        client_socket, addr = tcp_server.accept()
        print(f"Accepted TCP connection from {addr}")
        tcp_thread = threading.Thread(target=handle_tcp_client, args=(client_socket,))
        tcp_thread.start()

if __name__ == "__main__":
    start_server()