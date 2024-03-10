import socket

client = socket.socket()

try:
    client.connect(('localhost', 8080)) # maybe will fail to connect, add exception judgment
    while True:
        client.send('hello'.encode('utf-8'))
        recv_data = client.recv(1024)
        if not recv_data:
            break
        print(recv_data.decode('utf-8'))
except Exception:
    client.close()