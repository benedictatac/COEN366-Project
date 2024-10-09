import socket, sqlite3

# Setup SQLite Database
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

# Create table to store the registered users (Bachar)

# Server Configuration
UDP_IP = "0.0.0.0"  # When testing, make sure that the ip address here is the machine that will run the server
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Server is starting on IP: {UDP_IP}:{UDP_PORT}")


# Register user
def registerUser(name, ipAddress, udpSocket, tcpSocket, addr):
    try:
        # Check if the name already exists
        cursor.execute("SELECT * FROM users WHERE name=?", (name,))
        # Retrieve the auto-incremented rqNum for this user
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
    sock.sendto(response.encode(), addr)


# Deregister user (Charles)


# Server loop to handle incoming messages
try:
    while True:
        data, addr = sock.recvfrom(1024)
        message = data.decode()
        print(f"Received message from {addr}: {message}")

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
            # deregisterUser function here
        else:
            response = f"INVALID-COMMAND {rqNum}"
            sock.sendto(response.encode(), addr)
finally:
    # Close the SQLite connection when the server shuts down
    conn.close()
