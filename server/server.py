import socket
import sqlite3
import threading

# Setup SQLite Database
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

# Server Configuration
UDP_IP = "192.168.1.140"  # The IP address for the server
UDP_PORT = 5005
TCP_PORT = 5006  # Separate port for TCP

# UDP socket
udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_sock.bind((UDP_IP, UDP_PORT))

# TCP socket
tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_sock.bind((UDP_IP, TCP_PORT))
tcp_sock.listen()

print(f"Server is starting on UDP IP: {UDP_IP}:{UDP_PORT}")
print(f"Server is also starting on TCP IP: {UDP_IP}:{TCP_PORT}")


# Register user
def registerUser(name, ipAddress, udpSocket, tcpSocket, addr):
    try:
        # Check if the name already exists
        cursor.execute("SELECT * FROM users WHERE name=?", (name,))
        if cursor.fetchone():
            cursor.execute("SELECT rqNum FROM users WHERE name=?", (name,))
            existingRqNum = cursor.fetchone()[0]
            response = f"REGISTER-DENIED {existingRqNum} Name-Already-Exists"
        else:
            # Insert the new user into the database
            cursor.execute(
                "INSERT INTO users (name, ipAddress, udpSocket, tcpSocket) VALUES (?, ?, ?, ?)",
                (name, ipAddress, int(udpSocket), int(tcpSocket)),
            )
            conn.commit()
            rqNum = cursor.lastrowid
            response = f"REGISTERED {rqNum}"
    except Exception as e:
        rqNum = -1
        response = f"REGISTER-DENIED {rqNum} Error-{str(e)}"

    # Send the response to the client
    udp_sock.sendto(response.encode(), addr)


# Deregister user
def deregisterUser(rqNum, name, addr):
    try:
        # Check if the user exists
        cursor.execute("SELECT * FROM users WHERE name=?", (name,))
        if cursor.fetchone():
            # Delete the user from the database
            cursor.execute("DELETE FROM users WHERE name=?", (name,))
            conn.commit()
            response = f"DEREGISTERED {rqNum}"
        else:
            response = f"DEREGISTER-DENIED {rqNum} User-Not-Found"
    except Exception as e:
        response = f"DEREGISTER-DENIED {rqNum} Error-{str(e)}"

    # Send the response to the client
    udp_sock.sendto(response.encode(), addr)


# Handle incoming UDP messages
def udp_handler():
    while True:
        data, addr = udp_sock.recvfrom(1024)
        message = data.decode()
        print(f"Received message from {addr} via UDP: {message}")

        # Parse the received message
        dataParts = message.split(" ")
        command = dataParts[0]

        if command == "REGISTER":
            name = dataParts[1]
            ipAddress = dataParts[2]
            udpSocket = dataParts[3]
            tcpSocket = dataParts[4]
            registerUser(name, ipAddress, udpSocket, tcpSocket, addr)
        elif command == "DEREGISTER":
            rqNum = int(dataParts[1])
            name = dataParts[2]
            deregisterUser(rqNum, name, addr)
        else:
            response = f"INVALID-COMMAND"
            udp_sock.sendto(response.encode(), addr)


# Handle incoming TCP connections
def tcp_handler():
    while True:
        conn, addr = tcp_sock.accept()
        print(f"New TCP connection from {addr}")
        conn.sendall("Connected to TCP server.".encode())
        conn.close()


# Start UDP and TCP handlers in separate threads
udp_thread = threading.Thread(target=udp_handler)
tcp_thread = threading.Thread(target=tcp_handler)

udp_thread.start()
tcp_thread.start()
