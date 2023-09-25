import socket
import cv2
import balldetection2


# Set the host and port for the server
HOST = '127.0.0.1'
PORT = 8080

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the host and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen()

print(f"Server listening on {HOST}:{PORT}")

# Accept a new connection
client_socket, client_address = server_socket.accept()
print(f"Connected to {client_address}")

vs, lower, upper = balldetection2.camera_init()

while True:
    # Send data to Unity
    data_to_send = "Hello Unity!"
    client_socket.sendall(data_to_send.encode('utf-8'))

    # run ball detection algorithm
    balldetection2.ball_detection(vs, lower, upper)

    # if the 'q' key is pressed, stop the loop
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        balldetection2.end_camera(vs)


# Close the connection
client_socket.close()
