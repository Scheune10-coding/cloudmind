import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('localhost', 8080))
server.listen(5)

while True:
    conn, addr = server.accept()
    print(f"Connection from {addr}")

    data = conn.recv(1024).decode('utf-8')
    print(f"Received data: {data}")

    first_line = data.split('\n')[0]
    
    method, path, protocol = first_line.split()
    print(f"Method: {method}, Path: {path}, Protocol: {protocol}")
    