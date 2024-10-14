import socket

# Server address (must match the server's IP and UDP/TCP ports)
SERVER_IP = "192.168.1.140"
UDP_PORT = 5005
TCP_PORT = 5006  # Separate port for TCP

# Create UDP and TCP sockets
udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpSocket.bind(('', 0))  # Bind to an available local port
tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the TCP socket to the server's TCP port
tcpSocket.connect((SERVER_IP, TCP_PORT))


def registerUser(name, udpSocket, tcpSocket, ipAddress):
    try:
        localIP = socket.gethostbyname(socket.gethostname())
        udpPort = udpSocket.getsockname()[1]  # Get the assigned UDP port
        tcpPort = tcpSocket.getsockname()[1]  # Get the assigned TCP port
        message = f"REGISTER {name} {localIP} {udpPort} {tcpPort}"

        # Send the registration request to the server via UDP
        udpSocket.sendto(message.encode(), (SERVER_IP, UDP_PORT))

        # Receive the server's response
        response, addr = udpSocket.recvfrom(1024)
        print("Server response:", response.decode())
    except Exception as e:
        print(f"Error registering user: {e}")


def deregisterUser(rqNum, name):
    message = f"DEREGISTER {rqNum} {name}"
    udpSocket.sendto(message.encode(), (SERVER_IP, UDP_PORT))

    response, _ = udpSocket.recvfrom(1024)
    print("Server response:", response.decode())


def menu():
    print("Client started.")
    print("1. Register User")
    print("2. Deregister User")
    print("3. Exit")
    choice = input("Enter your choice: ")

    if choice == '1':
        name = input("Enter your name: ")
        ipAddress = socket.gethostbyname(socket.gethostname())
        registerUser(name, udpSocket, tcpSocket, ipAddress)
        print("Registration request sent.")
    
    elif choice == '2':
        rqNum = input("Enter request number: ")
        name = input("Enter your name: ")
        deregisterUser(int(rqNum), name)
    elif choice == '3':
        print("Exiting...")
        return
    else:
        print("Invalid choice. Please try again.")

    menu()


if __name__ == "__main__":
    menu()

    # Close the socket when done
    udpSocket.close()
    tcpSocket.close()
