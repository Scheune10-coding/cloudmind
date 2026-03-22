import socket
import json

STATUS_TEXT = {
    200: "OK",
    404: "Not Found",
    400: "Bad Request",
    500: "Internal Server Error",
    401: "Unauthorized",
    403: "Forbidden",
    405: "Method Not Allowed",
    408: "Request Timeout",
    429: "Too Many Requests"
}

def route(path):
    path = path.split('?')[0]
    match path:
        case "/":
            data = {"message": "Willkommen bei CloudMind"}
            return json.dumps(data), 200
        case "/health":
            data = {"status": "ok"}
            return json.dumps(data), 200
        case _:
            data = {"error": "Not Found"}
            return json.dumps(data), 404

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('localhost', 8080))
server.listen(5)

print("Server is listening on port 8080...")


while True:
  try:
    
    conn, addr = server.accept()
    print(f"Connection from {addr}")

    data = conn.recv(1024).decode('utf-8')
    print(f"Received data: {data}")

    first_line = data.split('\n')[0]

    method, path, protocol = first_line.split()
    print(f"Method: {method}, Path: {path}, Protocol: {protocol}")

    body, status_code = route(path)
    status_text = STATUS_TEXT.get(status_code, "Unknown")
    response = f"HTTP/1.1 {status_code} {status_text}\r\nContent-Type: application/json\r\nContent-Length: {len(body)}\r\n\r\n{body}"

    conn.sendall(response.encode('utf-8'))

  except Exception as e:
    print(f"[ERROR]: {e}", file=sys.stderr)
    
  finally:
    conn.close()  

