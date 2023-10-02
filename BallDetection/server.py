import socket
import cv2
import balldetection2
import time

# Set the host and port for the server
HOST = '127.0.0.1'
PORT = 8080

# Create a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the host and port
# socket.bind((HOST, PORT))

# Listen for incoming connections
# socket.listen()

# print(f"Server listening on {HOST}:{PORT}")

# Accept a new connection
# client_socket, client_address = server_socket.accept()
# print(f"Connected to {client_address}")

sock.connect((HOST, PORT))

vs, lower, upper = balldetection2.camera_init()

while True:
    # run ball detection algorithm
    x, y, dist = balldetection2.ball_detection(vs, lower, upper, False)

    # Send data to Unity
    data_to_send = f"{x},{y},{dist}"
    # data_to_send = "1,2,3"  # test
    print(data_to_send)
    sock.sendall(data_to_send.encode("utf-8"))
    # client_socket.sendall(data_to_send.encode('utf-8'))

    time.sleep(1.0)

    # if the 'q' key is pressed, stop the loop
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        balldetection2.end_camera(vs)
        break


# Close the connection
sock.close()
