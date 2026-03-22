import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('localhost', 8080))
server.listen(5)

print("Server is listening on port 8080...")

while True:
    conn, addr = server.accept()
    print(f"Connection from {addr}")

    data = conn.recv(1024).decode('utf-8')
    print(f"Received data: {data}")

    first_line = data.split('\n')[0]

    method, path, protocol = first_line.split()
    print(f"Method: {method}, Path: {path}, Protocol: {protocol}")

    body = "Hallo von Cloudmind!"
    response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(body)}\r\n\r\n{body}"

    conn.sendall(response.encode('utf-8'))
    conn.close()
    