import socket

HOST, PORT = "localhost", 9999
data = "dasdsad "

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((HOST, PORT)) 
    d = str(data + "\n")
    sock.sendall(bytes("hi world","utf-8"))

    # Receive data from the server and shut down
    received = sock.recv(1024)
finally:
    sock.close()

print("Sent:     {}".format(data))
print("Received: {}".format(received))