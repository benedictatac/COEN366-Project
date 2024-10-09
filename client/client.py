import socket

# Server address (must match the server's IP and UDP port)
SERVER_IP = (
    "0.0.0.0"  # Change this to the machine that will run the server's IP address
)
SERVER_PORT = 5005

# Might need to instantiate TCP socket here as well


clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def registerUser(name, ipAddress, udpSocket, tcpSocket):

    localIP = socket.gethostbyname(socket.gethostname())
    message = f"REGISTER {name} {localIP} {udpSocket} {tcpSocket}"
    # Send the registration request to the server
    clientSocket.sendto(
        message.encode(),
        (SERVER_IP, SERVER_PORT),
    )

    # Receive the server's response
    response, addr = clientSocket.recvfrom(1024)
    print(response.decode())

    # Display the server's response
    print("Server response:", response.decode())


# create deregisterUser function here (Charles)


def menu():
    print("1. Register User")
    print("2. Deregister User")
    print("3. Exit")
    choice = input("Enter your choice: ")

    match choice:
        case "1":
            name = input("Enter your name: ")
            udpSocket = input("Enter your UDP socket: ")
            tcpSocket = input("Enter your TCP socket: ")
            registerUser(name, SERVER_IP, udpSocket, tcpSocket)
        case "2":
            rqNum = input("Enter your rqNum: ")
            name = input("Enter your name: ")
            # call the deregisterUser function here
        case "3":
            print("Exiting...")
            exit()
        case _:
            print("Invalid choice")
            menu()


if __name__ == "__main__":
    print("Client started.")
    menu()

    # Close the socket when done
    clientSocket.close()
